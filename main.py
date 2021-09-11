# TODO: try putting interactable files in tools/ and importing via sys
from datetime import date
import regex as re
from src.config import *
from math import *
import os
from src.success import *

today = date.today()
date = today.strftime("%Y-%m-%d")
year = date[:4]
month = date[5:7]
day = date[8:]

cacheFile = open("src/shared_var.py", 'r')
cont = cacheFile.read()
cacheFile.close()

if cont == '':
    from script_fetch import *
else:
    from src.shared_var import mag_dict, fetch_date

if fetch_date != date:
    from script_fetch import *


def timeAdd(obs_time):
    obs_hr = int(obs_time[:2])
    obs_min = int(obs_time[2:])
    obs_min += ceil((obs_interval+exposure*img_num/60)/10)*10
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


#   ↓ TEXT PROCESSING ↓
script = open(fr'output\{date}\{date}-raw.txt', 'r')
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

times = {}
fast = {}
asteroids = {}
all_asteroids = {}
for asteroid in content_list:
    if asteroid[-1] != '.':
        desig = asteroid[:asteroid.find('\n')]
        data = asteroid[asteroid.find(f'{year}'):]

        if desig in mag_dict and '\n\n \n' != asteroid and data != ' ':
            # print(f'{desig} began processing')
            line_start = 0
            line_end = 0
            line_end = data.find('\n', line_start+1)
            if line_end != -1:
                data = data.replace(data[line_end+1:], '\n')
                line = data[line_start:line_end]
            # print(data)
            obs_time = data[11:15]  # earliest asteroids time
            obs_hr = int(obs_time[:2])
            obs_min = int(obs_time[2:])
            if obs_hr < 10:
                obs_hr += 24
            obs_total = obs_hr*60+obs_min
            asteroid = asteroid.replace('\n'+top, '')
            asteroid = asteroid.replace('\n'+top2, '')
            asteroid += '\n\n'
            times[asteroid] = obs_total
            all_asteroids[desig] = asteroid


times_sorted = dict(sorted(times.items(), key=lambda item: item[1]))
# print(times_sorted)
test = open(f'output\{date}\{date}-time-sorted.txt', 'w')
for i in times_sorted:
    test.write(i)
test.close()

asteroids = [top+'\n\n']
excluded = {}
for asteroid in times_sorted:
    skip = False
    desig = asteroid[:asteroid.find('\n')]
    data = asteroid[asteroid.find('\n')+1:asteroid.find('\n\n')]
    if obs_start == '':
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
            obs_time_target = obs_start
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
    if speed >= min_speed:
        fast[desig] = str(speed)+' "/min'
    img_batch = f'  {img_num} x {exposure} sec'
    desig += img_batch
    asteroid = desig+'\n'+data+'\n\n'
    if not skip:
        asteroids.append(asteroid)
    else:
        excluded[asteroid[:asteroid.find(' ')]] = asteroid

#   ↓ FILE WRITING ↓

# print(asteroids)
f = open(f'output/{date}/{date}-log.txt', 'w')
for i in asteroids:
    f.write(i)
f.close()
f = open(f'output/{date}/{date}-excluded.txt', 'w')
for i in excluded.values():
    f.write(i)
f.close()
print('Attention! The following asteroids have high speeds: ')
for i in fast:
    if i not in excluded:
        print(i+"   " + fast[i])
if len(excluded) > 0:
    print(f'\n{len(asteroids)} asteroids are in the script!')
    print(f"{len(excluded)} asteroids didn't fit in the script & have been moved to excluded.txt file.")
else:
    print('\nAll asteroids are in the script!')

if open_script:
    os.startfile(f'output\{date}\{date}-log.txt')
if open_excluded:
    if len(excluded) != 0:
        os.startfile(f'output\{date}\{date}-excluded.txt')
#print('\nProcessing done!')

done('Processing done!')
