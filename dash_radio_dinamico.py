import dash
import plotly.express as px
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output, State


app = dash.Dash(__name__)

opcoes = {
    'USA':{'Liberty City','San Fierro','Las Venturas'},
    'Brasa':{'January River','San Paul','Chirstmas'}
}

app.layout = html.Div([
    dcc.RadioItems(
        list(opcoes.keys()),
        'USA',
        id='paises'
    ),
    html.Hr(),
    dcc.RadioItems(id='cidades'),
    html.Hr(),
    html.Div(id='display')
])

@app.callback(Output('cidades','options'),[Input('paises','value')])
def set_city_op(pais):
    return [{'label':i,'value':i} for i in opcoes[pais]]

@app.callback(Output('cidades','value'),Input('cidades','options'))
def set_city_v(op):
    return op[0]['value']

@app.callback(Output('display','children'),[Input('paises','value'),Input('cidades','value')])
def display(paises,cidades):
    return f'{cidades} fica em {paises}'

if __name__ == '__main__':
    app.run_server(debug=True)