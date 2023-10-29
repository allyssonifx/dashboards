from dash import html, dcc
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages import login, register, data

# pip install dash-auth
import dash_auth
from app import *
import webbrowser


# =========  Layout  =========== #
app.layout =  dbc.Container(children=[
                dbc.Row(children=[
                    dbc.Col([
                        dcc.Location(id='url',refresh=False),
                        dcc.Store(id='login-state',data=''),
                        dcc.Store(id='register-state',data=''),
                        html.Div(id='page',style={'height':'100vh','display':'flex','justify-content':'center'})
                    ])
                ])
])



@app.callback(Output("page","children"),Input('url','pathname'))
def loadpage(pathname):
    if pathname == '/login' or pathname == '/':
        return login.render_layout()
    elif pathname == '/register':
        return register.render_layout()
    elif pathname == '/data':
        return data.render_layout('pombo')


if __name__ == "__main__":
    webbrowser.open_new_tab('http://localhost:8050')
    app.run_server(port=8050, debug=True, use_reloader=False, threaded=True)