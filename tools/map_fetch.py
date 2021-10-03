import pickle
import webbrowser

desig = input(
    'Input desired object and time in format "object_designation HHMM": ')
try:
    with open('output/NEO_data.pkl', 'rb') as f:
        data = pickle.load(f)
    map_dict = data['map_dict'][desig]

    link = map_dict[desig]
    webbrowser.open(link)
except KeyError:
    print('Could not find desired object.')
input("\nPress ENTER to close...")
