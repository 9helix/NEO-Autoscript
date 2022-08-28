[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
![GitHub release (latest by date)](https://img.shields.io/github/v/tag/9helix/NEO-Autoscript?color=gren&label=Release)
![GitHub repo size](https://img.shields.io/github/repo-size/9helix/NEO-Autoscript?label=Size)
![GitHub license](https://img.shields.io/github/license/9helix/NEO-Autoscript)


# NEO-Autoscript <img src='https://image.flaticon.com/icons/png/512/547/547436.png' width='30'/>

Collection of Python files for an automatized making of the scripts of the NEAs for the observations.  
&nbsp;

# Requirements <img src='https://cdn-icons-png.flaticon.com/512/4295/4295919.png' width='30'/>

**Python 3.6 or newer**

Optional - **.NET Framework**

# Getting Started <img src='https://image.flaticon.com/icons/png/512/1321/1321639.png' width='30'/>

## Interactable files

- **settings.exe;** configuring program settings and running other files
- **main<span>.</span>py;** making an observation-ready script
- **script_fetch.py;** fetcing data from MPC site

- **map_fetch.py;** opening specific uncertainty map in the browser

## Instructions

In the `settings.exe` file you can configure the settings used in the program. Default values are already written. You can also edit `config.py` manually. It is in `src` folder, but don't edit/delete `config_backup.py` since it contains the default settings.<br>
`script_fetch.py` is used to access the data on the MPC site. After it's done, the data will be written in the `{date}-raw.txt`.<br>
`main.py` can automatically run the `script_fetch.py` if it detects that the `shared_var.py` file is empty or if the date in it doesn't match the current date. Then the `main.py` will process the data that `script_fetch.py` has written and output it into two files: `{date}-log.txt` (contains the asteroids for the script) and `{date}-excluded.txt` (contains the rest of the asteroids that didn't fit in the script). Also it will write all the asteroids sorted from the one that shows up earliest on the sky to the one that shows up latest to a file `{date}-time-sorted.txt`.<br>
Also, `map_fetch.py` is used to open in a browser an uncertainty map of a desired object at the desired time, as long as the desired object and time are written in the `{date}-raw.txt`.<br>
There will also be created `neocp.html` if you want to view the full list of asteroids with all their map links.<br>
You can find all outputed files in the `output` folder, they are their furtherly sorted in subfolders by date.

# Contact <img src='https://image.flaticon.com/icons/png/512/3062/3062634.png' width='30'/>

If you have any questions, issues or possible improvement suggestions about this project, feel free to contact me.

Dino Gržinić - grzinicdino@gmail.com - [@dinogrzinic](https://www.instagram.com/dinogrzinic/) - Helix#3958
