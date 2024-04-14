import pandas as pd
import plotly.express as px
import altair as alt
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

    # Display choropleth map based on selections
    @app.callback(
        Output("graph", "figure"), 
        [
            Input("pollutant_type_filter", "value"),
            Input("region_filter", "value"),
            Input("start_year", "value"),
            Input("start_month", "value"),
            Input("end_year", "value"),
            Input("end_month", "value")
        ]
    )
    def display_choropleth(selected_pollutant, regions, start_year, start_month, end_year, end_month):
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

        aggregated_data = filtered_data.groupby('countryname')['value'].mean().reset_index()
        
        fig = px.choropleth(
            aggregated_data,
            locations='countryname',
            color='value',
            hover_name='countryname',
            color_continuous_scale=px.colors.sequential.Plasma
        )

        return fig

    # Update data summary table
    @app.callback(
        [Output('data-summary-table', 'columns'), Output('data-summary-table', 'data')],
        [Input("pollutant_type_filter", "value"), Input("country_filter", "value"),
         Input("start_year", "value"), Input("start_month", "value"),
         Input("end_year", "value"), Input("end_month", "value")]
    )
    def update_data_summary(pollutant, countries, start_year, start_month, end_year, end_month):
        start_date_str = f"{start_year}-{start_month:02d}"
        end_date_str = f"{end_year}-{end_month:02d}"
        start_date = pd.to_datetime(start_date_str).date()
        end_date = pd.to_datetime(end_date_str).date()

        filtered_data = data[
            (data['time'] >= start_date) &
            (data['time'] <= end_date) &
            (data['pollutant'] == pollutant)
        ]

        if countries:
            filtered_data = filtered_data[filtered_data['countryname'].isin(countries)]

        summary = filtered_data.groupby('countryname').agg(
            Min_AQI=('value', 'min'),
            Max_AQI=('value', 'max'),
            Avg_AQI=('value', 'mean')
        ).reset_index()

        columns = [{"name": i, "id": i} for i in summary.columns]
        data = summary.to_dict('records')

        return columns, data

    # Update top countries chart
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
    def update_top_countries_chart(pollutant, start_year, start_month, end_year, end_month, regions):
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

        top_countries_data = filtered_data.groupby('countryname')['value'].mean().sort_values(ascending=False).head(10).reset_index()

        bar_chart = alt.Chart(top_countries_data).mark_bar().encode(
            x='value:Q',
            y=alt.Y('countryname:N', sort='-x')
        ).properties(
            width=600,
            height=400
        )

        return bar_chart.to_dict()
