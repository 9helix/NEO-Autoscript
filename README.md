# NEO-Autoscript <img src='https://image.flaticon.com/icons/png/512/547/547436.png' width='30'/>

Collection of Python files for an automatized making of the scripts of the NEAs for the observations.  
&nbsp;

# Requirements <img src='https://image.flaticon.com/icons/png/512/4295/4295919.png' width='30'/>

**Python 3.6 or newer**

## Required Python modules

- **regex**

- **selenium**

## Other requirements

- **Chrome browser**

- **Chrome driver**
  &nbsp;  
  &nbsp;

# Getting Started <img src='https://image.flaticon.com/icons/png/512/1321/1321639.png' width='30'/>

## Interactable files

- **main;** making an observation-ready script

- **script_fetch;** fetcing data from MPC site
- **config;** configuring program settings
- **map_fetch;** opening specific uncertainty map in the browser

## Instructions

Firstly, you'll need a Chrome driver executable placed in your PATH, I've already put the driver for the Chrome 93 version in the `browser_driver` folder, but you can download any other at [this link](https://sites.google.com/a/chromium.org/chromedriver/downloads).

In the `config.py` file you can configure the settings used in the program. Default values are already written.<br>
Next, `script_fetch.py` is used to access the MPC site using the browser and the `selenium` module. By running that file, it will open a separate browser window through which it will navigate to get the list of all the available asteroids. After it's done, the window will close.<br>
While `main.py` can automatically run the `script_fetch.py` if it detects that the `shared_var.py` file is empty or if the date in it doesn't match the current date. Then the `main.py` will process the data that `script_fetch.py` has written and output it in the separate file.<br>
Also, `map_fetch.py` is used to open in a browser an uncertainty map of a desired object at the desired time, as long as the desired object and time are written in the `unprocessed.txt`.<br><br>

# Contact <img src='https://image.flaticon.com/icons/png/512/3062/3062634.png' width='30'/>

If you have any questions, issues or possible improvement suggestions about this project, feel free to contact me.

Dino Gržinić - grzinicdino@gmail.com - [@dinogrzinic](https://www.instagram.com/dinogrzinic/) - Helix#3958
