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
import unicodedata
from unidecode import unidecode
import plotly.graph_objects as go
import re



gdf_br = gpd.read_file(r'my_python-main\dashboards\dados\\shapes_brasil\\brasil\\br1.shp')
gdf_br.rename(columns={'sigla':'uf'},inplace=True)

data_dic ={'DC':pd.read_csv(r'my_python-main\dashboards\dados\csv_area_estado\\deter_cerrado.csv'),'DA':pd.read_csv(r'my_python-main\dashboards\dados\csv_area_estado\\deter_amazonia.csv'),'PC':pd.read_csv(r'my_python-main\dashboards\dados\csv_area_estado\\prodes_cer.csv'),'PA':pd.read_csv(r'my_python-main\dashboards\dados\csv_area_estado\\prodes_amz.csv'),'DM':pd.read_csv(r'my_python-main\dashboards\dados\csv_area_estado\\desmatamento_mapbiomas.csv')}
data_dic_mun ={'DC':pd.read_csv(r'my_python-main\dashboards\dados\csv_area_municipio\deter_cerrado_m.csv'),'DA':pd.read_csv(r'my_python-main\dashboards\dados\csv_area_municipio\deter_amazonia_m.csv'),'DM':pd.read_csv(r'my_python-main\dashboards\dados\csv_area_municipio\desmatamento_m.csv')}
coords = {'AC': [-8.77, -70.55],'AL': [-9.71, -35.73],'AM': [-3.47, -62.92],'AP': [1.41, -51.77],'BA': [-12.96, -38.51],'CE': [-3.71, -38.54],'DF': [-15.83, -47.86],'ES': [-19.19, -40.34],'GO': [-16.64, -49.31],'MA': [-2.55, -44.30],'MG': [-18.10, -44.38],'MS': [-20.51, -54.54],'MT': [-12.64, -55.42],'PA': [-5.53, -52.29],'PB': [-7.06, -35.55],'PE': [-8.28, -35.07],'PI': [-8.28, -43.68],'PR': [-24.89, -51.55],'RJ': [-22.25, -42.66],'RN': [-5.81, -36.59],'RO': [-11.22, -62.80],'RR': [1.99, -61.33],'RS': [-30.17, -53.50],'SC': [-27.45, -50.95],'SE': [-10.57, -37.45],'SP': [-22.19, -48.79],'TO': [-10.25, -48.25]}

class DataFrames:
    def __init__(self):
        self.dfnovo = pd.DataFrame(({'ano':[],'uf':[],'area':[]}))
        self.df = pd.DataFrame({'ano':[],'uf':[],'area':[]})
        self.df_mun = pd.DataFrame({'municipio':[],'ano':[],'uf':[],'area_ha':[]})
        self.data_agro = pd.read_csv(r'my_python-main\dashboards\dados\\csv_agro\\agro.csv')
        self.df_agro = pd.DataFrame()
        self.gdf_uf = gpd.GeoDataFrame()
        self.time = True



    def set_df(self,dfn):
        self.df = dfn

    def get_df(self,):
        return self.df

    def set_dfnovo(self,dfn):
        self.dfnovo = dfn

    def get_dfnovo(self,):
        return self.dfnovo
    
    def set_df_mun(self,dfn):
        self.df_mun = dfn

    def get_df_mun(self):
        return self.df_mun
    
    def set_gdf_agro(self,gdfn):
        self.gdf_agro = gdfn

    def get_gdf_agro(self):
        return self.gdf_agro
    
    def set_df_agro(self,gdfn):
        self.df_agro = gdfn

    def get_df_agro(self):
        return self.df_agro
    
    

datas = DataFrames()

def remover_caracteres_especiais(texto):
    # Normaliza a string removendo acentos e caracteres especiais
    texto_normalizado = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    # Remove os caracteres não alfanuméricos
    texto_sem_especiais = re.sub(r'[^a-zA-Z0-9\s]', '', texto_normalizado)
    return texto_sem_especiais.upper()

def data_config(check,divisor):
    df = pd.DataFrame({'municipio':[],'ano':[],'uf':[],'area_ha':[]})
    dados = {'DC':'DETER Cerrado','DA':'DETER Amazônia','PA':'PRODES Amazônia','PC':'PRODES Cerrado','DM':'Desmatamento MapBiomas'}
    ck = check
    print(ck)
    if divisor:
        for c in check:
            dftemp = data_dic[c]
            dftemp['tipo'] = dados[c]
            df = pd.concat([df,dftemp])
    else:
       for c in check:
            dftemp = data_dic_mun[c]
            dftemp['tipo'] = dados[c]
            df = pd.concat([df,dftemp]) 
    return df

def gerar_mapa(df):

    m = folium.Map(location=[-15.788497, -47.879873],zoom_start=4,tiles='CartoDB dark_matter')
    merged_df = pd.merge(gdf_br, df, on='uf', how='outer')
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
    fill_color="Reds",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="#212222",
    legend_name="Quantidade de hectares desmatado",
    ).add_to(m)


    return m

def buscar_shape(uf):
    #caminho = r'my_python-main\dashboards\dados\shapes_estados/'+uf+'/'+uf+'_Municipios_2022.shp'
    caminho = r'my_python-main\dashboards\dados\shapes_estados/'+uf+'/'+uf+'.shp'
    gdf = gpd.read_file(caminho)
    gdf.rename(columns={'MUNICIPIO':'municipio'},inplace=True)
    gdf['municipio']= gdf['municipio'].apply(remover_caracteres_especiais)
    datas.set_gdf_agro(gdf)

def gerar_mapa_mun(df,uf,var):
    gdf = datas.get_gdf_agro()
    coord = coords[uf]
    m = folium.Map(location=coord,zoom_start=6,tiles='CartoDB dark_matter')
    merged_df = pd.merge(gdf, df, on='municipio', how='outer')
    print('chegou')
    maior = merged_df[var].max()

    maior80 = round((maior*0.8))
    maior60 = round((maior*0.6))  
    maior40 = round((maior*0.4))
    maior20 = round((maior*0.2))
    print('aqui')

    geo3 = merged_df.to_json()

    folium.Choropleth(
    geo_data=geo3,
    data=merged_df,
    columns=("municipio", var),
    key_on="feature.properties.municipio",
    bins=[0,maior20,maior40,maior60,maior80,maior],
    fill_color="Reds",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="#212222",
    legend_name="Quantidade de hectares desmatado",
    ).add_to(m)
    print('chegou dnv')
    return m


ex_style = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=ex_style)

app.layout = html.Div([
    html.Div(
        children=[html.Div(children=[
            dcc.Checklist(
    id="ck",
    options=[
        {'label': 'DETER Cerrado', 'value': 'DC'},
        {'label': 'DETER Amazônia', 'value': 'DA'},
        {'label': 'PRODES Cerrado', 'value': 'PC'},
        {'label': 'PRODES Amazônia', 'value': 'PA'},
        {'label': 'Desmatamento Mapbiomas', 'value': 'DM'}
    ],
    value=["DC"],
    style={
        "margin-bottom": "20px",
        "margin-left": "20px",
        "margin-right": "20px",
        "display": "flex",
        "flex-wrap": "wrap",
        "width": "95%",
        "gap": "10px",
        "justify-content": "space-between",
        "font-family": "Arial, sans-serif",
        'backgroundcolor':"#212222"
        
    },
    labelStyle={
        "display": "inline-block",
        "background-color": '#333333',
        "border-radius": "5px",
        "margin-top": "20px",
        "padding": "5px",
        "font-family": "Arial, sans-serif",
        "color": "white",
        "cursor": "pointer"
    },
    inputStyle={
        "margin-right": "5px",
        "margin-bottom": "5px",
        "vertical-align": "middle"
    }
),

    dcc.RadioItems(id='ano',style={
                                "margin-bottom": "20px",
                                "margin-left": "20px",
                                "margin-right": "20px",
                                "display": "flex",
                                "flex-wrap": "wrap",
                                "width": "95%",
                                "gap": "10px",
                                "justify-content": "space-between",
                                "font-family": "Arial, sans-serif",
                                "color":"white"
    }),
        ],style={'backgroundColor': "#212222",'margin-bottom':'10px'}
                
        ),
       
    html.H3('ÁREA DESMATADA POR ESTADO (ha)',style={'backgroundColor': '#333333',"color":"white"}),
    html.Div(children=[
        dcc.Graph(id='graph',style={"width": "60%","backgroundColor": "#212222",'margin-right':'10px'}),
        html.Iframe(width='40%', height='400px',id='html',style={'padding': '10px'})],style={'backgroundColor': '#333333','margin-bottom':'10px','display':'flex','padding':'10px'}),
    ],
    style={
        'backgroundColor': '#333333','margin-bottom':'10px'
    }
    ),
    html.Div(children=[
        html.H3('ÁREA DESMATADA POR MUNICÍPIO (ha)',style={'backgroundColor': '#333333',"color":"white"}),
        html.Div(children=[
            html.Button(id='btn',children='GERAR MAPA'),
            dcc.RadioItems(id='mun',style={
                "margin-bottom": "20px",
                "margin-left": "20px",
                "margin-right": "20px",
                "display": "flex",
                "flex-wrap": "wrap",
                "width": "95%",
                "gap": "10px",
                "justify-content": "space-between",
                "font-family": "Arial, sans-serif",
                "color":"white"
                
            }),
        ],style={'backgroundColor': '#333333','margin-bottom':'10px','display':'flex'}),
        html.Div(children=[
        dcc.Graph(id='graph_mun',style={"width": "60%","backgroundColor": "#212222"}),
        html.Iframe(width='40%', height='400px',id='html_mun',style={'padding': '10px'})],style={'backgroundColor': '#333333','margin-bottom':'10px','display':'flex'}),
    ]),
    html.Div(children=[
        html.H3('ANÁLISE DADOS CENSO AGRO 2017',style={'backgroundColor': '#333333',"color":"white"}),
        html.Div(children=[
            html.Button(id='btn2',children='GERAR MAPA'),
            dcc.RadioItems(id='agro',options=[{'label':'Estab. Agropecuário','value':'V1'},{'label':'Área Média(ha)','value':'V2'},{'label':'Pessoal Ocupado','value':'V3'},{'label':'Ativ. Lavoura Temp.(%)','value':'V8'},{'label':'Ativ. Lavoura Perm.(%)','value':'V9'},{'label':'Pecuária (%)','value':'V10'},{'label':'Terras Pastagem (%)','value':'V17'},{'label':'Bovinos Corte (%)','value':'V20'},{'label':'Bovinos Leite (%)','value':'V21'},{'label':'Rendimento Milho (Kg/ha)','value':'V25'},{'label':'Rendimento Soja (Kg/ha)','value':'V26'},{'label':'Utilização Agrotóxicos(%)','value':'V34'},{'label':'Escolaridae até fundamental (%)','value':'V39'}],style={
                "margin-bottom": "20px",
                "margin-left": "20px",
                "margin-right": "20px",
                "display": "flex",
                "flex-wrap": "wrap",
                "width": "95%",
                "gap": "10px",
                "justify-content": "space-between",
                "font-family": "Arial, sans-serif",
                "color":"white"
                
            }),
        ],style={'backgroundColor': '#333333','margin-bottom':'10px','display':'flex'}),
        html.Div(children=[
        dcc.Graph(id='graph_agro',style={"width": "60%","backgroundColor": "#212222"}),
        html.Iframe(width='40%', height='400px',id='html_agro',style={'padding': '10px'})],style={'backgroundColor': '#333333','margin-bottom':'10px','display':'flex'}),
    ]),
    
    
  
    #dcc.Graph(id='map', config={'displayModeBar': False})
    
    
])

#@app.callback([Output('ano','min'),Output('ano','max'),Output('ano','value'),Output('ano','marks'),Output('ano','step')],[Input('ck','value')])
@app.callback([Output('ano','options'),Output('ano','value')],[Input('ck','value'),State('ano','value')])
def slide(check,ano):
    df = data_config(check,True)
    datas.set_df(df)
    if ano in df['ano'].unique():
        valor = ano
    else:
        valor = df['ano'].max()
    df = df.sort_values('ano')
    return [{'label':i,'value':i} for i in df['ano'].unique()],valor
    

@app.callback([Output('graph','figure'),Output('mun','options'),Output('mun','value')],[Input('ano','value')])
def update(ano):
    df = datas.get_df()
    dfnovo = df[df.ano ==ano].sort_values('uf')
    datas.set_dfnovo(dfnovo)
    fig = px.bar(dfnovo,x='uf',y='area',color='uf',hover_name='tipo', color_continuous_scale='greens')
    fig.update_layout(transition_duration=500,template='plotly_dark')#template='plotly_dark'
    
    return [fig,[{'label':i,'value':i} for i in dfnovo['uf'].unique()],dfnovo['uf'].iloc[0]]

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
    
@app.callback(Output('graph_mun','figure'),[Input('btn','n_clicks'),State('mun','value'),State('ck','value'),State('ano','value')])
def update2(click,uf,check,ano):
    if click:
        faltantes = ['PA','PC']
        for f in faltantes:
            if f in check:
                check.remove(f)
        df = data_config(check,False)
        dfx = df[df['uf'] == uf]
        dfy = dfx[dfx['ano'] == ano]
        datas.set_df_mun(dfy)
        fig = px.bar(dfy,x='municipio',y='area_ha',color='municipio',hover_name='municipio', color_continuous_scale='greens')
        fig.update_layout(transition_duration=500,template='plotly_dark')#template='plotly_dark'
        
        return fig
    return go.Figure()
    
@app.callback(Output('html_mun','srcDoc'),[Input('graph_mun','figure'),State('mun','value'),State('btn','n_clicks')])
def mapa(_,uf,click):
    if click:
        buscar_shape(uf)
        time.sleep(3)
        dfy = datas.get_df_mun()
        print(len(dfy))
        tempo = time.time()
        map = gerar_mapa_mun(dfy.groupby(["municipio"])['area_ha'].apply(np.sum),uf,'area_ha')
        print(time.time()-tempo)
        tempo = time.time()
        html = map.get_root().render()
        print(time.time()-tempo)
        return html
    return '<body></body>'

@app.callback(Output('graph_agro','figure'),[Input('btn2','n_clicks'),State('mun','value'),State('agro','value')])
def update3(click,uf,var):
    if click:
        df = datas.data_agro
        dfx = df[df['uf'] == uf]
        datas.set_df_agro(dfx.sort_values('municipio'))
        fig = px.bar(dfx,x='municipio',y=var,color='municipio',hover_name='municipio', color_continuous_scale='greens')
        fig.update_layout(transition_duration=500,template='plotly_dark')#template='plotly_dark'
        return fig
    return go.Figure()
    
@app.callback(Output('html_agro','srcDoc'),[Input('graph_agro','figure'),State('agro','value'),State('mun','value'),State('btn2','n_clicks')])
def mapa(_,var,uf,click):
    if click:
        time.sleep(3)
        dfx = datas.get_df_agro()
        print(len(dfx))
        tempo = time.time()
        map = gerar_mapa_mun(dfx,uf,var)
        print(time.time()-tempo)
        tempo = time.time()
        html = map.get_root().render()
        print(time.time()-tempo)
        return html
    return '<body></body>'




if __name__ == '__main__':
    app.run_server(debug=True)

