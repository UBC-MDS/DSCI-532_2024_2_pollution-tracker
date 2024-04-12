import dash
from dash import html
from dash import dcc
import dash_vega_components as dvc
from dash.dependencies import Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import dash_mantine_components as dmc
from dash import dash_table
import json
import plotly.express as px


# Read in data
data = pd.read_csv("data/processed/world_air_quality.csv")
data['time'] = pd.to_datetime(data['time']).dt.date

# Setup app and layout/frontend
app = dash.Dash(
    __name__, title="Air Quality Tracker", external_stylesheets=['https://bootswatch.com/4/lux/bootstrap.css']
)
server = app.server

# Filters
pollutant_filter = html.Div([
    html.Label('Select pollutant:'),
    dcc.RadioItems(
        id='pollutant_type_filter',
        options=[{'label': i, 'value': i} for i in ['PM2.5', 'SO2', 'NO', 'CO', 'NOX', 'NO2', 'PM1', 'PM10']],
        value='PM2.5',
        labelStyle={'display': 'inline-block', 'margin-right': '20px'}
    )
], style={'textAlign': 'center'})

region_filter = html.Div([
    html.Label('Select region(s):'),
    dcc.Dropdown(
        id='region_filter',
        options=[{"label": region, "value": region} for region in data['continent'].unique()],
        #value=['Asia'],  # default selected value
        multi=True,
        placeholder='Select multiple continents...'
    )
])

years = list(range(2014, 2025))
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

start_year_dropdown = dcc.Dropdown(
    id='start_year',
    options=[{'label': year, 'value': year} for year in years],
    value=years[0]
)

start_month_dropdown = dcc.Dropdown(
    id='start_month',
    options=[{'label': month, 'value': i+1} for i, month in enumerate(month_names)],
    value=1
)

end_year_dropdown = dcc.Dropdown(
    id='end_year',
    options=[{'label': year, 'value': year} for year in years],
    value=years[-1]
)

end_month_dropdown = dcc.Dropdown(
    id='end_month',
    options=[{'label': month, 'value': i+1} for i, month in enumerate(month_names)],
    value=12
)

# time_period_picker_1 = html.Div([
#     html.Div(style={'width': '20%', 'display': 'inline-block'}), 

#     html.Div([
#         html.Div('Start Month', style={'margin-bottom': '5px'}),
#         dcc.Dropdown(
#             id='start_year',
#             options=[{'label': year, 'value': year} for year in years],
#             value=years[0],
#             style={'width': '50%', 'display': 'inline-block'}
#         ),
#         dcc.Dropdown(
#             id='start_month',
#             options=[{'label': month, 'value': i+1} for i, month in enumerate(month_names)],
#             value=1,
#             style={'width': '50%', 'display': 'inline-block'}
#         ),
#     ], style={'display': 'inline-block', 'width': '29%', 'vertical-align': 'top'}),

#     html.Div('|', style={'display': 'inline-block', 'width': '2%', 'text-align': 'center', 'font-size': '24px'}),

#     html.Div([
#         html.Div('End Month', style={'margin-bottom': '5px'}),
#         dcc.Dropdown(
#             id='end_year',
#             options=[{'label': year, 'value': year} for year in years],
#             value=years[-1],
#             style={'width': '50%', 'display': 'inline-block'}
#         ),
#         dcc.Dropdown(
#             id='end_month',
#             options=[{'label': month, 'value': i+1} for i, month in enumerate(month_names)],
#             value=12,
#             style={'width': '50%', 'display': 'inline-block'}
#         ),
#     ], style={'display': 'inline-block', 'width': '29%', 'vertical-align': 'top'}),
    
#     html.Div(style={'width': '20%', 'display': 'inline-block'}), 
# ], style={"width": "100%", 'textAlign': 'center'})

country_filter = html.Div([
    html.Label('Select country:'),
    dcc.Dropdown(
        id='country_filter',
        options=[{"label": country, "value": country} for country in data['countryname'].unique()],
        value='Japan',  # default selected value
    )
])


graph_placeholder = html.Div([
    html.Label('Worldwide Distribution'),
    dcc.Graph(id='graph'),  # Placeholder for the pollution map
])

top_countries_chart = html.Div([
    html.H3('Top 15 Countries of Pollutant'),
    dvc.Vega(id='top_countries_chart', spec={}, style={'width': '100%', 'height': '100%'})
])

data_summary = html.Div([
    html.H3('Data Summary'),
    dash_table.DataTable(
        id='data-summary-table',
        style_cell={'textAlign': 'center'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
    )
], style={'width': '100%'})

trend_chart = html.Div([
    html.H3('Trend of Pollutant over time'),
    dvc.Vega(id='trend_chart', spec={}, style={'width': '100%', 'height': '100%'})
])

# Layout
app.layout = html.Div([
    dbc.Row(html.H1('Pollutant Tracker'), justify="center"),
    dbc.Row(pollutant_filter, justify="center"),
    dbc.Row([
        dbc.Col(width=1.3), 
        dbc.Col(html.Div([
            html.Label('Start Year:'),
            start_year_dropdown
        ]), width=2), 
        dbc.Col(html.Div([
            html.Label('Start Month:'),
            start_month_dropdown
        ]), width=2),
        dbc.Col(width=0.7),
        dbc.Col(html.Div(className='text-center', style={'borderLeft': '1px solid #ccc', 'height': '50px'}), width=0.7),
        dbc.Col(html.Div([
            html.Label('End Year:'),
            end_year_dropdown
        ]), width=2),  
        dbc.Col(html.Div([
            html.Label('End Month:'),
            end_month_dropdown
        ]), width=2),
        dbc.Col(width=1.3),
    ], justify="center"),
    html.Hr(),
    # First card with header: Region, Time Period Picker for Region, Graph, and Top Countries Chart
    dbc.Card(
        [
            dbc.CardHeader("Worldwide Comparison", className="font-weight-bold"),  # Card header with title
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(region_filter, width=3)
                ], justify="start"),
                html.Hr(), 
                dbc.Row([
                    dbc.Col(graph_placeholder, width=8),
                    dbc.Col(top_countries_chart, width=4)
                ], justify="around"),
            ]),
        ],
        className="mb-3", 
    ),
    # Second card with header: Country Filter, Time Period Picker for Country, Data Summary, and Trend Chart
    dbc.Card(
        [
            dbc.CardHeader("Country of Interest Trend", className="font-weight-bold"),  # Card header with title
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(country_filter, width=3),
                ], justify="start"),
                html.Hr(),  
                dbc.Row([
                    dbc.Col(trend_chart, width=4),
                    dbc.Col(data_summary, width=4),
                ], justify="around"),
            ]),
        ],
        className="mb-3",
    ),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.P(" ", style={"font-size": "16px"}),
                html.P("This dashboard visualizes global air pollution levels, making it easy to explore global and local trends",
                       style={"font-size": "16px"}),
                html.P("Creators: Merete Lutz, Kun Ya, Weiran Zhao, Sid Grover",
                       style={"font-size": "12px"}),
                html.A("GitHub Repository", href="https://github.com/UBC-MDS/DSCI-532_2024_2_pollution-tracker",
                       target="_blank", style={"font-size": "12px"}),
                html.P("Last updated on April 7, 2024",
                       style={"font-size": "12px"}),
            ])
        ], width=12),
    ]),
])




# Set up callbacks/backend
@app.callback(
    Output("graph", "figure"), 
    Input("pollutant_type_filter", "value"),
    Input("region_filter", "value"),
    Input("start_year", "value"),
    Input("start_month", "value"),
    Input("end_year", "value"),
    Input("end_month", "value"),
)

def display_choropleth(selected_pollutant, regions, start_year, start_month, end_year, end_month):
    region_centers = {
    'Asia': {'lat': 34.0479, 'lon': 100.6197},
    'Europe': {'lat': 54.5260, 'lon': 15.2551},
    'Africa': {'lat': -8.7832, 'lon': 34.5085},
    'North America': {'lat': 54.5260, 'lon': -105.2551},
    'South America': {'lat': -8.7832, 'lon': -55.4915},
    'Australia': {'lat': -25.2744, 'lon': 133.7751}
}

    start_date_str = f"{start_year}-{start_month:02d}"
    end_date_str = f"{end_year}-{end_month:02d}"
    start_date = pd.to_datetime(start_date_str).date()
    end_date = pd.to_datetime(end_date_str).date()

    with open("data/raw/custom.geo.json", "r", encoding="utf-8") as f:
        countries_geojson = json.load(f)
    
    df = data
    filtered_data = data[
        (data['pollutant'] == selected_pollutant) &
        (data['time'] >= start_date) &
        (data['time'] <= end_date)
    ]

    if regions:
        filtered_data = filtered_data[filtered_data['continent'].isin(regions)]

    aggregated_data = filtered_data.groupby('countryname')['value'].mean().reset_index()
    
    map = px.choropleth(
        aggregated_data,
        geojson=countries_geojson,
        locations='countryname',          #aggregated data country label should exactly match name in featureidkey
        color='value',       
        featureidkey="properties.admin", #for country name
        color_continuous_scale=px.colors.sequential.Plasma,  # Example color scale
    )

    if regions and len(regions) == 0:
        center = None
        projection_scale = 1
    elif regions and len(regions) == 1: 
        center = region_centers.get(regions[0], {'lat': 0, 'lon': 0})
        projection_scale = 1.5
    else:
        center = {'lat': 0, 'lon': 0}
        projection_scale = 1
            
    map.update_layout(
        geo=dict(
            center = center,
            projection_type = 'natural earth',
            projection_scale = projection_scale
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return map


@app.callback(
    Output("top_countries_chart", "spec"),
    [
        Input("pollutant_type_filter", "value"),
        Input("start_year", "value"),
        Input("start_month", "value"),
        Input("end_year", "value"),
        Input("end_month", "value"),
        Input("region_filter", "value")
    ]
)
def plot_bar(pollutant, start_year, start_month, end_year, end_month, regions):
    start_date_str = f"{start_year}-{start_month:02d}"
    end_date_str = f"{end_year}-{end_month:02d}"
    start_date = pd.to_datetime(start_date_str).date()
    end_date = pd.to_datetime(end_date_str).date()

    filtered_data = data[
        (data['time'] >= start_date) &
        (data['time'] <= end_date) &
        (data['pollutant'] == pollutant)
    ]

    if regions:
        filtered_data = filtered_data[filtered_data['continent'].isin(regions)]

    top_countries_data = filtered_data.groupby('countryname', as_index=False)['value'].mean().sort_values(by='value', ascending=False).head(15)

    bar = alt.Chart(top_countries_data).mark_bar(fill='black').encode(
        x=alt.X('value:Q', title='Average AQI Value'),
        y=alt.Y('countryname:N', title='Country', sort='-x'),
        tooltip=[
            alt.Tooltip('countryname:N', title='Country'),
            alt.Tooltip('value:Q', title='AQI value')
        ]
    ).properties(
        title='Top 15 Countries by AQI Value',
        width=250,
        height=300
    ).to_dict()
    
    return bar


@app.callback(
    Output("trend_chart", "spec"),
    Input("pollutant_type_filter", "value"),
    Input("country_filter", "value"),
    Input("start_year", "value"),
    Input("start_month", "value"),
    Input("end_year", "value"),
    Input("end_month", "value"),
)

def plot_line(pollutant, countries, start_year, start_month, end_year, end_month):
    start_date_str = f"{start_year}-{start_month:02d}"
    end_date_str = f"{end_year}-{end_month:02d}"
    start_date = pd.to_datetime(start_date_str).date()
    end_date = pd.to_datetime(end_date_str).date()
    
    filtered_data = data[
        (data['time'] >= start_date) &
        (data['time'] <= end_date) &
        (data['countryname']== countries) &
        (data['pollutant'] == pollutant)
    ]
    filtered_data['time'] = filtered_data['time'].astype(str)
    line = alt.Chart(filtered_data).mark_line(color='black').encode(
        x=alt.X('time:T', axis=alt.Axis(title='Date', format='%Y-%m')), 
        y=alt.Y('value:Q', axis=alt.Axis(title='Value')),  
        #color=alt.Color('countryname:N', legend=alt.Legend(title='Country')),
        tooltip=[
        alt.Tooltip('time:T', title='Date', format='%Y-%m-%d'),
        alt.Tooltip('value:Q', title='AQI value'),
        alt.Tooltip('countryname:N', title='Country')
        ]
        ).properties(
            title='Air Quality Index (AQI) Over Time',
            width=400,
            height=300
        ).to_dict()
    return line

@app.callback(
    Output('data-summary-table', 'columns'),
    Output('data-summary-table', 'data'),
    Input("pollutant_type_filter", "value"),
    Input("country_filter", "value"),
    Input("start_year", "value"),
    Input("start_month", "value"),
    Input("end_year", "value"),
    Input("end_month", "value"),
)

def summary(pollutant, countries, start_year, start_month, end_year, end_month):
    start_date_str = f"{start_year}-{start_month:02d}"
    end_date_str = f"{end_year}-{end_month:02d}"
    start_date = pd.to_datetime(start_date_str).date()
    end_date = pd.to_datetime(end_date_str).date()
    
    filtered_data = data[
        (data['time'] >= start_date) &
        (data['time'] <= end_date) &
        (data['countryname'] == countries) &
        (data['pollutant'] == pollutant)
    ]
    summary = filtered_data.describe().reset_index()
    summary.rename(columns={'index': 'Statistic'}, inplace=True)

    # Round numerical columns to two decimal places
    for col in summary.select_dtypes(include=['float64']).columns:
        summary[col] = summary[col].round(2)

    columns = [{"name": i, "id": i} for i in summary.columns]
    summary_data = summary.to_dict('records')

    return columns, summary_data


if __name__ == '__main__':
    app.run_server(debug=True)
