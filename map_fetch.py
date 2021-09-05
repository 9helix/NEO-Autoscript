from shared_var import *
import webbrowser

desig = input(
    'Input desired object and time in format "object_designation HHMM": ')

try:
    link = map_dict[desig]
    webbrowser.open(link)
except KeyError:
    print('Could not find desired object.')
