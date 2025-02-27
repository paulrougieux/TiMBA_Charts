#Import packages
import pandas as pd
import numpy as np
from classes.import_data import import_pkl_data
from classes.dashboard import DashboardPlotter
import warnings
#warnings.simplefilter(action='ignore', category=FutureWarning)

#Import data
import_pkl = import_pkl_data()
data = import_pkl.combined_data()

# Usage
plotter = DashboardPlotter(data=data["data_periods"])
plotter.run()


