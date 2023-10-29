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

card_style = {
    'width':'300px',
    'min-height' :'300px',
    'padding-top':'25px',
    'padding-right':'25px',
    'padding-left':'25px',
    'align-self':'center'
}

def render_layout():
    login = dbc.Card([
        html.Legend("Login"),
        dbc.Input(id='user',placeholder='Usuários',type='text'),
        dbc.Input(id='pass',placeholder='Senha',type='password'),
        dbc.Button('Entrar',id='btn-login'),
        html.Span('',style={'text-aling':'center'}),
        html.Div([
            html.Label('Ou',style={'margin-right':'5px'}),
            dcc.Link('Registre-se',href='/register')
        ],style={'padding':'20px','justify-content':'center','display':'flex'})

    ],style=card_style)
    return login