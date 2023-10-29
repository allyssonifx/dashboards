import dash
import plotly.express as px
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output, State


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

ex_style = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=ex_style)

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Slider(
        id='ano',min=df['year'].min(),max=df['year'].max(),value=df['year'].min(),marks={str(year):str(year) for year in df['year'].unique()},step=None
    )
])

@app.callback(Output('graph','figure'),[Input('ano','value')])
def update(ano):
    dfnovo = df[df.year ==ano]
    fig = px.scatter(dfnovo,x='gdpPercap',y='lifeExp',size='pop',color='continent',hover_name='country',log_x=True,size_max=55)

    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)