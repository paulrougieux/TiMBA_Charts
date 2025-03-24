import pickle
import gzip
import os
from pathlib import Path
from dataclasses import dataclass
import pandas as pd

PACKAGEDIR = Path(__file__).parent.absolute()

@dataclass
class Parameters:
    input_folder_sc: str = "\\Input"
    input_folder: str = "\\Input"
    seperator_scenario_name: str = "Sc_"
    column_name_scenario: str = "Scenario"
    column_name_model: str = "Model"
    column_name_id: str = "ID"
    model_name: str = "GFPMpt"
    csv_input: str = "FAO_Data.csv"
    csv_input_forest: str = 'Input\\Additional_Information\\Forest_world500.csv'

params = Parameters()

class import_pkl_data:
    def __init__(self, inputfolder:str='\\Input'):
        self.inputfolder = inputfolder

    @staticmethod
    def open_pickle(src_filepath: str):
        open_func = gzip.open if src_filepath.endswith('.gz') else open
        with open_func(src_filepath, "rb") as f:
            return pickle.load(f)

    def read_country_data(self):
        country_data = pd.read_csv(PACKAGEDIR / params.input_folder / "Additional_Information/country_info.csv", encoding="ISO-8859-1")
        country_data = country_data[["Country-Code", "ContinentNew", "Country"]]
        country_data.columns = ["RegionCode","Continent", "Country"]
        country_data.Country = country_data.Country.astype("category")
        country_data.Continent = country_data.Continent.astype("category")
        return country_data
    
    def downcasting(self, data: pd.DataFrame):
        type_dict = {
            'category': ['RegionCode', 'CommodityCode', 'domain', 'Scenario', 'Model', 'ID'],
            'float32': ['price', 'quantity', 'elasticity_price', 'slope', 'intercept', 'shadow_price', 'lower_bound', 'upper_bound'],
            'int16': ['Period', 'year']
        }
        for dtype, columns in type_dict.items():
            for col in columns:
                if col in data.columns:
                    data[col] = data[col].astype(dtype)
        return data

    def concat_scenarios(self, data: dict, sc_name:str, data_prev: dict, ID: int):
        for key in data:
            data[key][params.column_name_scenario] = sc_name
            data[key][params.column_name_model] = params.model_name
            data[key][params.column_name_id] = ID
            if data_prev:
                data[key] = pd.concat([data_prev[key], data[key]], axis=0)
                
    def combined_data(self):
        file_list = [f for f in os.listdir(PACKAGEDIR / self.inputfolder) if f.endswith('.pkl') or f.endswith('.gz')]
        data_list = []
        for ID, scenario_file in enumerate(file_list, start=1):
            src_filepath = PACKAGEDIR / self.inputfolder / scenario_file
            scenario_name = scenario_file[scenario_file.rfind(params.seperator_scenario_name)+3:-4]
            try:
                data = self.open_pickle(src_filepath)
                for key in data:
                    data[key][params.column_name_scenario] = scenario_name
                    data[key][params.column_name_model] = params.model_name
                    data[key][params.column_name_id] = ID
                data_list.append(data)
            except (gzip.BadGzipFile, pickle.UnpicklingError, PermissionError, ValueError):
                continue

        combined_data = {key: pd.concat([d[key] for d in data_list if key in d], axis=0) for key in data_list[0]}
        combined_data["data_periods"] = self.downcasting(combined_data["data_periods"])

        try:
            csv_data = pd.read_csv(PACKAGEDIR / self.inputfolder / params.csv_input)
            csv_data = self.downcasting(csv_data)
        except FileNotFoundError:
            csv_data = pd.DataFrame()

        country_data = self.read_country_data()
        forest_data = self.read_forest_data_gfpm(country_data)
        
        combined_data["data_periods"] = pd.merge(combined_data["data_periods"], country_data, on="RegionCode", how="left")
        data_results = pd.concat([combined_data["data_periods"], csv_data], axis=0)
        combined_data["data_periods"] = data_results

        return combined_data

    def read_forest_data_gfpm(self, country_data:pd.DataFrame):
        for_data_gfpm = pd.read_csv(PACKAGEDIR / params.csv_input_forest, encoding="ISO-8859-1")
        
        rearranged_for_data = pd.melt(for_data_gfpm, id_vars=['domain','Country'], var_name='Year', value_name='for')
        rearranged_for_data = rearranged_for_data.dropna()
        rearranged_for_data['Year'] = rearranged_for_data['Year'].astype(int)

        foreststock = pd.Series(dtype=float)
        for domain in rearranged_for_data.domain.unique():
            rearranged_for_data_domain = rearranged_for_data[rearranged_for_data['domain'] == domain].reset_index(drop=True)
            if domain == 'ForArea':
                rearranged_for_data_domain['ForStock'] = foreststock
            else: 
                foreststock = rearranged_for_data_domain['for']

        forest_data = rearranged_for_data_domain[['Country', 'Year', 'for', 'ForStock']]
        forest_data.columns = ['Country', 'Year', 'ForArea', 'ForStock']
        forest_data = pd.merge(forest_data, country_data, on='Country')

        period_mapping = {2017: 0, 2020: 1, 2025: 2, 2030: 3, 2035: 4, 2040: 5, 2045: 6, 2050: 7, 2055: 8, 2060: 9, 2065: 10}
        forest_data['Period'] = forest_data['Year'].map(period_mapping)

        forest_gfpm = forest_data[['RegionCode', 'Period', 'ForStock', 'ForArea']]
        forest_gfpm[params.column_name_scenario] = 'world500'
        forest_data['Model'] = 'GFPM'
        return forest_gfpm

if __name__ == "__main__":
    importer = import_pkl_data()
    result = importer.combined_data()
    print(result)