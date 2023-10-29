from dash import html, dcc
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from werkzeug.security import generate_password_hash
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
    register = dbc.Card([
                html.Legend("Login"), 
                dbc.Input(id='user',placeholder='Usuários',type='text'),
                dbc.Input(id='pass',placeholder='Senha',type='password'),
                dbc.Input(id='email',placeholder='E-mail',type='email'),
                dbc.Button('Registrar',id='btn-register'),
                html.Span('',style={'text-aling':'center'}),
                html.Div([
                    html.Label('Ou',style={'margin-right':'5px'}),
                    dcc.Link('faça Login',href='/login')
                ],style={'padding':'20px','justify-content':'center','display':'flex'})

    ],style=card_style)
    return register

@app.callback(Output('register-state','data'),Input('btn-register','n_clicks'),[State('user','value'),State('pass','value'),State('email','value')])
def register(clicks,username,password,email):
    print(clicks)
    if clicks:
        if None  not in [username,password,email]:
            # hashed = generate_password_hash(password, method='sha256')
            # ins = users_table.insert().values(username=username,password=hashed,email=email)
            # conn = engine.connect()
            # conn.execute(ins)
            # conn.close()
            return ''
        else:
            return 'erro'
