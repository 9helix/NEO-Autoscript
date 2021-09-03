from shared_var import *
import webbrowser

desig = input(
    'Input desired object and time in format "object_designation HHMM": ')

link = map_dict[desig]
webbrowser.open(link)
