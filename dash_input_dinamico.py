import dash
import plotly.express as px
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output, State


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='input1',type='text', value='*'),
    dcc.Input(id='input2',type='text', value='*'),
    html.Button(id='btn',children='Submit'),
    html.Div(id='number')
])

@app.callback(Output('number','children'),[Input('btn','n_clicks'),State('input1','value'),State('input2','value')])
def att(nclick,input1,input2):
    return f'Tua {input1} é uma {input2}'


if __name__ == "__main__":
    app.run_server(debug=True)