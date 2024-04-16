import pandas as pd

def load_data():
    data = pd.read_parquet('../data/processed/world_air_quality.parquet')
    # data['time_hour'] = pd.to_datetime(data['time_hour']).dt.tz_convert(None)
    # data['time'] = pd.to_datetime(data['time']).dt.date
    return data

