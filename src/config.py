obs_code = 'L01'       # observatory code
ephem_interval = 10    # ephemeris interval in minutes 60/30/10/1
max_mag = 22           # maximum object magnitude
min_alt = 20           # minimum object altitude
obs_start = ''         # aproximated time of the start of the observation in UT in format HHMM; if blank, it uses the earliest avaiable time
obs_interval = 5       # average time between observing two different objects in minutes
# minimal speed of the asteroid in "/min for it to be classified as fast in the script
min_speed = 10
open_script = True     # auto-opens script when main.py finishes
open_excluded = True   # auto-opens file with excluded asteroids when main.py finishes
# browser used for getting MPC data; 'Chrome', 'Firefox', 'Edge', 'Ie', 'Safari', 'Opera'
browser = 'Chrome'
