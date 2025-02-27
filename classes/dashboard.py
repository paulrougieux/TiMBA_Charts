import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

class DashboardPlotter:
    def __init__(self, data):
        self.data = data
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.start = self.data['year'].min()
        self.end = self.data['year'].max()
        self.color_list = ['black','darkblue','green','red','yellow','purple','cyan','orange','pink','brown','teal']
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
                                         options=[{'label': i, 'value': i} for i in ['Alle'] + self.data['RegionCode'].dropna().unique().tolist()], 
                                         value='Alle',
                                         style=dropdown_style),
                            dcc.Dropdown(id='continent-dropdown', 
                                         options=[{'label': i, 'value': i} for i in ['Alle'] + self.data['Continent'].dropna().unique().tolist()], 
                                         value='Alle',
                                         style=dropdown_style),
                            dcc.Dropdown(id='domain-dropdown', 
                                         options=[{'label': i, 'value': i} for i in ['Alle'] + self.data['domain'].dropna().unique().tolist()], 
                                         value='Alle',
                                         style=dropdown_style),
                            dcc.Dropdown(id='commodity-dropdown', 
                                         options=[{'label': i, 'value': i} for i in ['Alle'] + self.data['CommodityCode'].dropna().unique().tolist()], 
                                         value='Alle',
                                         style=dropdown_style),
                        ])
                    ], className="mb-4")
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='plot',
                                      config={'toImageButtonOptions': {'format': 'png', 'filename': 'dashboard_plot'}},
                                      style={'height': '85vh'})
                        ])
                    ])
                ], width=9)
            ])
        ], fluid=True)

    def create_callbacks(self):
        @self.app.callback(
            Output('plot', 'figure'),
            [Input('region-dropdown', 'value'),
             Input('continent-dropdown', 'value'),
             Input('domain-dropdown', 'value'),
             Input('commodity-dropdown', 'value')]
        )
        def update_plot(region, continent, domain, commodity):
            return self.update_plot_data(region, continent, domain, commodity)

    def update_plot_data(self, region, continent, domain, commodity):
        filtered_data = self.data

        if region != 'Alle':
            filtered_data = filtered_data[filtered_data['RegionCode'] == region]
        if continent != 'Alle':
            filtered_data = filtered_data[filtered_data['Continent'] == continent]
        if domain != 'Alle':
            filtered_data = filtered_data[filtered_data['domain'] == domain]
        if commodity != 'Alle':
            filtered_data = filtered_data[filtered_data['CommodityCode'] == commodity]

        grouped_data = filtered_data.groupby(['year', 'Scenario']).sum().reset_index()
        grouped_data = grouped_data[(grouped_data["year"] >= self.start) & (grouped_data["year"] < self.end)]

        fig = go.Figure()

        for i, scenario in enumerate(grouped_data['Scenario'].unique()):
            subset = grouped_data[grouped_data['Scenario'] == scenario]
            color = self.color_list[i % len(self.color_list)]
            dash = 'solid' if scenario in ['World500', 'FAOStat'] else 'dash'
            fig.add_trace(go.Scatter(x=subset['year'], y=subset['quantity'], mode='lines', 
                                     name=f'M: {scenario}', line=dict(color=color, dash=dash)))

        title = self.generate_title(region, continent, domain, commodity)
        fig.update_layout(
            title=title,
            xaxis_title='Year',
            yaxis_title='Quantity',
            yaxis=dict(rangemode='nonnegative', zeroline=True, zerolinewidth=2, zerolinecolor='LightGrey'),
            legend_title='Scenario',
            hovermode='x unified',
            template='plotly_white'
        )

        return fig

    def generate_title(self, region, continent, domain, commodity):
        title_parts = []
        if region != 'Alle':
            title_parts.append(f"Region: {region}")
        if continent != 'Alle':
            title_parts.append(f"Continent: {continent}")
        if domain != 'Alle':
            title_parts.append(f"Domain: {domain}")
        if commodity != 'Alle':
            title_parts.append(f"Commodity: {commodity}")
        
        return "Figure for " + ", ".join(title_parts) if title_parts else "Figure for all data"

    def run(self):
        self.app.run_server(debug=True)