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

def get_layout(data):
    pollutant_filter, region_filter, country_filter = get_filters(data)
    start_year_dropdown, start_month_dropdown, end_year_dropdown, end_month_dropdown = get_datepickers()

    layout = html.Div([
        dbc.Row(html.H1('Pollutant Tracker'), justify="center"),
        dbc.Row(pollutant_filter, justify="center"),
        dbc.Row([
            dbc.Col(region_filter, width=4),
            dbc.Col(country_filter, width=4),
            dbc.Col(html.Div([
                dbc.Row([
                    dbc.Col(html.Div('Start Year:'), width=3),
                    dbc.Col(start_year_dropdown, width=9)
                ]),
                dbc.Row([
                    dbc.Col(html.Div('Start Month:'), width=3),
                    dbc.Col(start_month_dropdown, width=9)
                ]),
                dbc.Row([
                    dbc.Col(html.Div('End Year:'), width=3),
                    dbc.Col(end_year_dropdown, width=9)
                ]),
                dbc.Row([
                    dbc.Col(html.Div('End Month:'), width=3),
                    dbc.Col(end_month_dropdown, width=9)
                ])
            ], width=4))
        ], justify="center"),
        html.Hr(),
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(id='graph'),
                dvc.Vega(id='top_countries_chart', opt={"renderer": "svg", "actions": False}, spec={}, style={'width': '100%', 'height': '100%'}),
                dash_table.DataTable(id='data-summary-table', style_cell={'textAlign': 'center'}, style_header={'backgroundColor': 'white', 'fontWeight': 'bold'})
            ])
        ])
    ])

    return layout
