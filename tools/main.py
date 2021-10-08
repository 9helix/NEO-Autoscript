from math import *
from datetime import date
import os
import sys
cwd = os.getcwd()
sys.path.insert(1, cwd+'\src')
from utils import PersistentData
from config import Settings, DATA_DIR

today = date.today()
date = today.strftime("%Y-%m-%d")
year = date[:4]
month = date[5:7]
day = date[8:]

try:
    if PersistentData.fetch_date != date:
        from script_fetch import *
except:
    from script_fetch import *
mag_dict=PersistentData.mag_dict


def timeAdd(obs_time):
    obs_hr = int(obs_time[:2])
    obs_min = int(obs_time[2:])
    obs_min += ceil((Settings.obs_interval+exposure*img_num/60)/10)*10
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
    time_target = str(obs_hr)+str(obs_min)
    return time_target


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


def batch_def(exposure):
    if exposure == 10:
        img_num = 24
    if exposure == 15:
        img_num = 24
    if exposure == 30:
        img_num = 24
    if exposure == 60:
        img_num = 24
    if exposure == 120:
        img_num = 12
    if exposure == 180:
        img_num = 8
    return img_num


def split(string, delimiter):
    s = string
    d = delimiter
    counter = 1
    x = s.split(d)
    while counter <= len(x)-1:
        if counter <= len(x)-1:
            x.insert(counter, d)
        elif x[len(x)-1] == '':
            x.insert(counter, d)
            x.remove(x[len(x)-1])
        counter += 2
    return x


#   ↓ TEXT PROCESSING ↓
script = open(f'output\{date}\{date}-raw.txt', 'r')
content = script.read()
script.close()

extra_start = """



NEO Confirmation Page: Query Results



Quick links :
  Home Page  :
  Contact Us  :
  Index  :
  Site Map  :
  Search Site 

NEO Confirmation Page: Query Results
Below are the results of your request from the Minor Planet Center's
NEO Confirmation Page.

Use the feedback form to report
problems or
to comment on this page.

   Ephemerides are for
 observatory code L01.
 
"""
extra_end = """
 

These calculations have been performed on the
Tamkin
Foundation Computing Network.


      



"""
spacing = '\n \n \n'

top = """Date       UT   *  R.A. (J2000) Decl.  Elong.  V        Motion     Object     Sun         Moon        Uncertainty
            h m                                      "/min   P.A.  Azi. Alt.  Alt.  Phase Dist. Alt."""
top2 = """Date       UT      R.A. (J2000) Decl.  Elong.  V        Motion     Object     Sun         Moon        Uncertainty
            h m                                      "/min   P.A.  Azi. Alt.  Alt.  Phase Dist. Alt."""

content = content.replace(extra_start, '')
content = content.replace(extra_end, '')
content = content.replace("""
Get the observations or orbits.""", '')
content = content.replace("\n... suppressed ...", '')
content_list = split(content, spacing)
limit = len(content_list)

times = {}
fast = {}
asteroids = {}
prefix = "* "

for asteroid in content_list:
    if asteroid != spacing:
        desig = asteroid[1:asteroid.find('\n')]
        data = asteroid[asteroid.find(f'{year}'):]

        if desig in mag_dict and asteroid.find(f'{year}') != -1 and data != asteroid[len(asteroid)-1]:
            #print('\n' in data)
            #line_end = data.find('\n')
            #data = data.replace(data[line_end+1:], '\n')
            obs_time = data[11:15]  # earliest asteroids time
            obs_hr = int(obs_time[:2])
            obs_min = int(obs_time[2:])
            if obs_hr < 10:
                obs_hr += 24
            obs_total = obs_hr*60+obs_min
            times[desig+'\n' +
                  asteroid[asteroid.find(f'{year}'):]+'\n\n'] = obs_total


times_sorted = dict(sorted(times.items(), key=lambda item: item[1]))
test = open(f'output\{date}\{date}-time-sorted.txt', 'w')
for asteroid in times_sorted:
    test.write(asteroid)
test.close()
# print(times_sorted)
asteroids = [top+'\n\n']
excluded = []
for asteroid in times_sorted:
    skip = False
    desig = asteroid[:asteroid.find('\n')]
    data = asteroid[asteroid.find('\n')+1:]
    if Settings.obs_start == None:
        if len(asteroids) == 1:
            line_end = data.find('\n')
            data = data[:line_end]
            time = data[11:15]
            mag = float(data[46:50])
            exposure = exposure_def(mag)
            img_num = batch_def(exposure)
            obs_time_target = timeAdd(time)
            # print(obs_time_target)
        else:
            #print(desig, time, obs_time_target)
            target_loc = data.find(obs_time_target)
            if target_loc != -1:
                data = data[target_loc-11:target_loc+102]
                # print(data)
                time = data[11:15]
                mag = float(data[46:50])
                exposure = exposure_def(mag)
                img_num = batch_def(exposure)
                obs_time_target = timeAdd(time)
                #print(time, obs_time_target)
            else:
                line_end = data.find('\n')
                line = data[:line_end]
                time = line[11:15]
                mag = float(line[46:50])
                exposure = exposure_def(mag)
                img_num = batch_def(exposure)
                skip = True
    else:

        if len(asteroids) == 1:
            obs_time_target = Settings.obs_start
        target_loc = data.find(obs_time_target)
        if target_loc != -1:
            data = data[target_loc-11:target_loc+102]
            # print(data)
            time = data[11:15]
            mag = float(data[46:50])
            exposure = exposure_def(mag)
            img_num = batch_def(exposure)
            obs_time_target = timeAdd(time)
            #print(time, obs_time_target)
        else:
            line_end = data.find('\n')
            line = data[:line_end]
            time = line[11:15]
            mag = float(line[46:50])
            exposure = exposure_def(mag)
            img_num = batch_def(exposure)
            skip = True
    speed = float(data[53:58].strip())
    if speed >= Settings.min_speed:
        fast[desig] = str(speed)+' "/min'
    img_batch = f'  {img_num} x {exposure} sec'
    desig += img_batch
    asteroid = prefix+desig+'\n'+data+'\n\n'
    if not skip:
        asteroids.append(asteroid)
    else:
        excluded.append(asteroid[:len(asteroid)-2])
# print(excluded)
#   ↓ FILE WRITING ↓

# print(asteroids)
f = open(f'output/{date}/{date}-log.txt', 'w')
for i in asteroids:
    f.write(i)
f.close()

f = open(f'output/{date}/{date}-excluded.txt', 'w')
for i in excluded:
    f.write(i)
f.close()

if fast != {}:
    print('Attention! The following asteroids have high speeds: ')
    for i in fast:
        if i not in excluded:
            print(i+"   " + fast[i])

if len(excluded) > 0:
    print(f'\n{len(asteroids)-1} asteroids are in the script!')
    print(f"{len(excluded)} asteroids didn't fit in the script & have been moved to excluded.txt file.")
else:
    print('\nAll asteroids are in the script!')

if Settings.post_open_script:
    os.startfile(f'output\{date}\{date}-log.txt')
if Settings.post_open_excluded:
    if len(excluded) != 0:
        os.startfile(f'output\{date}\{date}-excluded.txt')
#print('\nProcessing done!')

input("\nPress ENTER to close...")
