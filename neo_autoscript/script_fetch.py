import requests
from html.parser import HTMLParser
from xml.etree import ElementTree
from neo_autoscript.config import Settings, NEOCONFIRM_URL, NEOCONFIRM_CGI


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


# Find and parse table on NEO confirmation page
tp = TableParser({'class': 'tablesorter'})
tp.feed(requests.get(NEOCONFIRM_URL).text)
table = tp.to_dictlist()

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

# TODO: rewrite rest of script
open('neocp.html', 'w').write(response.text)
