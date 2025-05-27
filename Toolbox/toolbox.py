from Toolbox.classes.import_data import import_pkl_data
from Toolbox.classes.dashboard import DashboardPlotter
from pathlib import Path
import Toolbox.parameters.paths as toolbox_paths

class timba_dashboard:
    def __init__(self,scenario_folder_path:Path,
                 additional_info_folderpath:Path,
                 num_files_to_read:int=10):
        self.num_files_to_read = num_files_to_read
        self.scenario_folder_path = scenario_folder_path
        self.additional_info_folderpath = additional_info_folderpath

    def import_data(self):
        import warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)
        import_pkl = import_pkl_data(num_files_to_read=self.num_files_to_read,
                                     SCENARIOPATH=self.scenario_folder_path,
                                     ADDINFOPATH=self.additional_info_folderpath)
        self.data = import_pkl.combined_data()

    def call_dashboard(self):
        DashboardPlotter(data=self.data["data_periods"]).run()

    def run(self):
        self.import_data()
        self.call_dashboard() 

if __name__ == "__main__":
    td = timba_dashboard(num_files_to_read=4,
                         scenario_folder_path=toolbox_paths.SCINPUTPATH)
    td.run()

