import click
import warnings
from Toolbox.toolbox import timba_dashboard
import Toolbox.parameters.paths as toolbox_paths
from pathlib import Path
warnings.simplefilter(action='ignore', category=FutureWarning)

@click.command()
@click.option('-NF', '--num_files', default=10, 
              show_default=True, required=True, type=int, 
              help="Specify the number of most recent .pkl files to read. Limits output to prevent overcrowding.")
@click.option('-FP', '--sc_folderpath', default=toolbox_paths.SCINPUTPATH, 
              show_default=True, required=True, type=Path, 
              help="Define the folder where the code will look for .pkl files containing the scenarios.")
@click.option('-AIFP', '--additional_info_folderpath', default=toolbox_paths.AIINPUTPATH, 
              show_default=True, required=True, type=Path, 
              help="Define the folder where the code will look for additional infos, like historic data or country information.")

def cli(num_files,sc_folderpath,additional_info_folderpath):    
    td = timba_dashboard(num_files_to_read=num_files,
                         scenario_folder_path=sc_folderpath,
                         additional_info_folderpath=additional_info_folderpath)
    td.run()

if __name__ == '__main__':
    cli()
