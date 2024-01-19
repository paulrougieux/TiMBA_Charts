import pandas as pd
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt

class parameters(Enum):
    pass

class validation():
    def init(self):
        pass

    def model_difference(self, data: pd.DataFrame):
        data_gfpm = data[data.ID==0].reset_index(drop=True)
        data_gfpm = data_gfpm[['RegionCode','domain',"CommodityCode","quantity"]]
        for i in data.ID.unique():
            sc_name = list(data.Scenario[data.ID==i])[0]
            data_gfpmpt = data[data.ID==i].reset_index(drop=True)
            data_gfpm[sc_name] = data_gfpm.quantity - data_gfpmpt.quantity
        return data_gfpm
    
    def model_corrcoef(self, data: pd.DataFrame, unit: str = 'quantity'):
        data_gfpm = data[data.ID==0].reset_index(drop=True)
        column_list = ['Continent','domain','CommodityCode','year']
        data_gfpm = data_gfpm[column_list + [unit]]
        cor_df = pd.DataFrame()
        for column in column_list:
            corr_full = pd.DataFrame()
            for i in data.ID.unique():
                sc_name = list(data.Scenario[data.ID==i])[0]
                data_gfpmpt = data[data.ID==i].reset_index(drop=True)
                data_gfpm[sc_name] = data_gfpmpt.quantity
                correlations = data_gfpm.groupby(column)[[unit,sc_name]].corr().iloc[0::2,-1].reset_index()
                corr_full = pd.concat([corr_full,correlations[sc_name]], axis=1)
            correlations.rename(columns={column: "ID"}, inplace=True)
            correlations = pd.concat([correlations["ID"], corr_full], axis=1)
            correlations["column"] = column
            cor_df = pd.concat([cor_df,correlations],axis=0)

        color_palette=['royalblue', 'peru', 'forestgreen', 
               'orangered', 'darkviolet', 'darkcyan', 
               'brown', 'pink', 'olive', 'grey']
        width = 0.5  # the width of the bars
        data_barplot = cor_df[cor_df.column == "domain"]
        
        num_sc = len(data_barplot.ID)
        name_df = pd.DataFrame()
        cor_df = data_barplot[data_barplot.columns[1:-2]]
        for i in range(0,num_sc):
            title_name = data_barplot[data_barplot.columns[0:1]].iloc[i:i+1]
            name_df = pd.concat([name_df,title_name])
        
        fig, axes =  plt.subplots(5, 1, sharex=False, sharey= False, figsize=(3,9)) 
        for i in range(0,num_sc):
            value = pd.DataFrame(cor_df.iloc[i])
            mean_val = value.mean()
            diff_val = value - mean_val
            ylim_max = diff_val.max().values * 1.05
            ylim_min = diff_val.min().values * 0.95
            diff_val.plot.bar(grid=True, color=color_palette[i], width=0.9, ax=axes[i])
            axes[i].title.set_text(str(name_df.iloc[i].values))
            axes[i].get_legend().remove()
            axes[i].set_ylim([ylim_min,ylim_max])
            if i < 4:
                axes[i].get_xaxis().set_visible(False)
        
        fig.tight_layout(pad=1.0)
        plt.show()


            # courses = data_plot.columns
            # values = data_plot.iloc[i].values
            # fig = plt.figure(figsize = (10, 5))
            # values.plt.bar(courses,axs = axs[i])#, color='royalblue',
                          #color_paette, 
                          #width = width)
            # axs[i].plt.xticks(rotation=30, ha='right') 
            # axs[i].plt.ylim([min(values)*0.995, max(values)*1.005])   
            # axs[i].plt.xlabel("")
            # axs[i].plt.ylabel("")
            # axs[i].plt.title(title_name.values[0][0])
            # plt.show()
        return cor_df
    
    def validation(self, data: pd.DataFrame):
        data_vali = data[data.ID==0].reset_index(drop=True)
        data_std_prev = []
        for i in data.ID.unique():
            print(data.Scenario[data.ID == i][0])
            sc_name = data.Scenario[data.ID == i][0]
            data_gfpm = data_vali
            data_gfpmpt = data[data.ID==i].reset_index(drop=True)
            data_gfpm["vali"] = data_gfpm.quantity - data_gfpmpt.quantity
            data_std = pd.DataFrame(data_gfpm.groupby(['RegionCode','domain',"CommodityCode"])["vali"].std()).reset_index()
            data_std.columns = ["Region", "Domain","Commodity",sc_name]
            data_std_index = data_std[["Region", "Domain","Commodity"]]
            data_std_prev = pd.concat([pd.DataFrame(data_std_prev),pd.DataFrame(data_std[sc_name])], axis=1)
        data_std = pd.concat([data_std_index, data_std_prev], axis=1)
        fourth_quantile = data_std[data_std.columns[3]].quantile([.75])
        data_std = data_std.sort_values(by=data_std.columns[3], ascending=False)
        #data_std_count = pd.DataFrame(data_std.groupby(['Region','Domain']).count()).reset_index()
        return data_std