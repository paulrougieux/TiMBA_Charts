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

    def filter_data(self, region, estimate, scenario, model):
        data = self.data.copy()

        region_filter = region if region != ['All'] else data['Region'].unique()
        model_filter = model if model != ['All'] else data['Model'].unique()
        var_filter = estimate if estimate != 'All' else data['Estimate'].unique()
        sc_filter = scenario if scenario != ['All'] else data['Scenario'].unique()

        filtered_data = data[
            (data['Region'].isin(region_filter)) &
            (data['Model'].isin(model_filter)) &
            (data['Estimate'].isin(var_filter)) &
            (data['Scenario'].isin(sc_filter))
            ].reset_index(drop=True)

        return filtered_data

    def plot_min_max(self, data):
        fig_formip_main = go.Figure()

        for (model, region), subset in data.groupby(['Model', 'Region']):
            color = self.model_colors.get(model, (0, 0, 0))
            dash = 'solid'

            if model == 'Max':
                name_up_bnd = 'Upper bound max'
                name_low_bnd = 'Confidence interval max'
                name_mean = 'Mean max'
            if model == 'Min':
                name_up_bnd = 'Upper bound min'
                name_low_bnd = 'Confidence interval min'
                name_mean = 'Mean min'
            if model == 'TiMBA':
                name_up_bnd = 'Upper bound TiMBA'
                name_low_bnd = 'Confidence interval TiMBA'
                name_mean = 'Mean TiMBA'

            subset_new = pd.DataFrame()
            for year in subset['Year'].unique():
                subset_tmp = subset[subset['Year'] == year].reset_index(drop=True)
                subset_tmp_info = pd.DataFrame([subset_tmp.iloc[0, 0: -1]])
                subset_tmp_mean = pd.DataFrame([subset_tmp["Data"].mean()], columns=['mean'])
                subset_tmp_max = pd.DataFrame([subset_tmp["Data"].max()], columns=['max'])
                subset_tmp_min = pd.DataFrame([subset_tmp["Data"].min()], columns=['min'])

                subset_tmp_new = pd.concat(
                    [subset_tmp_info, subset_tmp_mean, subset_tmp_max, subset_tmp_min], axis=1).reset_index(drop=True)
                subset_new = pd.concat([subset_new, subset_tmp_new], axis=0)

            # Add upper bound
            fig_formip_main.add_trace(go.Scatter(
                x=subset_new['Year'],
                y=subset_new['max'],
                line=dict(color=f"rgba({color[0]}, {color[1]}, {color[2]}, 1)", width=0),
                mode='lines',
                showlegend=False,
                name=name_up_bnd
            ))

            # Add lower bound and fill to upper
            fig_formip_main.add_trace(go.Scatter(
                x=subset_new['Year'],
                y=subset_new['min'],
                fill='tonexty',
                fillcolor=f"rgba({color[0]}, {color[1]}, {color[2]}, 0.2)",
                line=dict(color=f"rgba({color[0]}, {color[1]}, {color[2]}, 1)", width=0),
                mode='lines',
                showlegend=True,
                name=name_low_bnd
            ))

            # Add the mean line
            fig_formip_main.add_trace(go.Scatter(
                x=subset_new['Year'],
                y=subset_new['mean'],
                line=dict(color=f"rgba({color[0]}, {color[1]}, {color[2]}, 1)", dash=dash),
                mode='lines',
                name=name_mean
            ))
        return fig_formip_main

    def plot_range(self, formip_data, timba_data):
        fig_formip_main = go.Figure()

        color_range = self.model_colors.get("", (0, 0, 0))
        dash = 'solid'
        formip_data = (formip_data.groupby('Year').agg(
            mean=('Data', 'mean'),
            min=('Data', 'min'),
            max=('Data', 'max')).reset_index())

        formip_data['lower_err'] = formip_data['mean'] - formip_data['min']
        formip_data['upper_err'] = formip_data['max'] - formip_data['mean']

        # Add upper bound ForMIP range
        fig_formip_main.add_trace(go.Scatter(
            x=formip_data['Year'],
            y=formip_data['max'],
            line=dict(color=f"rgba({color_range[0]}, {color_range[1]}, {color_range[2]}, 1)", width=0),
            mode='lines',
            showlegend=False,
            name="Upper bound"
        ))

        # Add lower bound ForMIP range
        fig_formip_main.add_trace(go.Scatter(
            x=formip_data['Year'],
            y=formip_data['min'],
            fill='tonexty',
            fillcolor=f"rgba({color_range[0]}, {color_range[1]}, {color_range[2]}, 0.2)",
            line=dict(color=f"rgba({color_range[0]}, {color_range[1]}, {color_range[2]}, 1)", width=0),
            mode='lines',
            showlegend=True,
            name="ForMIP Min-Max range"
        ))

        color = self.model_colors.get("TiMBA", (0, 0, 0))
        timba_data = (timba_data.groupby('Year').agg(
            mean=('Data', 'mean'),
            min=('Data', 'min'),
            max=('Data', 'max')).reset_index())

        timba_data['lower_err'] = timba_data['mean'] - timba_data['min']
        timba_data['upper_err'] = timba_data['max'] - timba_data['mean']

        # Add upper bound TiMBA
        fig_formip_main.add_trace(go.Scatter(
            x=timba_data['Year'],
            y=timba_data['max'],
            line=dict(color=f"rgba({color[0]}, {color[1]}, {color[2]}, 1)", width=0),
            mode='lines',
            showlegend=False,
            name="Upper bound"
        ))

        # Add lower bound TiMBA
        fig_formip_main.add_trace(go.Scatter(
            x=timba_data['Year'],
            y=timba_data['min'],
            fill='tonexty',
            fillcolor=f"rgba({color[0]}, {color[1]}, {color[2]}, 0.2)",
            line=dict(color=f"rgba({color[0]}, {color[1]}, {color[2]}, 1)", width=0),
            mode='lines',
            showlegend=True,
            name="TiMBA Min-Max range"
        ))

        # Add the mean line TiMBA
        fig_formip_main.add_trace(go.Scatter(
            x=timba_data['Year'],
            y=timba_data['mean'],
            line=dict(color=f"rgba({color[0]}, {color[1]}, {color[2]}, 1)", dash=dash),
            mode='lines',
            name="TiMBA mean"
        ))
        return fig_formip_main

    def plot_ssp_fsm_range(self, data):
        fig_formip_main = go.Figure()

        for (model, region), subset in data.groupby(['Model', 'Region']):
            color = self.model_colors.get(model, (0, 0, 0))
            dash = 'solid'

            name_up_bnd = f'Upper bound {model}'
            name_low_bnd = f'Min-Max range {model}'
            name_mean = f'Mean {model}'

            subset_new = pd.DataFrame()
            for year in subset['Year'].unique():
                subset_tmp = subset[subset['Year'] == year].reset_index(drop=True)
                subset_tmp_info = pd.DataFrame([subset_tmp.iloc[0, 0: -1]])
                subset_tmp_mean = pd.DataFrame([subset_tmp["Data"].mean()], columns=['mean'])
                subset_tmp_max = pd.DataFrame([subset_tmp["Data"].max()], columns=['max'])
                subset_tmp_min = pd.DataFrame([subset_tmp["Data"].min()], columns=['min'])

                subset_tmp_new = pd.concat(
                    [subset_tmp_info, subset_tmp_mean, subset_tmp_max, subset_tmp_min], axis=1).reset_index(drop=True)
                subset_new = pd.concat([subset_new, subset_tmp_new], axis=0)

            # Add upper bound
            fig_formip_main.add_trace(go.Scatter(
                x=subset_new['Year'],
                y=subset_new['max'],
                line=dict(color=f"rgba({color[0]}, {color[1]}, {color[2]}, 1)", width=0),
                mode='lines',
                showlegend=False,
                name=name_up_bnd
            ))

            # Add lower bound and fill to upper
            fig_formip_main.add_trace(go.Scatter(
                x=subset_new['Year'],
                y=subset_new['min'],
                fill='tonexty',
                fillcolor=f"rgba({color[0]}, {color[1]}, {color[2]}, 0.2)",
                line=dict(color=f"rgba({color[0]}, {color[1]}, {color[2]}, 1)", width=0),
                mode='lines',
                showlegend=True,
                name=name_low_bnd
            ))

            # Add the mean line
            fig_formip_main.add_trace(go.Scatter(
                x=subset_new['Year'],
                y=subset_new['mean'],
                line=dict(color=f"rgba({color[0]}, {color[1]}, {color[2]}, 1)", dash=dash),
                mode='lines',
                name=name_mean
            ))
        return fig_formip_main

    def plot_ssp_fsm_all(self, data):
        fig_formip_main = go.Figure()
        dash_styles = {}
        dash_list = ["solid", "dash", "dot", "longdash", "dashdot", "longdashdot"]
        dash_runner = 0
        for scenario in data["Scenario"].unique():
            if dash_runner > 5:
                dash_runner = 0

            dash_styles[scenario] = dash_list[dash_runner]

            dash_runner += 1
        
        for (model, region, scenario), subset in data.groupby(['Model', 'Region', 'Scenario']):
            color = self.model_colors.get(model, (0, 0, 0))
            name_mean = f'{model}_{scenario}'

            subset_new = pd.DataFrame()
            for year in subset['Year'].unique():
                subset_tmp = subset[subset['Year'] == year].reset_index(drop=True)
                subset_tmp_info = pd.DataFrame([subset_tmp.iloc[0, 0: -1]])
                subset_tmp_mean = pd.DataFrame([subset_tmp["Data"].mean()], columns=['mean'])

                subset_tmp_new = pd.concat(
                    [subset_tmp_info, subset_tmp_mean], axis=1).reset_index(drop=True)
                subset_new = pd.concat([subset_new, subset_tmp_new], axis=0)

            # Add the mean line
            fig_formip_main.add_trace(go.Scatter(
                x=subset_new['Year'],
                y=subset_new['mean'],
                line=dict(color=f"rgba({color[0]}, {color[1]}, {color[2]}, 1)", dash=dash_styles[scenario]),
                mode='lines',
                name=name_mean
            ))

        return fig_formip_main


    def update_plot_validation(self, region, estimate, scenario, model, figure_type):
        graphic_template = 'plotly_white'  # 'plotly_dark'#'plotly_white'
        filtered_data = self.filter_data(region, estimate, scenario, model)

        filtered_data = filtered_data.reset_index(drop=True)
        filtered_data['Model'] = filtered_data['Model'].str.strip()

        # ForMIP main plot (absolute value comparison)

        if (figure_type == 'min_max') | (figure_type == 'range'):
            timba_data = filtered_data[filtered_data['Model'] == 'TiMBA'].reset_index(drop=True)

            fsm_data = filtered_data[filtered_data['Model'] != 'TiMBA'].reset_index(drop=True)
            fsm_data_max = fsm_data.groupby(['Year', 'Region', 'Estimate', 'Scenario'])['Data'].max().reset_index()
            fsm_data_min = fsm_data.groupby(['Year', 'Region', 'Estimate', 'Scenario'])['Data'].min().reset_index()
            fsm_data_max['Model'] = 'Max'
            fsm_data_min['Model'] = 'Min'

            if figure_type == 'min_max':
                data_fin = pd.concat([timba_data, fsm_data_max, fsm_data_min], axis=0).reset_index(drop=True)
                fig_formip_main = self.plot_min_max(data=data_fin)

            if figure_type == 'range':
                data_fin = pd.concat([fsm_data_max, fsm_data_min], axis=0).reset_index(drop=True)
                fig_formip_main = self.plot_range(formip_data=data_fin, timba_data=timba_data)

        if figure_type == "ssp_fsm_range":
            fig_formip_main = self.plot_ssp_fsm_range(data=filtered_data)

        if figure_type == "ssp_fsm_all":
            fig_formip_main = self.plot_ssp_fsm_all(data=filtered_data)

        title_formip_main = self.generate_title(region, estimate, scenario, model)
        title = title_formip_main

        fig_formip_main.update_layout(
            title='<br>'.join(textwrap.wrap(title, width=150)),
            xaxis_title='Year',
            yaxis_title=f'{estimate[0]}',
            xaxis=dict(gridcolor='white'),
            yaxis=dict(rangemode='nonnegative', zeroline=True, zerolinewidth=2, zerolinecolor='LightGrey',
                       gridcolor='white'),
            legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5),
            margin=dict(l=35, r=35, t=110, b=90),
            hovermode='x unified',
            template=graphic_template,
            plot_bgcolor='rgb(229, 236, 246)'
        )

        # ForMIP secondary plot (relative value comparison)
        fig_formip_second = go.Figure()

        # ForMIP teriary plot
        fig_formip_third = go.Figure()

        return fig_formip_main, fig_formip_second, fig_formip_third


    def generate_title(self, region, estimate, scenario, model):
        title_parts = []
        if estimate:
            title_parts.append(f"{estimate}")
        if region:
            title_parts.append(f" for {region}<br>")
        if scenario:
            title_parts.append(f"Scenarios: {scenario}<br>")
        if model:
            title_parts.append(f"Models: {model}")
        title = "".join(title_parts) if title_parts else "all data"
        clean_title = title.replace("'", "").replace("[", "").replace("]", "")
        return clean_title

    def create_world_map(self, region, continent, domain, commodity, commodity_group, scenario=None, year=None):
        pass

    def open_browser(self):
        webbrowser.open_new("http://localhost:8050")

    def run(self):
        Timer(1, self.open_browser).start()
        self.app.run(host='localhost', debug=False, dev_tools_ui=False, dev_tools_hot_reload=False, port=8050)
