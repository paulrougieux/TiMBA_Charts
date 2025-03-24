![TiMBA Logo](/Toolbox/classes/assets/timba_dashboard_logo.png)  

# Analyses_Toolbox_TiMBA

This package can be used as a toolbox for analysing **TiMBA** results. TiMBA is a partial economic equilibrium model for the global forest products market. The toolbox generates a dashboard which let the user interact with some of the main TiMBA results, like development in prices, production, consumption, trade and forests. It also provides information about historic developments which are covered by the FAO.

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
