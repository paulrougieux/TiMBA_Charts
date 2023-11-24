import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display,clear_output

class sc_plot():
    def init(self):
        pass

    def predefined_plot(self, data: pd.DataFrame):
        grouped_data = data.groupby(['Period', 'Scenario']).sum().reset_index()
        plt.figure(figsize=(12, 8))

        for price_value in grouped_data['Scenario'].unique():
            subset = grouped_data[grouped_data['Scenario'] == price_value]
            plt.plot(subset['Period'], subset['quantity'], label=f'Scenario {price_value}')

        plt.title('Quantity for each country grouped by Period')
        plt.xlabel('period')
        plt.ylabel('Quantity')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def drop_down(self, data: pd.DataFrame):
        #drop down
        region_dropdown = widgets.Dropdown(
            options=['Alle'] + list(data['RegionCode'].unique()),
            value='Alle',
            description='Select RegionCode:',
            disabled=False,
        )

        model_dropdown = widgets.Dropdown(
            options=['Alle'] + list(data['Model'].unique()),
            value='Alle',
            description='Select Model:',
            disabled=False,
        )

        id_dropdown = widgets.Dropdown(
            options=['Alle'] + list(data['ID'].unique()),
            value='Alle',
            description='Select ID:',
            disabled=False,
        )

        domain_dropdown = widgets.Dropdown(
            options=['Alle'] + list(data['domain'].unique()),
            value='Alle',
            description='Select Domain:',
            disabled=False,
        )

        commodity_code_dropdown = widgets.Dropdown(
            options=['Alle'] + list(data['CommodityCode'].unique()),
            value='Alle',
            description='Select CommodityCode:',
            disabled=False,
        )
        return region_dropdown, model_dropdown, id_dropdown, domain_dropdown, commodity_code_dropdown
    
    '''The next passages did not work until now    
    def update_plot_data(self, data, region_code, model, id_value, domain, commodity_code):
        region_code_filter = [region_code] if region_code != 'Alle' else data['RegionCode'].unique()
        model_filter = [model] if model != 'Alle' else data['Model'].unique()
        id_filter = [id_value] if id_value != 'Alle' else data['ID'].unique()
        domain_filter = [domain] if domain != 'Alle' else data['domain'].unique()
        commodity_code_filter = [commodity_code] if commodity_code != 'Alle' else data['CommodityCode'].unique()

        filtered_data = data[
            (data['RegionCode'].isin(region_code_filter)) &
            (data['Model'].isin(model_filter)) &
            (data['ID'].isin(id_filter)) &
            (data['domain'].isin(domain_filter)) &
            (data['CommodityCode'].isin(commodity_code_filter))
        ]
        
        grouped_data = filtered_data.groupby(['Period', 'Scenario']).sum().reset_index()

        plt.figure(figsize=(12, 8))

        for price_value in grouped_data['Scenario'].unique():
            subset = grouped_data[grouped_data['Scenario'] == price_value]
            plt.plot(subset['Period'], subset['quantity'], label=f'M: {price_value}')

        plt.title(f'quantity for each Period - RegionCode: {region_code}, Model: {model}, ID: {id_value}, Domain: {domain}, CommodityCode: {commodity_code}')
        plt.xlabel('period')
        plt.ylabel('quantity')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def interactive_plot(self, data: pd.DataFrame):
        region_dropdown, model_dropdown, id_dropdown, domain_dropdown, commodity_code_dropdown = self.drop_down(data=data)
        interactive_plot_update = widgets.interactive(self.update_plot_data,
                                                      region_code=region_dropdown,
                                                      model=model_dropdown,
                                                      id_value=id_dropdown,
                                                      domain=domain_dropdown,
                                                      commodity_code=commodity_code_dropdown)
        display(interactive_plot_update)
    '''