from dash import Dash
import dash_bootstrap_components as dbc
from data import load_data
from components import get_layout
from callbacks import register_callbacks

# Create a Dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Air Quality Tracker"

# Load data
data = load_data()

# Setup the layout using components from components.py
app.layout = get_layout(data)

# Register callbacks to manage interactivity
register_callbacks(app, data)

# Server variable for deploying with gunicorn or other WSGI servers
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
