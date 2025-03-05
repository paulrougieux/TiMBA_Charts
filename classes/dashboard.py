import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from pathlib import Path
import plotly.express as px

PACKAGEDIR = Path(__file__).parent.parent.absolute()

class DashboardPlotter:

    def __init__(self, data):
        self.data = data
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.start = self.data['year'].min()
        self.end = self.data['year'].max()
        self.color_list = ['darkblue','green','purple','cyan','red','yellow','orange','pink','brown','teal']
        self.logo = PACKAGEDIR/'timba_logo_v3.png'
        self.create_layout()
        self.create_callbacks()

    def create_layout(self):
        dropdown_style = {'height': '30px','marginBottom': '10px'}
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col(html.H1("TiMBA Dashboard", className="text-center mb-4"), width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Filters", className="card-title"),
                            dcc.Dropdown(id='region-dropdown',
                                         options=[{'label': i, 'value': i} for i in ['Country'] + self.data['ISO3'].dropna().unique().tolist()],
                                         value='Country',
                                         style=dropdown_style),
                            dcc.Dropdown(id='continent-dropdown',
                                         options=[{'label': i, 'value': i} for i in ['Continent'] + self.data['Continent'].dropna().unique().tolist()],
                                         value='Continent',
                                         style=dropdown_style),
                            dcc.Dropdown(id='domain-dropdown',
                                         options=[{'label': i, 'value': i} for i in ['Domain'] + self.data['domain'].dropna().unique().tolist()],
                                         value='Domain',
                                         style=dropdown_style),
                            dcc.Dropdown(id='commodity-dropdown',
                                         options=[{'label': i, 'value': i} for i in ['Commodity'] + self.data['Commodity'].dropna().unique().tolist()],
                                         value='Commodity',
                                         style=dropdown_style),
                            dcc.Dropdown(id='commodity-group-dropdown',
                                         options=[{'label': i, 'value': i} for i in ['Commodity_Group'] + self.data['Commodity_Group'].dropna().unique().tolist()],
                                         value='Commodity_Group',
                                         style=dropdown_style),
                            html.Button("Download CSV", id="btn_csv"),
                            dcc.Download(id="download-dataframe-csv"),
                        ])
                    ], className="mb-4", style={'white': 'white'}),  #filter box
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='price-plot',
                                      config={'toImageButtonOptions': {'format': 'png', 'filename': 'price_plot'}},
                                      style={'height': '54.5vh'})
                    ])
                ], style={'white': 'white'})  #price box
            ], width=3),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='quantity-plot',
                                          config={'toImageButtonOptions': {'format': 'png', 'filename': 'quantity_plot'}},
                                          style={'height': '85.75vh'})
                            ])
                        ], style={'backgroundColor': 'white'}) #mittelbox
                    ], width=8), # Breite auf 8 reduziert
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='forstock-plot',  # Geändert: ID auf 'forstock-plot'
                                          config={'toImageButtonOptions': {'format': 'png'}},
                                          style={'height': '40vh'})
                            ])
                        ], style={'backgroundColor': 'white', 'marginBottom': '20px'}), # Abstand hinzugefügt
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='placeholder-plot-2',
                                          config={'toImageButtonOptions': {'format': 'png'}},
                                          style={'height': '40vh'})
                            ])
                        ], style={'backgroundColor': 'white'})
                    ], width=4), # Breite auf 4 gesetzt
                ]),
            ], width=9)
        ])
    ], fluid=True, style={'backgroundColor': 'white'}) #gesamthintergrund

    def create_callbacks(self):
        @self.app.callback(
            [Output('quantity-plot', 'figure'),
             Output('price-plot', 'figure'),
             Output('forstock-plot', 'figure')
             ], # Hinzugefügt: Output für 'forstock-plot'
            [Input('region-dropdown', 'value'),
             Input('continent-dropdown', 'value'),
             Input('domain-dropdown', 'value'),
             Input('commodity-dropdown', 'value'),
             Input('commodity-group-dropdown', 'value')]
        )
        def update_plots(region, continent, domain, commodity, commodity_group):
            return self.update_plot_data(region, continent, domain, commodity, commodity_group)
        @self.app.callback(
            Output("download-dataframe-csv", "data"),
            Input("btn_csv", "n_clicks"),
            [State('region-dropdown', 'value'),
             State('continent-dropdown', 'value'),
             State('domain-dropdown', 'value'),
             State('commodity-dropdown', 'value'),
             State('commodity-group-dropdown', 'value')],
            prevent_initial_call=True
        )
        def func(n_clicks, region, continent, domain, commodity, commodity_group):
            filtered_data = self.filter_data(region, continent, domain, commodity, commodity_group)
            return dcc.send_data_frame(filtered_data.to_csv, "filtered_data.csv")

    def filter_data(self, region, continent, domain, commodity, commodity_group):
        filtered_data = self.data
        if region != 'Country':
            filtered_data = filtered_data[filtered_data['ISO3'] == region]
        if continent != 'Continent':
            filtered_data = filtered_data[filtered_data['Continent'] == continent]
        if domain != 'Domain':
            filtered_data = filtered_data[filtered_data['domain'] == domain]
        if commodity != 'Commodity':
            filtered_data = filtered_data[filtered_data['Commodity'] == commodity]
        if commodity_group != 'Commodity_Group':
            filtered_data = filtered_data[filtered_data['Commodity_Group'] == commodity_group]
        return filtered_data

    def update_plot_data(self, region, continent, domain, commodity, commodity_group):
        filtered_data = self.filter_data(region, continent, domain, commodity, commodity_group)

        # Quantity plot
        grouped_data_quantity = filtered_data.groupby(['year', 'Scenario']).sum().reset_index()
        grouped_data_quantity = grouped_data_quantity[(grouped_data_quantity["year"] >= self.start) & (grouped_data_quantity["year"] < self.end)]
        fig_quantity = go.Figure()
        for i, scenario in enumerate(grouped_data_quantity['Scenario'].unique()):
            subset = grouped_data_quantity[grouped_data_quantity['Scenario'] == scenario]
            color = self.color_list[i % len(self.color_list)]
            dash = 'solid' if scenario in ['Historic Data'] else 'dash'
            fig_quantity.add_trace(go.Scatter(x=subset['year'], y=subset['quantity'], mode='lines',
                                              name=f'{scenario}', line=dict(color=color, dash=dash)))
        title_quantity = self.generate_title(region, continent, domain, commodity, commodity_group)
        fig_quantity.update_layout(
            title=title_quantity,
            xaxis_title='Year',
            yaxis_title='Quantity',
            yaxis=dict(rangemode='nonnegative', zeroline=True, zerolinewidth=2, zerolinecolor='LightGrey'),
            legend_title='Scenario',
            legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5),
            hovermode='x unified',
            template='plotly_white'
        )

        # Price plot
        grouped_data_price = filtered_data.groupby(['Period', 'Scenario']).mean().reset_index()
        fig_price = go.Figure()
        for i, scenario in enumerate(grouped_data_price['Scenario'].unique()):
            subset = grouped_data_price[grouped_data_price['Scenario'] == scenario]
            color = self.color_list[i % len(self.color_list)]
            fig_price.add_trace(go.Bar(x=subset['price'], y=subset['Period'], orientation='h',
                                       name=f'{scenario}', marker_color=color))
        title_price = f'Price by Period and Scenario'
        fig_price.update_layout(
            title=title_price,
            xaxis_title='Price',
            yaxis_title='Period',
            legend_title='Scenario',
            template='plotly_white',
            showlegend=True,
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
            margin=dict(l=50, r=50, t=50, b=100),  # Increased bottom margin to accommodate legend
            barmode='group'
        )

        # ForStock plot
        grouped_data_stock = filtered_data.drop(columns=['domain', 'Domain', 'price','quantity','CommodityCode','Commodity','Commodity_Group'])
        grouped_data_stock = grouped_data_stock.drop_duplicates().reset_index(drop=True)
        grouped_data_stock = grouped_data_stock.groupby(['year', 'Scenario']).agg({
            'ForStock': 'sum',  # Summe von ForStock
            }).reset_index()
        grouped_data_stock = grouped_data_stock[grouped_data_stock.Scenario!='Historic Data']
        print('grouped',grouped_data_stock)
        fig_stock = go.Figure()
        for i, scenario in enumerate(grouped_data_stock['Scenario'].unique()):
            subset = grouped_data_stock[grouped_data_stock['Scenario'] == scenario]
            color = self.color_list[i % len(self.color_list)]
            fig_stock.add_trace(go.Bar(x=subset['year'], y=subset['ForStock'],
                                    name=f'{scenario}', marker_color=color))

        # Angenommen, 'Period' enthält die Jahreszahlen
        min_year = grouped_data_stock['year'].min() - 1
        max_year = grouped_data_stock['year'].max() + 0.5

        fig_stock.update_layout(
            title='ForStock by Year and Scenario',
            xaxis_title='Year',
            xaxis=dict(range=[min_year, max_year]),
            yaxis_title='ForStock',
            template='plotly_white',
            showlegend=True,
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
            barmode='group'
        )



        return fig_quantity, fig_price, fig_stock # Hinzugefügt: fig_forstock zum Return

    def generate_title(self, region, continent, domain, commodity, commodity_group):
        title_parts = []
        if region != 'Country':
            title_parts.append(f"{region}")
        if continent != 'Continent':
            title_parts.append(f"{continent}")
        if domain != 'Domain':
            title_parts.append(f"{domain}")
        if commodity != 'Commodity':
            title_parts.append(f"{commodity}")
        if commodity_group != 'Commodity_Group':
            title_parts.append(f"{commodity_group}")
        return "Quantity by Period and Scenario for " + ", ".join(title_parts) if title_parts else "Quantity by Period and Scenario for all data"

    def run(self):
        self.app.run_server(debug=True)
