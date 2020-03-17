# LSL sample scripts launcher
LSL example scripts launcher GUI for Python
## Installation
* Prerequisites
  * Python > 3
  * [PyQt5](https://pypi.org/project/PyQt5/): Python bindings for the Qt application toolkit
  * [Qtpy](https://pypi.org/project/QtPy/): Abstraction layer on top of the Qt bindings.
  * [`pylsl`](https://labstreaminglayer.readthedocs.io/dev/app_dev.html#python-apps): Python interface to the Lab Streaming Layer (LSL).
* Directory must be in the `Apps` directory and must be named `PythonScripts`
## Usage
* Start the `python_scripts.py` script. A graphical user interface will load. 
* Select the desired script to run.
* A new command window will appear with the script running in it.
## Changing the pylsl directory
* If the pylsl directory is different from the traditional directory structure, the pylsl directory can be modified by editing the `config.json` file.

###### 
