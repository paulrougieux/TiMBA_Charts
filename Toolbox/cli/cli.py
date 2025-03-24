import click
import warnings
from Toolbox.toolbox import timba_dashboard
warnings.simplefilter(action='ignore', category=FutureWarning)

@click.command()
# @click.option('-Y', '--year', default=default_year, 
#               show_default=True, required=True, type=int, 
#               help="Starting year.")

def cli():    
    td = timba_dashboard()
    td.run()

if __name__ == '__main__':
    cli()
