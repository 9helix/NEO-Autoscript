# NEO-Autoscript <img src='https://image.flaticon.com/icons/png/512/547/547436.png' width='30'/>

Collection of Python files for an automatized making of the scripts of the NEAs for the observations.  
&nbsp;

# Requirements <img src='https://image.flaticon.com/icons/png/512/4295/4295919.png' width='30'/>

**Python 3.6 or newer**

## Required Python modules

- **regex**

- **selenium**

- **.NET Framework**

## Other requirements

- **Supported Browser;** (Chrome, Firefox, Edge, Internet Explorer, Safari, Opera)

- **Browser driver**
  &nbsp;  
  &nbsp;

# Getting Started <img src='https://image.flaticon.com/icons/png/512/1321/1321639.png' width='30'/>

## Interactable files

- **main.py;** making an observation-ready script

- **script_fetch.py;** fetcing data from MPC site
- **settings.exe;** configuring program settings
- **map_fetch.py;** opening specific uncertainty map in the browser

## Instructions

Firstly, you'll need a driver executable for you browser you wish to use placed in your PATH. You can download the needed driver [here](https://www.selenium.dev/documentation/getting_started/installing_browser_drivers/).

In the `settings.exe` file you can configure the settings used in the program. Default values are already written. If the file doesn't run,there's a posibility that error occured. If so, contact me and send me the .exe file and `src` folder zipped.<br>
Next, `script_fetch.py` is used to access the MPC site using the browser and the `selenium` module. By running that file, it will open a separate browser window through which it will navigate to get the list of all the available asteroids. After it's done, the window will close and the data will be written in file `{date}-raw.txt`.<br>
While `main.py` can automatically run the `script_fetch.py` if it detects that the `shared_var.py` file is empty or if the date in it doesn't match the current date. Then the `main.py` will process the data that `script_fetch.py` has written and output it in two files: `{date}-log.txt` (contains the asteroids for the script) and `{date}-excluded.txt` (contains the rast of the asteroids that didn't fit in the script). Also it will write all the asteroids sorted from the one that shows up earliest on the sky to the one that shows up latest to a file `{date}-time-sorted.txt`.<br>
Also, `map_fetch.py` is used to open in a browser an uncertainty map of a desired object at the desired time, as long as the desired object and time are written in the `{date}-raw.txt`.<br><br>

# Contact <img src='https://image.flaticon.com/icons/png/512/3062/3062634.png' width='30'/>

If you have any questions, issues or possible improvement suggestions about this project, feel free to contact me.

Dino Gržinić - grzinicdino@gmail.com - [@dinogrzinic](https://www.instagram.com/dinogrzinic/) - Helix#3958
