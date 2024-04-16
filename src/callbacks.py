import pandas as pd
import plotly.express as px
import altair as alt
alt.data_transformers.enable("vegafusion")
from dash.dependencies import Input, Output, State
import json

def register_callbacks(app, data):
    # Update country options based on filters
    @app.callback(
        Output('country_filter', 'options'),
        [
            Input('pollutant_type_filter', 'value'),
            Input("start_year", "value"),
            Input("start_month", "value"),
            Input("end_year", "value"),
            Input("end_month", "value"),
            Input("region_filter", "value"),
        ]
    )
    def update_country_options(selected_pollutant, start_year, start_month, end_year, end_month, regions):
        start_date_str = f"{start_year}-{start_month:02d}"
        end_date_str = f"{end_year}-{end_month:02d}"
        start_date = pd.to_datetime(start_date_str).date()
        end_date = pd.to_datetime(end_date_str).date()

        filtered_data = data[
            (data['pollutant'] == selected_pollutant) &
            (data['time'] >= start_date) &
            (data['time'] <= end_date)
        ]

        if regions:
            filtered_data = filtered_data[filtered_data['continent'].isin(regions)]

        unique_countries = filtered_data['countryname'].unique()
        return [{'label': country, 'value': country} for country in unique_countries]

    @app.callback(
        Output('region_filter', 'options'),
        [
        Input('pollutant_type_filter', 'value'),
        Input("start_year", "value"),
        Input("start_month", "value"),
        Input("end_year", "value"),
        Input("end_month", "value"),
        ]
    )
    def update_region_options(selected_pollutant, start_year, start_month, end_year, end_month):
        start_date_str = f"{start_year}-{start_month:02d}"
        end_date_str = f"{end_year}-{end_month:02d}"
        start_date = pd.to_datetime(start_date_str).date()
        end_date = pd.to_datetime(end_date_str).date()

        filtered_data = data[
            (data['pollutant'] == selected_pollutant) &
            (data['time'] >= start_date) &
            (data['time'] <= end_date)
        ]

        unique_continent = filtered_data['continent'].unique()
        return [{'label': continent, 'value': continent} for continent in unique_continent]

    @app.callback(
        Output('country_filter', 'value'),
        [Input('first_country_name', 'children')]
    )
    def set_country_filter_default(first_country):
        return first_country
    
    @app.callback(
        Output("collapse", "is_open"),
        Input("collapse-button", "n_clicks"),
        State("collapse", "is_open"),  # Pass the current "state" of the component (is it open or not)
    )
    def toggle_collapse(n, is_open):
        print(n)  # The number of times the button has been clicked
        print(is_open)  # Whether the collapse is open or not
        return not is_open if n else is_open

    # Display choropleth map based on selections
    @app.callback(
        Output("graph", "figure"), 
        Input("pollutant_type_filter", "value"),
        Input("region_filter", "value"),
        Input("start_year", "value"),
        Input("start_month", "value"),
        Input("end_year", "value"),
        Input("end_month", "value"),
        State('selected-countries', 'data')
    )
    
    def display_choropleth(selected_pollutant, regions, start_year, start_month, end_year, end_month, selected_countries):
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

        with open("../data/raw/custom.geo.json", "r", encoding="utf-8") as f:
            countries_geojson = json.load(f)
        
        df = data
        filtered_data = data[
            (data['pollutant'] == selected_pollutant) &
            (data['time'] >= start_date) &
            (data['time'] <= end_date)
        ]

        if regions:
            filtered_data = filtered_data[filtered_data['continent'].isin(regions)]

        aggregated_data = filtered_data.groupby('countryname')['AQI_cat'].agg(lambda x: pd.Series.mode(x)[0]).reset_index()
        
        category_color_scale = dict([
            ('Good', '#98FB98'),  # Pale Green
            ('Moderate', '#FFFF99'),  # Light Yellow
            ('Unhealthy for Sensitive Groups', '#FFD700'),  # Gold
            ('Unhealthy', '#FFA500'),  # Orange
            ('Very Unhealthy', '#FF6347'),  # Tomato Red
            ('Hazardous', '#B22222')  # Firebrick Red
        ])
        
        map = px.choropleth(
            aggregated_data,
            geojson=countries_geojson,
            locations='countryname',
            color='AQI_cat',
            featureidkey="properties.admin",
            color_discrete_map=category_color_scale 
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
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            clickmode='event+select'
        )

        for trace in map.data:
            if any(loc in selected_countries for loc in trace.locations):
                trace.marker.line.width = 2
                trace.marker.line.color = 'silver'
            else:
                trace.marker.line.width = 0

        return map

    @app.callback(
        Output('selected-countries', 'data'),
        [Input('graph', 'clickData')],
        [State('selected-countries', 'data')]
    )
    def update_selected_countries(clickData, selected_countries):
        if clickData:
            country_name = clickData['points'][0]['location']
            if country_name in selected_countries:
                selected_countries.remove(country_name)
            else:
                selected_countries.append(country_name)
        return selected_countries

    # Update top countries chart
    @app.callback(
        Output("top_countries_chart", "spec"),
        Output("first_country_name", "children"),
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

        aggregated_data = filtered_data.groupby('countryname').agg(
            mean_value=pd.NamedAgg(column='value', aggfunc='mean'),
            most_frequent_cat=pd.NamedAgg(column='AQI_cat', aggfunc=lambda x: pd.Series.mode(x).iloc[0])
        ).reset_index()
        
        aggregated_data = aggregated_data.sort_values(by='mean_value', ascending=False).head(15)
        
        category_color_scale = dict([
            ('Good', '#98FB98'),  # Pale Green
            ('Moderate', '#FFFF99'),  # Light Yellow
            ('Unhealthy for Sensitive Groups', '#FFD700'),  # Gold
            ('Unhealthy', '#FFA500'),  # Orange
            ('Very Unhealthy', '#FF6347'),  # Tomato Red
            ('Hazardous', '#B22222')  # Firebrick Red
        ])

        bar = alt.Chart(aggregated_data).mark_bar().encode(
            x=alt.X('mean_value:Q', title='Average AQI Value'),
            y=alt.Y('countryname:N', title='Country', sort='-x'),
            fill=alt.Color('most_frequent_cat:N', scale=alt.Scale(domain=list(category_color_scale.keys()), range=list(category_color_scale.values())), legend=None),
            tooltip=[
                alt.Tooltip('countryname:N', title='Country'),
                alt.Tooltip('mean_value:Q', title='AQI value'),
                alt.Tooltip('most_frequent_cat:N', title='AQI category')
            ]
        ).properties(
            width=250,
            height=370
        ).to_dict(format='vega')

        if not aggregated_data.empty:
            first_country = aggregated_data.iloc[0]['countryname']
        else:
            first_country = None
        
        return bar, first_country
    
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
            #(data['countryname'].isin(countries)) &
            (data['pollutant'] == pollutant)
        ]
        if countries:
            if not isinstance(countries, list):
                countries = [countries]
            filtered_data = filtered_data[data['countryname'].isin(countries)]
        
        filtered_data['time'] = filtered_data['time'].astype(str)
        
        circles = alt.Chart(filtered_data).mark_circle(
            opacity=0.3
            ).encode(
                x=alt.X('time_hour:T', axis=alt.Axis(title='Date', format='%Y-%m')), 
                y=alt.Y('AQI:Q', axis=alt.Axis(title='AQI Value')),  
                color=alt.Color('countryname:N', legend=alt.Legend(title='Country')),
                tooltip=[
                alt.Tooltip('time_hour:T', title='Date', format='%Y-%m-%d'),
                alt.Tooltip('AQI:Q', title='AQI Value'),
                alt.Tooltip('countryname:N', title='Country')
                ]
            ).properties(
                title='Air Quality Index (AQI) Over Time',
                width=500,
                height=300
            )
        
        circles_line = circles + circles.mark_line(size=3).transform_regression(
                'time_hour',
                'AQI',
                groupby=['countryname']
            )

        return circles_line.to_dict(format='vega')

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
            #(data['countryname'].isin(countries)) &
            (data['pollutant'] == pollutant)
        ]
        
        if countries:
            if not isinstance(countries, list):
                countries = [countries]
            filtered_data = filtered_data[data['countryname'].isin(countries)]
        
        country_stats = {}

        for country in filtered_data['countryname'].unique():
            country_data = filtered_data[filtered_data['countryname'] == country]['value']
            min_value = round(country_data.min(), 2)
            avg_value = round(country_data.mean(), 2)
            max_value = round(country_data.max(), 2)
            unit_meas = filtered_data[filtered_data['countryname'] == country]['unit'].iloc[0]
            num_obs = country_data.shape[0]
            pol_type = filtered_data[filtered_data['countryname'] == country]['pollutant'].iloc[0]
            
            country_stats[country] = {
                'Country': country,
                'Pollutant': pol_type,
                'Unit of Measurement': unit_meas,
                'Minimum': min_value, 
                'Average': avg_value, 
                'Maximum ': max_value,
                'No. of Observations': num_obs
                }
        
        table = (pd.DataFrame
                .from_dict(country_stats, orient='index')
                .T
                .reset_index()
                .rename(columns={'index': ''})
                .tail(6)
                )

        columns = [{"name": i, "id": i} for i in table.columns]
        summary_data = table.to_dict('records')

        return columns, summary_data
