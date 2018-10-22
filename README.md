# Versatyle

Welcome to the Versatyle project

This project is part of "OpenGTB" project. The aim is to propose an open-source suitable software to manage your house equipements. 
Versatyle is a minimalist supervisor: it allows to make a graphical control/command.
Fully configurable by XML file, the GUI is designed for touchscreens.

I propose you a first example of its capabilities, with a configuration to manage an electric water-heater.

![Versatyle](https://raw.githubusercontent.com/lawrence-moy/Versatyle/master/PyQtWaterHeater/screenshot/capture1.png)

Versatyle requires some dependances to run:
- Python 3.x interpreter (Work well with a python 2.7 but I recommand you a 3.x for future).
- PySide (Python bindings for the Qt 4).

The Versatyle use HTTP procotol to communicate with low-level softwares. It uses GET HTTP commands
to get back values and POST HTTP commands with a JSON in body to send order requests.
