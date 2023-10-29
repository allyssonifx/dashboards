import dash
import plotly.express as px
import pandas as pd
from dash import html, dcc


ex_style = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=ex_style)

df = pd.DataFrame({'frutinha':['caju','mamão','laranjapocã','axaxaio'],"quantidade":[2,3,30,12],'cidade':['pombos','gravatá','caruaru','garanhuns']})

fig = px.bar(df,x='frutinha',y='quantidade',color='cidade')
 
app.layout = html.Div(id="Div1",
    children=[
        html.H1("Hello pessoal",id="h1",style={"color":"#FF02F2"}),
        html.Div("Bolando no python hehhe"),
        dcc.Graph(figure=fig,id="graph")
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)