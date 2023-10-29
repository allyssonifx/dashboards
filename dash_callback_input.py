import dash
import plotly.express as px
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output, State


ex_style = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=ex_style)

app.layout = html.Div([
    html.H6('Pombo Da Holanda'),
    html.Div([
        dcc.Input(id='input',value='Valor inicial',type='text')]),
    html.Br(),
    html.Div(id='output')
])

@app.callback(Output(component_id='output',component_property='children'),[Input(component_id='input',component_property='value')])
def update(value):
    return f"saída {value}"

if __name__ == '__main__':
    app.run_server(debug=True)