from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app


style_sidebar = style={"box-shadow": "2px 2px 10px 0px rgba(10, 9, 7, 0.10)",
                    "margin": "10px",
                    "padding": "10px",
                    "height": "100vh"}

# =========  Layout  =========== #
layout = dbc.Card(
    [
        html.H2("SIRIUS", style={'font-family': 'Voltaire', 'font-size': '40px'}),
        html.Hr(), 
        dbc.Nav(
            [
                dbc.NavLink("Page1", href="/", active="exact"),
                dbc.NavLink("Page2", href="/page2", active="exact"),
            ])
    ], style=style_sidebar
)

