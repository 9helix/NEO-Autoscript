from datetime import date
import webbrowser
import regex as re
from success import *
from config import *

today = date.today()
date = today.strftime("%Y-%m-%d")
year = date[:4]
month = date[5:7]
day = date[8:]

cacheFile = open("cache.py", 'r')
cont = cacheFile.read()
cacheFile.close()

if cont == '':
    from selenium_script_fetch import *
else:
    from cache import *

if fetch_date != date:
    from selenium_script_fetch import *


def timeAdd(obs_time):
    obs_hr = int(obs_time[:2])
    obs_min = int(obs_time[2:])
    obs_min += round((obs_interval+exposure*24/60)/10)*10
    #print(obs_hr, obs_min)
    while obs_min >= 60:
        obs_hr += 1
        obs_min -= 60
    while obs_hr >= 24:
        obs_hr -= 24
    if len(str(obs_hr)) == 1:
        obs_hr = '0'+str(obs_hr)
    if len(str(obs_min)) == 1:
        obs_min = '0'+str(obs_min)
    global obs_time_target
    obs_time_target = str(obs_hr)+str(obs_min)
    # print(obs_time_target)


def custom_list_sort(start):
    global content_list
    sorted_list = []
    loc = content_list.index(start)
    sorted_list.append(start)
    br = 1
    while loc+br < len(content_list):
        sorted_list.append(content_list[loc+br])
        br += 1
    br = 0
    while br < loc:
        sorted_list.append(content_list[br])
        br += 1

    content_list = sorted_list.copy()
    # print(content_list)


def exposure_def(mag):
    # global exposure
    if mag < 18.5:
        exposure = 10
    if 18.5 <= mag < 20:
        exposure = 15
    if 20 <= mag < 20.3:
        exposure = 30
    if 20.3 <= mag < 21:
        exposure = 60
    if mag >= 21:
        exposure = 180
    return exposure


#   ↓ TEXT PROCESSING ↓
script = open('script_unprocessed.txt', 'r')
content = script.read()
script.close()

extra_start = """Quick links : Home Page : Contact Us : Index : Site Map : Search Site
NEO Confirmation Page: Query Results
Below are the results of your request from the Minor Planet Center's NEO Confirmation Page.
Use the feedback form to report problems or to comment on this page.
Ephemerides are for observatory code L01.
"""
extra_end = """
These calculations have been performed on the Tamkin Foundation Computing Network."""
if ephem_interval == 60:
    top = """Date       UT   *  R.A. (J2000) Decl.  Elong.  V        Motion     Object     Sun         Moon        Uncertainty
            h                                        "/min   P.A.  Azi. Alt.  Alt.  Phase Dist. Alt."""
    top2 = """Date       UT      R.A. (J2000) Decl.  Elong.  V        Motion     Object     Sun         Moon        Uncertainty
            h                                        "/min   P.A.  Azi. Alt.  Alt.  Phase Dist. Alt."""
else:
    top = """Date       UT   *  R.A. (J2000) Decl.  Elong.  V        Motion     Object     Sun         Moon        Uncertainty
            h m                                      "/min   P.A.  Azi. Alt.  Alt.  Phase Dist. Alt."""
    top2 = """Date       UT      R.A. (J2000) Decl.  Elong.  V        Motion     Object     Sun         Moon        Uncertainty
            h m                                      "/min   P.A.  Azi. Alt.  Alt.  Phase Dist. Alt."""

content = content.replace(extra_start, '')
content = content.replace(extra_end, '')
content = content.replace("""
Get the observations or orbits.""", '')
content = content.replace("\n... <suppressed> ...", '')
content_list = re.split('(\n \n)', content)
img_batch = '  24 x 60 sec'
limit = len(content_list)
# global limiter

verified = []
backup = []


def mainloop(count=0):
    global fast, empty, exposure, content_list, backup
    fast = {}
    empty = ''
    asteroids = {}
    for asteroid in content_list:
        if asteroid[-1] != '.':
            desig = asteroid[:asteroid.find('\n')]
            data = asteroid[asteroid.find(f'{year}'):]
            if '\n \n' == asteroid and (empty == '' or empty[-1] != '\n'):
                empty += asteroid
                ok = True
            if desig in mag_dict and '\n\n \n' != asteroid and data != ' ':
                # print(f'{desig} began processing')
                speed = float(data[53:58].strip())
                if speed >= 10:
                    fast[desig] = str(speed)+' "/min'
                line_start = 0
                line_end = 0
                if obs_start == '' and 'Map' not in empty:
                    ok = True
                    line_end = data.find('\n', line_start+1)
                    data = data.replace(data[line_end+1:], '\n')
                    line = data[line_start:line_end]

                    obs_time = data[11:15]

                    mag = float(line[46:50])
                    # print(mag)
                    exposure = exposure_def(mag)
                    # print(exposure)
                    timeAdd(obs_time)
                    verified.append(desig)

                else:
                    if 'Map' in empty:  # TODO: find object with earliest time; put it on the beggining and sort so that telescope movement still remains minimal
                        line_time = data.find(obs_time_target)
                        if line_time != -1:
                            ok = True
                            line_start = line_time-11
                            line_end = data.find('\n', line_time)
                            line = data[line_start:line_end]
                            # print(line)
                            data = line
                            mag = float(line[46:50])
                            # print(mag)
                            exposure = exposure_def(mag)
                            # print(exposure)
                            timeAdd(obs_time_target)
                            verified.append(desig)

                        elif desig not in verified:
                            print('here')
                            verified.append(desig)

                            # print(
                            #   f"target date {obs_time_target} not found in {desig}")
                            asteroid, content_list[content_list.index(
                                asteroid)-2] = content_list[content_list.index(asteroid)-2], asteroid
                            # custom_list_sort(asteroid)
                        else:
                            ok = False
                if ok:
                    img_batch = f'  24 x {exposure} sec'
                    desig += img_batch
                    asteroid = desig+'\n'+data
                    empty += asteroid
                    asteroids[desig] = data


mainloop()
empty = empty.replace('\n'+top, '')
empty = empty.replace('\n'+top2, '')
empty = top+"\n\n"+empty
print('Attention! The following asteroids have high speeds: ')
for i in fast:
    print(i+"   " + fast[i])
test = open('test.txt', 'w')
test.write(empty)
test.close()

#   ↓ WRITING TO FILE ↓
'''
# script = open(f'{d1}test.txt', 'w')
script = open(f'test.txt', 'w')
script.write(content)
script.close()
'''
# webbrowser.open(f'{d1}test.txt') used when testing is finished
# webbrowser.open(f'test.txt')

done('Processing done!')
# TODO: maybe at the end add function in which user can input asteroid name, and it will take himto the link of the uncertainty map for the asteroid, when acquiring data then, try to store the map links
