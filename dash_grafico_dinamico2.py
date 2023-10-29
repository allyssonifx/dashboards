import dash
import plotly.express as px
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output, State


df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

indica = df['Indicator Name'].unique()

ex_style = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=ex_style)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(id='columnx',options=[{'label':i,'value':i} for i in indica],value='Ferility'),
            dcc.RadioItems(id='typex',options=[{'label':i,'value':i} for i in ['Linear','Log']],value='Linear',labelStyle={'display':'inline-block'})
        ],style={'width':'48%','display':'inline-block'}),
        html.Div([
            dcc.Dropdown(id='columny',options=[{'label':i,'value':i} for i in indica],value='Ferility'),
            dcc.RadioItems(id='typey',options=[{'label':i,'value':i} for i in ['Linear','Log']],value='Linear',labelStyle={'display':'inline-block'})
        ],style={'width':'48%','display':'inline-block','float':'right'}),
    ]),
    dcc.Graph(id='graph'),
    dcc.Slider(id='slider',min=df['Year'].min(),max=df['Year'].max(),value=df['Year'].min(),marks={str(year):str(year) for year in df['Year'].unique()},step=None)
])

@app.callback(Output('graph','figure'),[Input('columnx','value'),Input('typex','value'),Input('columny','value'),Input('typey','value'),Input('slider','value')])
def update(columnx,columny,typex,typey,ano):
    dfnovo = df[df['Year'] ==ano]
    dfx = dfnovo[dfnovo['Indicator Name'] == columnx]['Value']
    dfy = dfnovo[dfnovo['Indicator Name']==columny]['Value']
    print(list(dfx['Value']))
    fig = px.scatter(x=list(dfx.Value),y=list(dfy.Value),hover_name=dfy['Country Name'])
#     fig = px.scatter(
#     dfnovo[dfnovo['Indicator Name'] == columnx],
#     x='Value',
#     y='Value',
#     hover_name=dfnovo[dfnovo['Indicator Name'] == columny]['Country Name']
# )

    fig.update_layout(margin={'l':40,'b':40,'t':40,'r':0},hovermode='closest')

    fig.update_xaxes(title=columnx,type='linear' if typex == 'Linear' else 'log')

    fig.update_yaxes(title=columny,type='linear' if typey == 'Linear' else 'log')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)