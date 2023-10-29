from dash import html, dcc
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_auth
from app import *
from dash_bootstrap_templates import load_figure_template
load_figure_template(['quartz'])

card_style = {
    'width':'800px',
    'min-height' :'300px',
    'padding-top':'25px',
    'padding-right':'25px',
    'padding-left':'25px',
    'align-self':'center'
}

df = pd.DataFrame(np.random.randn(100,1),columns=['data'])
fig = px.line(df, x=df.index,y='data',template='quartz')

def render_layout(user):
    login = dbc.Card([
                    dcc.Location(id='data'),
                    html.Legend(f'ola{user}'),
                    dcc.Graph(figure=fig),
                    html.Div([
                        dbc.Button('Sair',id='btn-logout')
                    ],style={'padding':'20px','justify-content':'end','display':'flex'})
                ],style=card_style,className='aling-self-center')

    return login