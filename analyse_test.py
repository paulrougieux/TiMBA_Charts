#Import packages
import pandas as pd
import numpy as np
from classes.import_data import package_directory, parameters
from classes.import_data import import_pkl_data
from classes.scenario_plots import sc_plot, PlotDropDown
from classes.model_analysis import validation
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#Identify the actual path of this jupyter file
PACKAGEDIR = package_directory()
print(PACKAGEDIR)

#Import data
import_pkl = import_pkl_data()
data = import_pkl.combined_data()
#data = data["data_periods"]
data = data['Forest']
# data.ForStock = data.ForStock.astype("float32")
# data.ForArea = data.ForArea.astype("float32")
# data = data.drop_duplicates().reset_index(drop=True)
# data = data[['Scenario','Model','ID','RegionCode','Period','ForStock','ForArea']]
# #data = pd.pivot_table(data, values='ForStock', index=['RegionCode'],columns=['Period'], aggfunc="mean")
print(data)
#data.to_csv('ForstockData.csv')

# #Predefined plot
# sc_plot = sc_plot()
# sc_plot.predefined_plot(data)

# #Interactive plot
# plot_dropdown_instance = PlotDropDown(data)

#validation = validation()
#data_vali = validation.model_difference(data=data)

#data_quantities = validation.model_corrcoef(data=data, unit='quantity')