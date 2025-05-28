![TiMBA Logo](https://raw.githubusercontent.com/TI-Forest-Sector-Modelling/TiMBA/main/timba_logo_v3.png)

# TiMBA ToolBox

[![Build Status](https://github.com/TI-Forest-Sector-Modelling/Analyses_Toolbox_TiMBA_workshop/actions/workflows/actions.yml/badge.svg)](https://github.com/TI-Forest-Sector-Modelling/Analyses_Toolbox_TiMBA_workshop/actions/workflows/actions.yml)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

This package can be used as a toolbox for analysing **TiMBA** results after simulation. TiMBA is a partial economic equilibrium model for the global forest product market. The toolbox provides a dashboard which let the user interact with the main TiMBA results. This includes the development of prices, production, consumption, and trade of forest products as well as forest stock development. It also gives information about historic developments as reported by the FAOSTAT.

## Install the Toolbox

The package is developed and tested with Python 3.12.6 on Windows. Please ensure that Python is installed on your system. It can be downloaded and installed
from [Python.org](https://www.python.org/downloads/release/python-3126/).

1. Clone the repository
Begin by cloning the repository to your local machine using the following command: 
    >git clone https://github.com/TI-Forest-Sector-Modelling/Analyses_Toolbox_TiMBA_workshop
   > 
2. Switch to the TiMBA directory  
Navigate into the TiMBA project folder on your local machine.
   >cd Toolbox
   >
3. Create a virtual environment  
It is recommended to set up a virtual environment for TiMBA to manage dependencies. If you are using only a single version of Python on your computer:
   >python -m venv .venv
   >
1. Activate the virtual environment  
Enable the virtual environment to isolate TiMBA dependencies. 
   >.venv\Scripts\activate
   >
1. Install TiMBA in the editable mode  
   >pip install -e .

If the following error occurs: "ERROR: File "setup.py" or "setup.cfg" not found."
you might need to update the pip version you use with: 
>python.exe -m pip install --upgrade pip

## Start the dashbord
After installing the package the user could simply start the dashboard board typing the following CLI command:
> show_dashboard

To show all possible options that could be changed with the CLI the user could type:
> show_dashboard --help

At the moment there are two options that coud be changed. The specification of the number of most recent .pkl files to read and 
the definition of the folder path where the scenario results are stored.

The first option, about the number of scenarios, can be changed by:
> show_dashboard -NF=4

To change the folder path the user can type, e.g.:
> show_dashboard -FP='E:\P_TiMBA\TiMBA\data\output'
