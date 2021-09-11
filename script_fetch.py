from src.success import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import date
from src.config import *
import os


intervals = {60: 1, 30: 2, 10: 3, 1: 4}
row_num = 0
browsers = {'Chrome': webdriver.Chrome, 'Firefox': webdriver.Firefox, 'Edge': webdriver.Edge,
            'Ie': webdriver.Ie, 'Safari': webdriver.Safari, 'Opera': webdriver.Opera}

#   ↓ DATA ACQUISITION ↓
driver = browsers[browser]()

driver.get('https://www.minorplanetcenter.net/iau/NEO/toconfirm_tabular.html')

if obs_code != "":
    obs_box = driver.find_element_by_xpath(
        '//*[@id="main"]/form/p[8]/input[3]')
    obs_box.clear()
    obs_box.send_keys(f'{obs_code}')

supress = Select(driver.find_element_by_name('sun'))
supress.select_by_value('n')

if ephem_interval != 60:
    interval = driver.find_element_by_xpath(
        f'//*[@id="main"]/form/p[13]/input[{intervals[ephem_interval]}]')
    interval.click()

sel_all = driver.find_element_by_xpath(
    '//*[@id="main"]/form/p[4]/input[3]')
sel_all.click()

sort_ra = driver.find_element_by_xpath(
    '//*[@id="main"]/form/p[5]/table/thead/tr/th[4]')
sort_ra.click()

alt = driver.find_element_by_name('oalt')
alt.clear()
alt.send_keys(f'{min_alt}')

mag_dict = {}
success = 0
run = True
while run:
    try:
        while True:
            row_num += 1
            desig = driver.find_element_by_xpath(
                f'//*[@id="main"]/form/p[5]/table/tbody/tr[{row_num}]/td[1]').text.strip()
            mag = driver.find_element_by_xpath(
                f'//*[@id="main"]/form/p[5]/table/tbody/tr[{row_num}]/td[6]').text.strip()
            #print(mag, desig)
            if mag != '' and float(mag) <= max_mag:
                mag = float(mag)
                mag_dict[desig] = mag
            success += 1
    except:
        if success > 0:
            run = False

get_ephem = driver.find_element_by_xpath('//*[@id="main"]/form/input[1]')
get_ephem.click()


content = driver.find_element_by_xpath('/html/body').text
map_links = driver.find_elements_by_partial_link_text("Map")
map_dict = {}
map_list = []
for map_link in map_links[1:]:
    link = map_link.get_attribute("href")
    map_list.append(link)
    # print(link)

    obj = link[link.find('=')+1:link.find('&')]
    JDtime = link[link.find('&')+4:link.find('&Ext')]

    decimal_part = JDtime[JDtime.find('.')+1:]
    decimal_part = float(decimal_part)/(10**len(decimal_part))+0.5
    day_decimal = str(decimal_part*24)
    hr_decimal = day_decimal[:day_decimal.find('.')]

    min_decimal = str(round(float(day_decimal.replace(hr_decimal, ''))*60))
    #min_decimal = min_decimal[:min_decimal.find('.')]
    if len(hr_decimal) == 1:
        hr_decimal = '0'+hr_decimal
    if len(min_decimal) == 1:
        min_decimal = '0'+min_decimal
    time = hr_decimal+min_decimal
    #print(JDtime, time)
    map_dict[obj+' '+time] = (map_link.get_attribute("href"))

# print(map_list)

#   ↓ FILE WRITING ↓

today = date.today()
fetch_date = today.strftime("%Y-%m-%d")

parent_dir = os.getcwd()+"\output"
directory = f"{fetch_date}"
path = os.path.join(parent_dir, directory)
# print(path)
os.mkdir(path)

script = open(f'output/{fetch_date}/{fetch_date}-raw.txt', 'w')
script.write(content)
script.close()
driver.quit()

mag_dict = dict(sorted(mag_dict.items(), key=lambda item: item[1]))
print(len(mag_dict), 'suitable asteorids found.')
var = open('src/shared_var.py', 'w')
var.write('mag_dict='+str(mag_dict)+'\n')
var.write('fetch_date = ' + "'" + fetch_date+"'\n")
var.write('map_dict = ' + str(map_dict))
var.close()
done('Fetching data complete!')
