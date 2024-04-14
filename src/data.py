import pandas as pd
import json

def load_geojson():
    with open("path/to/your/custom.geo.json", "r") as file:
        geojson = json.load(file)
    return geojson

def load_data():
    data = pd.read_csv("data/processed/world_air_quality.csv")
    data['time_hour'] = pd.to_datetime(data['time_hour']).dt.tz_convert(None)
    data['time'] = pd.to_datetime(data['time']).dt.date
    return data, load_geojson()

