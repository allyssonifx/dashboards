import time
import dash
import json
import folium
import numpy as np
import pandas as pd
import geopandas as gpd
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output, State

gdf = gpd.read_file(r'dados\shapes_brasil\brasil\estados_2010.shp')
gdf.rename(columns={'sigla':'uf'},inplace=True)
data_dic ={'DC':pd.read_csv(r'dados\csv_area_estado\deter_cerrado.csv'),'DA':pd.read_csv(r'dados\csv_area_estado\deter_amazonia.csv'),'PC':pd.read_csv(r'dados\csv_area_estado\prodes_cer.csv'),'PA':pd.read_csv(r'dados\csv_area_estado\prodes_amz.csv'),'DM':pd.read_csv(r'dados\csv_area_estado\desmatamento_mapbiomas.csv')}
class DataFrames:
    def __init__(self):
        self.dfnovo = pd.DataFrame(({'ano':[],'uf':[],'area':[]}))
        self.df = pd.DataFrame({'ano':[],'uf':[],'area':[]})
        self.time = True
    def set_df(self,dfn):
        self.df = dfn

    def get_df(self,):
        return self.df

    def set_dfnovo(self,dfn):
        self.dfnovo = dfn

    def get_dfnovo(self,):
        return self.dfnovo
    
datas = DataFrames()

def data_config(check):
    df = pd.DataFrame({'ano':[],'uf':[],'area':[]})
    ck = check
    print(ck)
    for c in check:
        df = pd.concat([df,data_dic[c]])
    return df

def gerar_mapa(df):

    m = folium.Map(location=[-15.788497, -47.879873],zoom_start=4,tiles='CartoDB positron')
    merged_df = pd.merge(gdf, df, on='uf', how='outer')
    maior = merged_df['area'].max()

    maior80 = round((maior*0.8) / 100) * 100
    maior60 = round((maior*0.6) / 100) * 100 
    maior40 = round((maior*0.4) / 100) * 100
    maior20 = round((maior*0.2) / 100) * 100

    geo3 = merged_df.to_json()

    folium.Choropleth(
    geo_data=geo3,
    data=merged_df,
    columns=("uf", "area"),
    key_on="feature.properties.uf",
    bins=[0,maior20,maior40,maior60,maior80,maior],
    fill_color="RdYlGn_r",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="white",
    legend_name="Quantidade de hectares desmatado",
    ).add_to(m)
    #gjson = json.loads(geo3)

    # tempo = time.time()
    # for feature in gjson['features']:
    #     area = feature['properties']['area']
    #     estado = feature['properties']['uf']
    #     if str(area) == 'None':
    #         texto = 'Sem informações'
    #     else:
    #         texto = f'Estado : {estado} \n Area desmatada (ha) : {area:,.2f}'.replace('.','/').replace(',','.').replace('/',',')
    
    #     popup = folium.Popup(texto)
    #     folium.GeoJson(feature, popup=popup, style_function=lambda x: {'color': 'transparent', 'fillColor': 'transparent'}).add_to(m)

    return m


#,min=df['ano'].min(),max=df['ano'].max(),value=df['ano'].min(),marks={str(ano):str(ano) for ano in df['ano'].unique()},step=None
  

#indica = df['Indicator Name'].unique()

ex_style = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=ex_style)

app.layout = html.Div([
    html.Div(
        children=[
       dcc.Checklist(id="ck",
                 options=[{'label':'DETER Cerrado','value':'DC'},
                        {'label':'DETER Amazônia','value':'DA'},
                        {'label':'PRODES Cerrado','value':'PC'},
                        {'label':'PRODES Amazônia','value':'PA'},
                        {'label':'Dematamento Mapbiomas','value':'DM'}],
                value=["DC"],style={
    "margin-bottom": "20px",
    "margin-left": "20px",
    "margin-right": "20px",
    "display": "flex",
    "flex-wrap": "wrap",
    "width": "95%",
    "gap": "10px",
    "justify-content": "space-between",
    "font-family": "Arial, sans-serif"
}
),
    # dcc.Slider(
    #     id='ano') 
    dcc.RadioItems(id='ano',style={
    "margin-bottom": "20px",
    "margin-left": "20px",
    "margin-right": "20px",
    "display": "flex",
    "flex-wrap": "wrap",
    "width": "95%",
    "gap": "10px",
    "justify-content": "space-between",
    "font-family": "Arial, sans-serif"
}),
    ],
    style={
        'backgroundColor': 'white','margin-bottom':'10px'
    }
    ),
    
    dcc.Graph(id='graph'),
    html.Button(id='btn',children='Submit'),
    html.Iframe(width='100%', height='600px',id='html')
    #dcc.Graph(id='map', config={'displayModeBar': False})
    
    
])

#@app.callback([Output('ano','min'),Output('ano','max'),Output('ano','value'),Output('ano','marks'),Output('ano','step')],[Input('ck','value')])
@app.callback([Output('ano','options'),Output('ano','value')],[Input('ck','value'),State('ano','value')])
def slide(check,ano):
    df = data_config(check)
    datas.set_df(df)
    if ano in df['ano'].unique():
        valor = ano
    else:
        valor = df['ano'].max()
    df = df.sort_values('ano')
    return [{'label':i,'value':i} for i in df['ano'].unique()],valor
    

@app.callback(Output('graph','figure'),[Input('ano','value')])
def update(ano):
    df = datas.get_df()
    dfnovo = df[df.ano ==ano].sort_values('uf')
    datas.set_dfnovo(dfnovo)
    fig = px.bar(dfnovo,x='uf',y='area',color='uf',hover_name='uf', color_continuous_scale='greens')
    fig.update_layout(transition_duration=500)#template='plotly_dark'
    
    return fig

@app.callback(Output('html','srcDoc'),Input('ano','value'))
def mapa(click):
    if datas.time:
        time.sleep(5)
        datas.time = False
    if click:
        df = datas.get_dfnovo()
        tempo = time.time()
        map = gerar_mapa(df.groupby(["uf"])['area'].apply(np.sum))
        print(time.time()-tempo)
        tempo = time.time()
        html = map.get_root().render()
        print(time.time()-tempo)
        return html
    else:
        return '<p>mapa</p>'


if __name__ == '__main__':
    app.run_server(debug=True)

