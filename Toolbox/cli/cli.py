import click
import warnings
from Toolbox.toolbox import timba_dashboard
import Toolbox.parameters.paths as toolbox_paths
warnings.simplefilter(action='ignore', category=FutureWarning)

@click.command()
# @click.option('-Y', '--year', default=default_year, 
#               show_default=True, required=True, type=int, 
#               help="Starting year.")

def cli():    
    td = timba_dashboard(num_files_to_read=4,
                         scenario_folder_path=toolbox_paths.SCINPUTPATH)
    td.run()

if __name__ == '__main__':
    cli()
