import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd


# Read in data
pollutant = pd.read_csv("data/raw/world_air_quality.csv", delimiter=';')


# Setup app and layout/frontend
app = dash.Dash(
    __name__, title="Air Quality Tracker", external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

app.layout = html.Div([
    html.H1('Pollutant Tracker'),
    
    # Filter by Type of Pollutant
    html.Div([
        html.Label('Select type of pollutant shown on the dashboard'),
        dcc.Checklist(
            id='pollutant_type_filter',
            options=[
                {'label': 'SO2', 'value': 'SO2'},
                {'label': 'NO', 'value': 'NO'},
                {'label': 'PM2.5', 'value': 'PM2.5'},
                {'label': 'CO', 'value': 'CO'},
                {'label': 'NOX', 'value': 'NOX'},
                {'label': 'NO2', 'value': 'NO2'},
                {'label': 'PM1', 'value': 'PM1'},
                {'label': 'PM10', 'value': 'PM10'},
            ],
            value='PM2.5',  # default selected value
            labelStyle={'display': 'inline-block'}
        ),
    ]),
    
    # Filter by Region
    html.Div([
        html.Label('Select region(s)'),
        dcc.Dropdown(
            id='region_filter',
            options=[
                    {"label": region, "value": region}
                    for region in ['Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']],
            value=['Asia'],  # default selected value
            multi=True
        ),
    ]),
    
    # Dropdown for Country
    html.Div([
        html.Label('Select country'),
        dcc.Dropdown(
            id='country_filter',
            options=[
                    {"label": country, "value": country}
                    for country in list(
                        pollutant["Country Label"].dropna().unique())],
            value='Japan',  # default selected value
            multi=True
        ),
    ]),
    
    # Filter by Time
    html.Div([
        html.Label('Select time period'),
        dcc.RangeSlider(
            id='time_filter',
            min=2020,
            max=2023,
            value=[2021, 2023],  # default selected values
            marks={i: str(i) for i in range(2020, 2024)},
            step=1
        ),
    ]),
    
    # Map for showing pollution levels
    html.Div([
        html.Label('Pollutant Tracker'),
        # Map
        dcc.Graph(id='pollution_map', figure={}),
    ]),
    
    # Side-by-side charts for top countries and trend over time
    html.Div([
        html.Div([
            html.Label('Top 15 Countries of Pollutant'),
            dcc.Graph(id='top_countries_chart', figure={}),
        ], style={'display': 'inline-block', 'width': '50%'}),
        
        html.Div([
            html.Label('Trend of Pollutant over time'),
            dcc.Graph(id='trend_chart', figure={}),
        ], style={'display': 'inline-block', 'width': '50%'}),
    ]),
])



# Set up callbacks/backend
@app.callback(
    Output("world_map", "srcDoc"),
    Input("pollutant", "value"),
    Input("region", "value"),
    Input("Country Label", "value"),
    Input("year", "value"),
)
def plot_map():
    return map


@app.callback(
    Output("bar", "srcDoc"),
    Input("pollutant", "value"),
    Input("region", "value"),
    Input("Country Label", "value"),
    Input("year", "value"),
)
def plot_bar():
    return bar


@app.callback(
    Output("line", "srcDoc"),
    Input("pollutant", "value"),
    Input("region", "value"),
    Input("Country Label", "value"),
    Input("year", "value"),
)
def plot_line():
    return line




if __name__ == "__main__":
    app.run_server()
