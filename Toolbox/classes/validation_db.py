import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import webbrowser
from threading import Timer
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import textwrap
import re

PACKAGEDIR = Path(__file__).parent.parent.absolute()


class Vali_DashboardPlotter:

    def __init__(self, data):
        self.data = data
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.start = self.data['Year'].min()
        self.end = self.data['Year'].max()
        self.model_colors = self.get_colors()
        self.logo = PACKAGEDIR / 'timba_validation_logo.png'
        self.create_layout()
        self.create_callbacks()

    def get_colors(self):
        color_palette = px.colors.qualitative.Bold
        model_colors = {
            "TiMBA": tuple(map(int, re.findall(r'\d+', color_palette[1]))),
            "GLOBIOM": tuple(map(int, re.findall(r'\d+', color_palette[4]))),
            "GFPM": tuple(map(int, re.findall(r'\d+', color_palette[3]))),
            "GTM": tuple(map(int, re.findall(r'\d+', color_palette[2]))),
            "Max": tuple(map(int, re.findall(r'\d+', color_palette[6]))),
            "Min": tuple(map(int, re.findall(r'\d+', color_palette[8]))),
        }

        return model_colors

    def create_layout(self):
        dropdown_style = {
            'height': '30px',
            'marginRight': '10px',
            'flex': '1 1 200px',  # Flex-Wachstum mit Basisgröße
            'minWidth': '200px'   # Mindestbreite für bessere Lesbarkeit
        }

        self.app.layout = dbc.Container(fluid=True, style={'backgroundColor': 'white'}, children=[

            # 1. filter options (bottom line)
            dbc.Row([
                dbc.Col([
                    dbc.Card(className="border-0 shadow-sm", children=[
                        dbc.CardBody(style={'padding': '15px'}, children=[
                            html.Div(style={
                                'display': 'flex',
                                'flexWrap': 'wrap',
                                'gap': '10px',
                                'alignItems': 'center'
                            }, children=[
                                # Logo links
                                html.Img(
                                    src=self.app.get_asset_url('timba_validation_logo.png'),
                                    style={'height': '50px', 'marginRight': '20px'}
                                ),

                                # Filter-Dropdowns
                                dcc.Dropdown(id='region-dropdown',
                                             options=[{'label': i, 'value': i}
                                                      for i in sorted(self.data['Region'].dropna().unique())],
                                             multi=True,
                                             placeholder="Select Region...",
                                             style=dropdown_style),
                                dcc.Dropdown(id='estimate-dropdown',
                                             options=[{'label': i, 'value': i}
                                                      for i in sorted(self.data['Estimate'].dropna().unique())],
                                             placeholder="Select Estimate...",
                                             multi=True,
                                             style=dropdown_style),
                                dcc.Dropdown(id='scenario-dropdown',
                                             options=[{'label': i, 'value': i}
                                                      for i in sorted(self.data['Scenario'].dropna().unique())],
                                             placeholder="Select Scenario...",
                                             multi=True,
                                             style=dropdown_style),
                                dcc.Dropdown(id='model-dropdown',
                                             options=[{'label': i, 'value': i}
                                                      for i in sorted(self.data['Model'].dropna().unique())],
                                             placeholder="Select Model...",
                                             multi=True,
                                             style=dropdown_style),
                                # Download-Button
                                html.Button(
                                    "⬇️ CSV Export",
                                    id="btn_csv",
                                    className="ml-auto",
                                    style={
                                        'height': '30px',
                                        'marginLeft': 'auto',
                                        'padding': '0 15px',
                                        'borderRadius': '4px',
                                        'border': '1px solid #ddd'
                                    }
                                )
                            ])
                        ])
                    ], style={'backgroundColor': '#f8f9fa'})
                ])
            ], className="mb-4"),  # Distance to bottom

            # 2. Main content
            dbc.Row([
                # Left column
                dbc.Col(children=[
                    dbc.Card(className="h-100 shadow-sm", children=[
                        dbc.CardBody(children=[
                            html.H5("Figure filter", className="card-title"),
                            dcc.Dropdown(
                                id='figure-type-dropdown',
                                options=[{'label': i, 'value': i}
                                                      for i in ['range', 'min_max', 'ssp_fsm_range', 'ssp_fsm_all']],
                                placeholder="Select Figure Type...",
                                style=dropdown_style
                            ),
                            dcc.Graph(
                                id='formip-plot',
                                config={'toImageButtonOptions': {'format': 'png'},
                                        'displayModeBar': True},
                                style={'height': '75vh'}
                            )
                        ])
                    ], style={'backgroundColor': 'white', 'padding': '15px'})
                ], width=8),

                # Secondary content
                dbc.Col(md=6, children=[
                    # Right column
                    dbc.Card(className="mb-3 shadow-sm", children=[
                        dbc.CardBody(style={'padding': '15px'}, children=[
                            dcc.Graph(
                                id='formip-plot-second',
                                style={'height': '35vh'}
                            )
                        ])
                    ]),

                    # Untere rechte Box
                    dbc.Card(className="mb-3 shadow-sm", children=[
                        dbc.CardBody(style={'padding': '15px'}, children=[
                            dcc.Graph(
                                id='formip-plot-third',
                                style={'height': '35vh'}
                            )
                        ])
                    ])
                ])
            ])
        ])

    def create_callbacks(self):
        @self.app.callback([
                Output('formip-plot', 'figure'),
                Output('formip-plot-second', 'figure'),
                Output('formip-plot-third', 'figure')],
            [
                Input('region-dropdown', 'value'),
                Input('estimate-dropdown', 'value'),
                Input('scenario-dropdown', 'value'),
                Input('model-dropdown', 'value'),
                Input('figure-type-dropdown', 'value')]
        )
        def update_plots(region, estimate, scenario, model, figure_type):
            return self.update_plot_validation(region, estimate, scenario, model, figure_type)

        @self.app.callback(
            Output("download-dataframe-csv", "data"),
            Input("btn_csv", "n_clicks"),
            [State('region-dropdown', 'value'),
             State('estimate-dropdown', 'value'),
             State('scenario-dropdown', 'value'),
             State('model-dropdown', 'value')],
            prevent_initial_call=True
        )
        def func(n_clicks, region, estimate, scenario, model):
            if n_clicks is None:
                raise dash.exceptions.PreventUpdate

            filtered_data = self.filter_data(region, estimate, scenario, model)
            return dcc.send_data_frame(filtered_data.to_csv, "filtered_data.csv")

    def filter_data(self, region, continent, domain, commodity, commodity_group, scenario):
        filtered_data = self.data
        if region and isinstance(region, list):
            filtered_data = filtered_data[filtered_data['ISO3'].isin(region)]
        if continent and isinstance(continent, list):
            filtered_data = filtered_data[filtered_data['Continent'].isin(continent)]
        if domain and isinstance(domain, list):
            filtered_data = filtered_data[filtered_data['domain'].isin(domain)]
        if commodity and isinstance(commodity, list):
            filtered_data = filtered_data[filtered_data['Commodity'].isin(commodity)]
        if commodity_group and isinstance(commodity_group, list):
            filtered_data = filtered_data[filtered_data['Commodity_Group'].isin(commodity_group)]
        if scenario and isinstance(scenario, list):
            filtered_data = filtered_data[filtered_data['Scenario'].isin(scenario)]
        filtered_data = self.remove_extreme_outliers(df=filtered_data, col='price')
        return filtered_data

    def update_plot_data(self, region, continent, domain, commodity, commodity_group, scenario):
        pass

    def generate_title(self, region, continent, domain, commodity, commodity_group):
        title_parts = []
        if region:
            title_parts.append(f"{region}")
        if continent:
            title_parts.append(f"{continent}")
        if domain:
            title_parts.append(f"{domain}")
        if commodity:
            title_parts.append(f"{commodity}")
        if commodity_group:
            title_parts.append(f"{commodity_group}")
        title = ", ".join(title_parts) if title_parts else "all data"
        clean_title = title.replace("'", "").replace("[", "").replace("]", "")
        return clean_title

    def create_world_map(self, region, continent, domain, commodity, commodity_group, scenario=None, year=None):
        pass

    def open_browser(self):
        webbrowser.open_new("http://localhost:8050")

    def run(self):
        Timer(1, self.open_browser).start()
        self.app.run(host='localhost', debug=False, dev_tools_ui=False, dev_tools_hot_reload=False, port=8050)
