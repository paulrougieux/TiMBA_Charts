import click
import warnings
from Toolbox.toolbox import timba_dashboard, bilateral_trade_dashboard,validation_dashboard
import Toolbox.parameters.paths as toolbox_paths
from pathlib import Path
warnings.simplefilter(action='ignore', category=FutureWarning)

@click.group()
def cli():
    pass

#Dashboard Command
@click.command()
@click.option('-NF', '--num_files', default=10, 
              show_default=True, required=True, type=int, 
              help="Number of .pkl files to read")
@click.option('-FP', '--sc_folderpath', default=toolbox_paths.SCINPUTPATH, 
              show_default=True, required=True, type=Path, 
              help="Folder path for scenarios")
def dashboard_cli(num_files, sc_folderpath):    
    click.echo("Begin to show default dashboard")
    td = timba_dashboard(
        num_files_to_read=num_files,
        scenario_folder_path=sc_folderpath
    )
    td.run()

#Validation Command
@click.command()
@click.option('-NF', '--num_files', default=10, 
              show_default=True, required=True, type=int, 
              help="Number of .pkl files to read")
@click.option('-FP', '--sc_folderpath', default=toolbox_paths.SCINPUTPATH, 
              show_default=True, required=True, type=Path, 
              help="Folder path for scenarios")
def validation_cli(num_files, sc_folderpath):    
    click.echo("Validation is started")
    validb = validation_dashboard(
        num_files_to_read=num_files,
        scenario_folder_path=sc_folderpath
    )
    validb.run()

cli.add_command(dashboard_cli, name="dashboard")
cli.add_command(validation_cli, name="validation")

