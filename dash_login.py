from dash import html, dcc
import dash_bootstrap_components as dbc
import dash
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_auth
from dash_bootstrap_templates import load_figure_template

load_figure_template(['quartz'])

user = {'pedrin':'1234'}

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.QUARTZ])
auth = dash_auth.BasicAuth(app,user)
server = app.server

card_style = {'width':'800px','min-height':'300px','padding':'25px','align-self':'center'}


df = pd.DataFrame(np.random.randn(100,1),columns=['data'])
fig = px.line(df,x=df.index,y='data',template='quartz')

app.layout = html.Div([
    dbc.Card([
        dcc.Graph(figure=fig)
    ],style=card_style)
])

if __name__ == '__main__':
    app.run_server(debug=True)