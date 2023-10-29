import dash
import plotly.express as px
import pandas as pd
from dash import html, dcc

app = dash.Dash(__name__)


app.layout = html.Div([
    html.Label("Dropdown"),
    dcc.Dropdown(id="dp-1",
                 options=[{'label':'Rio Grande do Sul','value':'RS'},
                        {'label':'Pernambuco','value':'PE'},
                        {'label':'Minas Gerais','value':'MG'}],
                value="RS",style={"margin-bottom":"20px"}),
    html.Label("cHEK"),
    dcc.Checklist(id="ck-1",
                 options=[{'label':'Rio Grande do Sul','value':'RS'},
                        {'label':'Pernambuco','value':'PE'},
                        {'label':'Minas Gerais','value':'MG'}],
                value=["PE"],style={"margin-bottom":"20px"}),
    html.Label("Input"),
    dcc.Input(value="",type='text'),
    html.Label("Slider"),
    dcc.Slider(min=0,max=10,marks={i:'Macaiba'.format(i) if i == 2 else str(i) for i in range(0,11)},value=2)

    
])


if __name__ == '__main__':
    app.run_server(debug=True)