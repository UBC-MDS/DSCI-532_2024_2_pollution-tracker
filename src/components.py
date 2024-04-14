from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import dash_table

def get_filters(data):
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
            multi=True,
            placeholder='Select multiple continents...'
        )
    ])

    country_filter = html.Div([
        html.Label('Select countries:'),
        dcc.Dropdown(
            id='country_filter',
            options=[{"label": country, "value": country} for country in data['countryname'].unique()],
            multi=True,
            placeholder='Select multiple countries...'
        )
    ])

    return pollutant_filter, region_filter, country_filter

def get_datepickers():
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

    return start_year_dropdown, start_month_dropdown, end_year_dropdown, end_month_dropdown

graph_placeholder = html.Div([
    html.Label('Worldwide Distribution', style={'fontSize': '29px', 'textAlign': 'center'}),
    dcc.Graph(id='graph'),  # Placeholder for the pollution map
])

top_countries_chart = html.Div([
    html.H3('Top 15 Countries of Pollutant'),
    dvc.Vega(id='top_countries_chart',
             opt={"renderer": "svg", "actions": False},
             spec={}, 
             style={'width': '100%', 'height': '100%'})
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
    dvc.Vega(id='trend_chart', 
             opt={"renderer": "svg", "actions": False}, 
             spec={}, 
             style={'width': '100%', 'height': '100%'})
])

def get_layout(data):
    pollutant_filter, region_filter, country_filter = get_filters(data)
    start_year_dropdown, start_month_dropdown, end_year_dropdown, end_month_dropdown = get_datepickers()

    layout = html.Div([
        dbc.Row(
        dbc.Col(html.H1('Pollution Tracker', className='text-center my-4'), width=12),
        justify='center',
        align='center',
        className='g-0',  # No gutters
    ),
        dbc.Row(pollutant_filter, justify="center", style={'color': 'white'}),
        dbc.Row([
            dbc.Col(width=1.3), 
            dbc.Col(html.Div([
                html.Label('Start Year:', style={'color': 'white'}),
                start_year_dropdown
            ]), width=2), 
            dbc.Col(html.Div([
                html.Label('Start Month:', style={'color': 'white'}),
                start_month_dropdown
            ]), width=2),
            dbc.Col(width=0.7),
            dbc.Col(html.Div(className='text-center', style={'borderLeft': '1px solid #ccc', 'height': '50px'}), width=0.7),
            dbc.Col(html.Div([
                html.Label('End Year:', style={'color': 'white'}),
                end_year_dropdown
            ]), width=2),  
            dbc.Col(html.Div([
                html.Label('End Month:', style={'color': 'white'}),
                end_month_dropdown
            ]), width=2),
            dbc.Col(width=1.3),
        ], justify="center"),
        html.Hr(style={'borderTop': '1px solid white'}),
        # Cards with default background from CSS
        dbc.Card([
            dbc.CardHeader("Worldwide Comparison", className="font-weight-bold"),
            dbc.CardBody([
                dbc.Row([dbc.Col(region_filter, width=3)], justify="start"),
                html.Hr(), 
                dbc.Row([
                    dbc.Col(graph_placeholder, width=8),
                    dbc.Col(top_countries_chart, width=4)
                ], justify="around"),
            ]),
        ], className="mb-3"),
        dbc.Card([
            dbc.CardHeader("Country of Interest Trend", className="font-weight-bold"),
            dbc.CardBody([
                dbc.Row([dbc.Col(country_filter, width=3)], justify="start"),
                html.Hr(),  
                dbc.Row([
                    dbc.Col(trend_chart, width=4),
                    dbc.Col(data_summary, width=4),
                ], justify="around"),
            ]),
        ], className="mb-3"),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P("This dashboard visualizes global air pollution levels, making it easy to explore global and local trends",
                        style={"font-size": "16px", 'color': 'white'}),
                    html.P("Creators: Merete Lutz, Kun Ya, Weiran Zhao, Sid Grover",
                        style={"font-size": "12px", 'color': 'white'}),
                    html.A("GitHub Repository", href="https://github.com/UBC-MDS/DSCI-532_2024_2_pollution-tracker",
                        target="_blank", style={"font-size": "12px", 'color': '#00BFFF'}),
                    html.P("Last updated on April 7, 2024",
                        style={"font-size": "12px", 'color': 'white'}),
                ])
            ], width=12),
        ]),
        html.Div(id='dummy_output'),
        dcc.Store(id='selected-countries', data=[]),
        html.Div(id='first_country_name', style={'display': 'none'})
    ])


    return layout
