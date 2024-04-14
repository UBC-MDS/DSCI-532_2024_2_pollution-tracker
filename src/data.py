import pandas as pd

def load_data():
    data = pd.read_csv("data/processed/world_air_quality.csv")
    data['time_hour'] = pd.to_datetime(data['time_hour']).dt.tz_convert(None)
    data['time'] = pd.to_datetime(data['time']).dt.date
    return data
