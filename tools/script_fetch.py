import os
import sys
cwd = os.getcwd()
sys.path.insert(1, cwd+'\src')
import requests
from datetime import datetime
from html.parser import HTMLParser
from xml.etree import ElementTree
from urllib.parse import urlparse, parse_qs
from utils import PersistentData, jd_to_hhmmss
from config import Settings, DATA_DIR, NEOCONFIRM_URL, NEOCONFIRM_CGI



class TableParser(HTMLParser):

    excluded = 'input', 'thead', 'tbody', 'span', 'center', 'a'

    def __init__(self, search_attrs):
        super().__init__(convert_charrefs=False)
        self.search_attrs = search_attrs.items()
        self.prev_cell = (None, 0)
        self.skip_next = False
        self.in_table = False
        self.table = []

    def handle_starttag(self, tag, attrs):
        if tag != 'table' and not self.in_table:
            # Not in <table>, skip
            return
        elif tag in self.excluded:
            # Do not open unsupported tags (ElementTree)
            if tag in ('input', 'center'):
                # Skip duplicated strings
                self.skip_next = True
            return
        elif self.in_table:
            # Fix successive unclosed tags, e.g. <tr>...<tr><tr>...<tr>
            if tag == self.prev_cell[0]:
                self.table[self.prev_cell[1]] = f'</{tag}>'
            self.prev_cell = tag, len(self.table)
            self.table.append(f'<{tag}>')
        elif any((k, v) in self.search_attrs for k, v in attrs):
            # Reached start of table with matching search_attrs
            self.in_table = True
            self.table.append('<table>')

    def handle_endtag(self, tag):
        if tag == 'table' and self.in_table:
            # Reached end of <table>
            self.in_table = False
            self.table.append('</table>')
        if tag == 'span':
            # Keep raw value from <span>, skip formatted value
            self.skip_next = True
        elif self.in_table and tag not in self.excluded:
            # Close current tag
            self.prev_cell = (None, 0)
            self.table.append(f'</{tag}>')

    def handle_data(self, data):
        if self.in_table:
            if self.skip_next:
                self.skip_next = False
                return
            self.table.append(data.strip())

    def to_dictlist(self):
        # Return a list of table records, {headers: values}
        table = ElementTree.fromstringlist(self.table)
        rows = iter(table)
        headers = [col.text for col in next(rows)]
        return [
            dict(zip(headers, [col.text for col in row]))
            for row in rows
        ]


class ResponseParser(HTMLParser):

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.prev_link = None
        self.content = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and 'href' in attrs[0][0]:
            self.prev_link = attrs[0][1]

    def handle_data(self, data):
        if data == 'Map':
            self.links.append(self.prev_link)
        self.content.append(data)

    def to_str(self):
        return ''.join(self.content)

    def parse_links(self):
        return [
            (qs['Obj'][0], qs['JD'][0]) for qs in
            map(lambda i: parse_qs(i.query), map(urlparse, self.links))
        ]

print('Fetching data...')
# Find and parse table on NEO confirmation page
tp = TableParser({'class': 'tablesorter'})
tp.feed(requests.get(NEOCONFIRM_URL).text)
table = tp.to_dictlist()


def ra_sort(e):
    if e['R.A.'] != None:
        return float(e['R.A.'])
    else:
        return 360


table.sort(key=ra_sort)

# Build query payload
form_data = {
    'mb': '-30', 'mf': '30',
    'dl': '-90', 'du': '+90',
    'nl': '0', 'nu': '100',
    'sort': 'd', 'W': 'j',
    'obj': [
        # Exclude 'Moved to PCCP' objects
        record['Temp Desig'] for record in table if record['V']
    ],
    'Parallax': '1',
    'obscode': Settings.obs_code,
    'long': '', 'lat': '', 'alt': '',
    'int': Settings.ephem_interval.value,
    'start': '0', 'raty': 'a',
    'mot': 'm', 'dmot': 'p',
    'out': 'f', 'sun': 'n',
    'oalt': Settings.min_alt,
}

form_headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Send query to CGI endpoint
response = requests.post(NEOCONFIRM_CGI, data=form_data, headers=form_headers)

# Collect uncertainty map URLs and filter tags from HTML text
rp = ResponseParser()
rp.feed(response.text)
response_text = rp.to_str()
qs_list = rp.parse_links()

# Store processed data
print('Writing data...')
now = datetime.now().strftime('%Y-%m-%d')
path = os.path.join(DATA_DIR, now, f'{now}-raw.txt')

try:

    open(f'output/{now}/neocp.html', 'w').write(response.text)
except:
    os.mkdir(f'output/{now}/')
    open(f'output/{now}/neocp.html', 'w').write(response.text)

os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'wt') as f:
    f.write(response_text)

PersistentData.fetch_date = now
PersistentData.mag_dict = {
    record['Temp Desig']: -mag+50
    for record in table
    for mag in [float(record['V'] or 0)]
    if mag and -mag+50 <= Settings.max_mag
}

PersistentData.map_dict = {
    f'{qs[0]} {jd_to_hhmmss(qs[1])}': link
    for qs, link in zip(qs_list, rp.links)
}
print('Fetching data complete!')
input("\nPress ENTER to continue...")
