from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import dash_table

def get_filters(data):
    pollutant_filter = html.Div([
        html.Label('Select pollutant:'),
        dcc.RadioItems(
            id='pollutant_type_filter',
            options=[{'label': i, 'value': i} for i in ['PM2.5', 'PM10', 'CO', 'SO2', 'NO2', 'O3']],
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
        value=years[0],
        style={
        'color': '#333333',  # Dark text color
        'borderColor': '#333333'  # Dark border color
    }
    )

    start_month_dropdown = dcc.Dropdown(
        id='start_month',
        options=[{'label': month, 'value': i+1} for i, month in enumerate(month_names)],
        value=1,
        style={
        'color': '#333333',  # Dark text color
        'borderColor': '#333333'  # Dark border color
    }
    )

    end_year_dropdown = dcc.Dropdown(
        id='end_year',
        options=[{'label': year, 'value': year} for year in years],
        value=years[-1],
        style={
        'color': '#333333',  # Dark text color
        'borderColor': '#333333'  # Dark border color
    }
    )

    end_month_dropdown = dcc.Dropdown(
        id='end_month',
        options=[{'label': month, 'value': i+1} for i, month in enumerate(month_names)],
        value=12,
        style={
        'color': '#333333',  # Dark text color
        'borderColor': '#333333'  # Dark border color
    }
    )

    return start_year_dropdown, start_month_dropdown, end_year_dropdown, end_month_dropdown

collapse_button = dbc.Button(
    "Learn more",
    id="collapse-button",
    outline=False,
    style={
        'width': '150px',
        'background-color': 'white',
        'color': '#333333',
        'margin-top': 10,
        'border-color': 'gray'
    }
)

collapse_section = dbc.Collapse(
    dbc.Container([
         html.P(
            [
                html.Strong("Air Quality Index (AQI)"),
                " is an indicator of air quality developed by government health authorities to communicate the level of air pollution in an area. "
                "When AQI levels are high, several subgroups are affected by its negative impacts - children, seniors, and those with respiratory and cardiorespiratory illnesses. "
                "In times of high AQI, health bodies suggest people stay indoors, use high-efficiency particulate absorbing (HEPA) filters, wear NIOSH N95, and avoid any risk to their health.",
            ],
            style={'color': 'white'}
        ),
        html.P(
            [
                "For more information, please ",
                html.A("visit here", href="https://github.com/UBC-MDS/DSCI-532_2024_2_pollution-tracker", target="_blank"),
                "."
            ],
            style={'color': 'white'}
        ),
        html.P(
            [
                html.Strong("PM2.5 (Particulate Matter 2.5):"),
                " PM2.5 refers to fine particulate matter that is less than 2.5 micrometers in diameter. "
                "These tiny particles can penetrate deep into the respiratory system, entering the lungs and even the bloodstream, causing a variety of health problems. "
                "Sources include vehicle emissions, industrial processes, and natural sources like wildfires."
            ],
            style={'color': 'white'}
        ),
        html.P(
            [
                html.Strong("NO (Nitric Oxide):"),
                " Nitric oxide is a colorless gas that is a by-product of combustion processes, particularly at high temperatures found in car engines and power plants. "
                "While not directly harmful, NO rapidly transforms into nitrogen dioxide (NO2) in the atmosphere, which is a major air pollutant and contributes to the formation of smog and acid rain."
            ],
            style={'color': 'white'}
        ),
        html.P(
            [
                html.Strong("CO (Carbon Monoxide):"),
                " Carbon monoxide is a colorless, odorless gas produced by the incomplete combustion of carbon-containing fuels. "
                "It is particularly dangerous in enclosed spaces, as it can interfere with the blood's ability to carry oxygen, leading to serious health effects like headaches, dizziness, and even death at high concentrations."
            ],
            style={'color': 'white'}
        ),
        html.P(
            [
                html.Strong("NOx (Nitrogen Oxides):"),
                " NOx is a collective term for nitrogen oxides, including NO and NO2. These gases are mainly produced from vehicle emissions and industrial activities. "
                "NOx gases are contributors to environmental issues such as smog, acid rain, and can exacerbate respiratory diseases such as asthma by irritating the airways."
            ],
            style={'color': 'white'}
        ),
        html.P(
            [
                html.Strong("PM10 (Particulate Matter 10):"),
                " PM10 includes particles that are 10 micrometers or smaller in diameter. "
                "These particles are smaller than the thickness of a human hair and can be inhaled into the respiratory tract. "
                "Sources of PM10 include dust from roads, construction sites, and other similar sources of fine particles."
            ],
            style={'color': 'white'}
        ),
    ], fluid=True),
    id="collapse",
    style={'width': '70%', 'margin': 'auto'}  # Adjust width and centering
)

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
        dbc.Row([
        dbc.Col(html.H1('Pollution Tracker', className='text-center my-4'), width=6),
        dbc.Col(collapse_button,md=3)
        ], justify='end', align='center', className='my-4 g-0',  # No gutters
    ),
        dbc.Row(pollutant_filter, justify="center", style={'color': 'white'}),
        dbc.Row([
            dbc.Col(html.Div([
                html.Label('Start Year:', style={'color': 'white'}),
                start_year_dropdown
            ]), width=2),
            dbc.Col(html.Div([
                html.Label('Start Month:', style={'color': 'white'}),
                start_month_dropdown
            ]), width=2),
            dbc.Col(html.Div([
                html.Label('End Year:', style={'color': 'white'}),
                end_year_dropdown
            ]), width=2),
            dbc.Col(html.Div([
                html.Label('End Month:', style={'color': 'white'}),
                end_month_dropdown
            ]), width=2),
        ], justify="center"),
        html.Hr(style={'borderTop': '1px solid white'}),
        dbc.Row(collapse_section, style={'color': 'white'}),
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
