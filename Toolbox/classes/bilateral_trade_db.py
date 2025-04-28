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

PACKAGEDIR = Path(__file__).parent.parent.absolute()

class BT_DashboardPlotter:

    def __init__(self, data):
        self.data = data
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.start = self.data['year'].min()
        self.end = self.data['year'].max()
        self.color_list = [
            '#2A4D69',  # Dunkelblau
            '#4B8BBE',  # Hellblau
            '#D35400',  # Dunkelorange
            '#AAB7B8',  # Grau
            '#9B59B6',  # Lila
            '#2980B9',  # Blau
            '#27AE60',  # Grün
            '#6C757D',  # Dunkelgrau
            '#F1C40F',  # Senfgelb
            '#E67E22',  # Orange  
        ]
        self.logo = PACKAGEDIR/'timba_trade_dashboard_logo.png'
        self.create_layout()
        self.create_callbacks()

    def create_layout(self):
        dropdown_style = {
            'height': '30px',
            'marginRight': '10px',
            'flex': '1 1 200px',
            'minWidth': '200px'
        }

        self.app.layout = dbc.Container(
            fluid=True,
            style={'backgroundColor': 'white', 'padding': '15px'},
            children=[
                # 1. Filterzeile (volle Breite oben)
                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            className="border-0 shadow-sm",
                            style={'backgroundColor': '#f8f9fa'},
                            children=[
                                dbc.CardBody(
                                    style={'padding': '15px'},
                                    children=[
                                        html.Div(
                                            style={
                                                'display': 'flex',
                                                'flexWrap': 'wrap',
                                                'gap': '10px',
                                                'alignItems': 'center'
                                            },
                                            children=[
                                                # Logo
                                                html.Img(
                                                    src=self.app.get_asset_url('timba_trade_dashboard_logo.png'),
                                                    style={'height': '50px', 'marginRight': '20px'}
                                                ),
                                                
                                                # Filter-Dropdowns
                                dcc.Dropdown(id='region-dropdown',
                                             options=[{'label': i, 'value': i}
                                                      for i in sorted(self.data['ISO3'].dropna().unique())],
                                             multi=True,
                                             placeholder="Select Country...",
                                             style=dropdown_style),
                                dcc.Dropdown(id='continent-dropdown',
                                             options=[{'label': i, 'value': i}
                                                      for i in sorted(self.data['Continent'].dropna().unique())],
                                             placeholder="Select Continent...",
                                             multi=True,
                                             style=dropdown_style),
                                dcc.Dropdown(id='domain-dropdown',
                                             options=[{'label': i, 'value': i}
                                                      for i in sorted(self.data['domain'].dropna().unique())],
                                             placeholder="Select Domain...",
                                             multi=True,
                                             style=dropdown_style),
                                dcc.Dropdown(id='commodity-dropdown',
                                             options=[{'label': i, 'value': i}
                                                      for i in sorted(self.data['Commodity'].dropna().unique())],
                                             placeholder="Select Commodity...",
                                             multi=True,
                                             style=dropdown_style),
                                dcc.Dropdown(id='commodity-group-dropdown',
                                             options=[{'label': i, 'value': i} for i in
                                                      self.data['Commodity_Group'].dropna().unique().tolist()],
                                             placeholder="Select Commodity Group...",
                                             multi=True,
                                             style=dropdown_style),
                                dcc.Dropdown(id='scenario-filter',
                                             options=[{'label': i, 'value': i} for i in self.data['Scenario'].unique()],
                                             placeholder="Select Scenario...",
                                             multi=True,
                                             style=dropdown_style),
                                                
                                                # Download-Button
                                                html.Button(
                                                    "⬇️ CSV Export",
                                                    id="btn_csv",
                                                    style={
                                                        'height': '30px',
                                                        'marginLeft': 'auto',
                                                        'padding': '0 15px',
                                                        'borderRadius': '4px',
                                                        'border': '1px solid #ddd',
                                                        'whiteSpace': 'nowrap'
                                                    }
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ])
                ], className="mb-4"),  # Abstand nach unten

                # 2. Hauptinhalt (4 Boxen)
                dbc.Row(
                    className="g-3",
                    children=[
                        # Erste Zeile
                        dbc.Row([
                            dbc.Col(md=6, children=[
                                dbc.Card(
                                    className="h-100 shadow-sm",
                                    children=[
                                        dbc.CardBody(
                                            style={'padding': '15px'},
                                            children=[
                                                dcc.Graph(
                                                    id='graph-1',
                                                    style={'height': '35vh'}
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]),
                            dbc.Col(md=6, children=[
                                dbc.Card(
                                    className="h-100 shadow-sm",
                                    children=[
                                        dbc.CardBody(
                                            style={'padding': '15px'},
                                            children=[
                                                dcc.Graph(
                                                    id='graph-2',
                                                    style={'height': '35vh'}
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ])
                        ]),
                        
                        # Zweite Zeile
                        dbc.Row([
                            dbc.Col(md=6, children=[
                                dbc.Card(
                                    className="h-100 shadow-sm",
                                    children=[
                                        dbc.CardBody(
                                            style={'padding': '15px'},
                                            children=[
                                                dcc.Graph(
                                                    id='graph-3',
                                                    style={'height': '35vh'}
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]),
                            dbc.Col(md=6, children=[
                                dbc.Card(
                                    className="h-100 shadow-sm",
                                    children=[
                                        dbc.CardBody(
                                            style={'padding': '15px'},
                                            children=[
                                                dcc.Graph(
                                                    id='graph-4',
                                                    style={'height': '35vh'}
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ])
                        ])
                    ]
                )
            ]
        )



    def create_callbacks(self):
        @self.app.callback(
            [Output('quantity-plot', 'figure'),
             Output('price-plot', 'figure'),
             Output('forstock-plot', 'figure')],
            [Input('region-dropdown', 'value'),
             Input('continent-dropdown', 'value'),
             Input('domain-dropdown', 'value'),
             Input('commodity-dropdown', 'value'),
             Input('commodity-group-dropdown', 'value'),
             Input('scenario-filter', 'value')]
        )
        def update_plots(region, continent, domain, commodity, commodity_group,scenario):
            return self.update_plot_data(region, continent, domain, commodity, commodity_group,scenario)

        @self.app.callback(
            Output('world-map', 'figure'),
            [Input('scenario-filter', 'value'),
             Input('year-filter', 'value'),
             Input('region-dropdown', 'value'),
             Input('continent-dropdown', 'value'),
             Input('domain-dropdown', 'value'),
             Input('commodity-dropdown', 'value'),
             Input('commodity-group-dropdown', 'value')]
        )
        def update_world_map(scenario, year, region, continent, domain, commodity, commodity_group):
            return self.create_world_map(region, continent, domain, commodity, commodity_group, scenario, year)

        @self.app.callback(
            Output("download-dataframe-csv", "data"),
            Input("btn_csv", "n_clicks"),
            [State('region-dropdown', 'value'),
            State('continent-dropdown', 'value'),
            State('domain-dropdown', 'value'),
            State('commodity-dropdown', 'value'),
            State('commodity-group-dropdown', 'value'),
            State('scenario-filter', 'value')],  # Geändert von Input zu State
            prevent_initial_call=True
        )
        def func(n_clicks, region, continent, domain, commodity, commodity_group, scenario):
            if n_clicks is None:
                raise dash.exceptions.PreventUpdate
            filtered_data = self.filter_data(region, continent, domain, commodity, commodity_group, scenario)
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
