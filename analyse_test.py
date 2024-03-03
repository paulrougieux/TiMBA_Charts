#Import packages
import pandas as pd
import numpy as np
from classes.import_data import package_directory, parameters
from classes.import_data import import_pkl_data
from classes.scenario_plots import sc_plot, PlotDropDown, interactiveModelComparison
from classes.model_analysis import validation
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#Identify the actual path of this jupyter file
PACKAGEDIR = package_directory()
print(PACKAGEDIR)

#Import data
import_pkl = import_pkl_data()
data = import_pkl.combined_data()
data_model_intercomparison = {}
data_model_intercomparison['Carbon'] = data['Carbon']
data_model_intercomparison['WorldPrices'] = data['WorldPrices']
data_model_intercomparison['Forest'] = data['Forest']
data_model_intercomparison['Data'] = data['data_periods']
data = data["data_periods"]
#print(import_pkl.validation(data=data))

#Plot predefined scenario results 
"""sc_plot = sc_plot()
sc_plot.predefined_plot(data)"""

#Interactive scenario results (quantities)
"""plot_dropdown_instance = PlotDropDown(data)"""

#Validation tables
validation = validation()
"""data_vali = validation.model_difference(data=data)
data_quantities = validation.model_corrcoef(data)"""

#Interactive scenario results (prices)

#Forest Plots

#Worldmap

#Heatmap

#Model intercomprison
country_data = validation.readin_country_data()
external_model_data = validation.readin_external_data()
data_filtered = validation.filter_data(data=data_model_intercomparison, country_data=country_data)

# reformate external_model_data
external_model_data = validation.reformate_external_data(data=external_model_data)

# align periods of gfpmpt data
period_data = validation.period_structure(data=data_model_intercomparison['Data'])
data_aligned = validation.align_period_data(data=data_filtered, period_data=period_data)

# convert units of gfpmpt 
data_aligned = validation.convert_unit(data=data_aligned)
data_aligned = validation.rename_parameter(data=data_aligned)

# merge data gfpmpt and external model data
data_fin = validation.merge_data(data=data_aligned, external_data=external_model_data)

# plot interactive model intercomparison
model_intercomparison = interactiveModelComparison(data=data_fin, plot_option="min_max")


