# NEO-Autoscript <img src='https://image.flaticon.com/icons/png/512/547/547436.png' width='30'/>

Collection of Python files for an automatized making of the scripts of the NEAs for the observations.  
&nbsp;

# Requirements <img src='https://image.flaticon.com/icons/png/512/4295/4295919.png' width='30'/>

**Python 3.6 or newer**

## Required Python modules

- **regex**

- **selenium**

## Other requirements

- **Refer to [this link](https://www.selenium.dev/documentation/getting_started/installing_browser_drivers/)**

- **Browser (Chrome, Firefox, Edge, Internet Explorer, Safari, Opera)**
- **Browser driver**
  &nbsp;  
  &nbsp;

# How-To-Use <img src='https://image.flaticon.com/icons/png/512/1321/1321639.png' width='30'/>

## Interactable files

- **main;** making an observation-ready script

- **script_fetch;** fetcing data from MPC site
- **config;** configuring program settings
- **map_fetch;** opening specific uncertainty map in the browser

## Instructions

In the `config.py` file you can configure the settings used in the program. Default values are already written.<br>
Next, `script_fetch.py` is used to access the MPC site using the browser and the `selenium` module. By running that file, it will open a separate browser window through which it will navigate to get the list of all the available asteroids. After it's done, the window will close.
While `main.py` can automatically run the `script_fetch.py` if it detects that the `shared_var.py` file is empty or if the date in it doesn't match the current date. Then the `main.py` will process the data that `script_fetch.py` has written and output it in the separate file.
Also, `map_fetch.py` is used to open in a browser an uncertainty map of a desired object at the desired time, as long as the desired object and time are written in the `unprocessed.txt`.
