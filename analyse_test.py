import pandas as pd
import numpy as np
from classes.import_data import package_directory, parameters
from classes.import_data import import_pkl_data
from classes.scenario_plots import sc_plot, PlotDropDown, HeatmapDropDown, InteractivePrice, interactiveModelComparison
from classes.model_analysis import validation
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

PACKAGEDIR = package_directory()
print(PACKAGEDIR)

import_pkl = import_pkl_data()
data = import_pkl.combined_data()
data_model_intercomparison = {}
try:
    data_model_intercomparison['Carbon'] = data['Carbon']
    data_model_intercomparison['WorldPrices'] = data['WorldPrices']
    data_model_intercomparison['Forest'] = data['Forest']
    data_model_intercomparison['Data'] = data['data_periods']
except KeyError:
    pass
#data = data["data_periods"]

import_pkl = import_pkl_data()
data = import_pkl.combined_data()
forest_data = data['Forest']
country_data = import_pkl.read_country_data()
forest_data_world = import_pkl.read_forest_data_gfpm(country_data=country_data)
forest_data = forest_data[forest_data_world.columns]
forest_data = pd.concat([forest_data, forest_data_world], axis= 0)


import matplotlib.pyplot as plt
class ForestData:
    def __init__(self, data):
        self.data = forest_data


    def drop_duplicates(self):
        self.data = self.data.drop_duplicates().reset_index(drop=True)



    def plot_stock_area_diagrams(self):
        scenarios = self.data['Scenario'].unique()
        total_periods = self.data['Period'].unique()


        plt.figure(figsize=(12, 6))
        bar_width = 0.05
        bar_gap = -0.42
        for i, scenario in enumerate(scenarios):
            scenario_name = self.data[self.data['Scenario'] == scenario]
            total_stock = scenario_name.groupby('Period')['ForStock'].sum()


            
            periods_runner = total_stock.index.intersection(total_periods)
            bar_positions = np.arange(len(periods_runner)) + i * (len(periods_runner) * bar_width + bar_gap)
            plt.bar(bar_positions, total_stock[periods_runner], label=f'{scenario} (ForStock)', width=bar_width, align='edge')


        #plt.ylim(ymin=3e6)
        plt.xlabel('Period')
        plt.ylabel('Sum of ForStock')
        plt.legend()
        plt.title('ForStock')
        plt.show()


        plt.figure(figsize=(12, 6))
        for i, scenario in enumerate(scenarios):
            scenario_name = self.data[self.data['Scenario'] == scenario]
            total_area = scenario_name.groupby('Period')['ForArea'].sum()


         
            periods_runner = total_area.index.intersection(total_periods)
            bar_positions = np.arange(len(periods_runner)) + i * (len(periods_runner) * bar_width + bar_gap)
            plt.bar(bar_positions, total_area[periods_runner], label=f'{scenario} (ForArea)', width=bar_width)


        #plt.ylim(ymin=3e7)
        plt.xlabel('Period')
        plt.ylabel('Sum of ForArea')
        plt.legend(loc = 'lower right')
        plt.title('ForArea')
        plt.show()



data_container = data
forest_plot = ForestData(data_container)
forest_plot.drop_duplicates()
forest_plot.plot_stock_area_diagrams()
