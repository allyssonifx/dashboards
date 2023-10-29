import time
import dash
import pdb
import styles
import numpy as np
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State
from dataframes import Dataframes
from layout import app
from mapas import Mapas


dataf = Dataframes()
mp = Mapas()

def gerar_graficos(df,x,y,color,hover):
    fig = px.bar(df,x=x,y=y,color=color,hover_name=hover)
    fig.update_layout(transition_duration=500,template='plotly_dark')
    return fig

def gerar_layout(titulo,fig,map):
    html1 = html.Div(children=[
        html.H3(titulo),
        html.Div(children=[
            dcc.Graph(figure = fig,style={"width": "60%","backgroundColor": "#212222",'margin-right':'10px'}),
            html.Iframe(srcDoc = map , width='40%', height='400px',id='html')
        ],style={'backgroundColor': '#333333','margin-bottom':'10px','display':'flex','padding':'10px'})
        ],style={'backgroundColor': '#333333','margin-bottom':'10px','padding':'10px'})
    return html1

@app.callback([Output('tela', 'children'),Output('btn_agro','hidden'),Output('btn_ivs','hidden')], [Input('btn-desmat', 'n_clicks'), Input('btn-home', 'n_clicks')])
def update_tela(btn, btn2):
    idd = callback_context.triggered[0]['prop_id'].split('.')[0]
    print(idd)
    if idd == 'btn-desmat':
        html1 = html.Div(children=[
                    html.Div(id='checklist',children=[
                        dcc.Checklist(
                        id="ck",
                        options=styles.optinonscheck,
                        value=["DC"],
                        style= styles.stylecheck,
                        labelStyle=styles.stylelabelcheck,
                        inputStyle=styles.styleinputcheck,)]),
                    html.Div(id='anos'),
                    html.Div(id='graficos_br'),
                    html.Div(id='radio_uf'),
                    html.Div(id='graficos_uf'),
                    html.Div(children=[
                        html.Div(id='dados',children=[
                        html.Button('CENSO AGRO',id='btn_agro', hidden=True),
                        html.Button('Ind. Vulnerabilidade',id='btn_ivs', hidden=True)],style={'display':'flex'}),
                        html.Div(id='div_radio_dados'),
                        html.Div(id='graficos_dados')
                    ])
                    
                        ])
        return html1,False,False
    else:
        return html.H1('Futuras atualizações'),True,True

@app.callback(Output('anos','children'),[Input('ck','value'),State('ano','value')])
def radio(check,ano):
    if check:
        df = dataf.data_config(check,True)
        dataf.set_df_uf(df)
        if ano in df['ano'].unique():
            valor = ano
        else:
            valor = df['ano'].max()
        df = df.sort_values('ano')

        html1 = html.Div(children=[
            dcc.RadioItems(id='ano',options=[{'label':i,'value':i} for i in df['ano'].unique()],value=valor,style=styles.styleradio)
        ])

        return html1
    return html.Div(children=[
            dcc.RadioItems(id='ano',style=styles.styleradio)
        ])
    
@app.callback(Output('graficos_br','children'),[Input('ck','value'),Input('ano','value')])
def graficos(check,ano):
    if check:
        df = dataf.get_df_uf()
        dfnovo = df[df.ano == ano].sort_values('uf')
        dataf.ufs = dfnovo['uf'].unique()
        fig = gerar_graficos(dfnovo,'uf','area','uf','tipo')
        dfnovo = dfnovo.groupby(["uf"])['area'].apply(np.sum)
        tempo = time.time()
        mapa = mp.gerar_mapa(dataf.gdf_br,dfnovo,'uf','area',[-15.788497, -47.879873],'Quantidade de área desmatada (ha)',3.5)
        htmlmap = mapa.get_root().render()
        print(time.time()-tempo)
        html1 = gerar_layout('Area desmatada por estado (ha)',fig,htmlmap)
        return html1
    
@app.callback(Output('radio_uf','children'),[Input('graficos_br','children'),State('ck','value'),State('ano','value')])
def radiouf(_,check,ano):
    if check:
        ufs = dataf.ufs
        html1 = html.Div(children=[
            html.Button('GERAR',id='btn_uf'),
            dcc.RadioItems(id='uf',options=[{'label':i,'value':i} for i in ufs],value=ufs[0],style=styles.styleradio)
        ],style={'backgroundColor': '#333333','margin-bottom':'10px','display':'flex','padding':'10px'})
        return html1
    
@app.callback(Output('graficos_uf','children'),[Input('btn_uf','n_clicks'),State('ck','value'),State('uf','value'),State('ano','value')])
def graficos(click,check,uf,ano):
    if click:
        for c in check:
            if c in ['PA','PC']:
                check.remove(c)
        df = dataf.data_config(check,False)
        dfnovo = df[df['ano'] == ano]
        dfnovo = dfnovo[dfnovo['uf']== uf].sort_values('municipio')
        fig = gerar_graficos(dfnovo,'municipio','area_ha','municipio','municipio')
        dfnovo = dfnovo.groupby(["municipio"])['area_ha'].apply(np.sum)
        tempo = time.time()
        dataf.buscar_shape(uf)
        coords = {'AC': [-8.77, -70.55],'AL': [-9.71, -35.73],'AM': [-3.47, -62.92],'AP': [1.41, -51.77],'BA': [-12.96, -38.51],'CE': [-3.71, -38.54],'DF': [-15.83, -47.86],'ES': [-19.19, -40.34],'GO': [-16.64, -49.31],'MA': [-2.55, -44.30],'MG': [-18.10, -44.38],'MS': [-20.51, -54.54],'MT': [-12.64, -55.42],'PA': [-5.53, -52.29],'PB': [-7.06, -35.55],'PE': [-8.28, -35.07],'PI': [-8.28, -43.68],'PR': [-24.89, -51.55],'RJ': [-22.25, -42.66],'RN': [-5.81, -36.59],'RO': [-11.22, -62.80],'RR': [1.99, -61.33],'RS': [-30.17, -53.50],'SC': [-27.45, -50.95],'SE': [-10.57, -37.45],'SP': [-22.19, -48.79],'TO': [-10.25, -48.25]}
        mapa = mp.gerar_mapa(dataf.gdf_uf,dfnovo,'municipio','area_ha',coords[uf],'Quantidade de área desmatada (ha)',6)
        htmlmap = mapa.get_root().render()
        print(time.time()-tempo)
        html1 = gerar_layout('Area desmatada por município (ha)',fig,htmlmap)
        return html1
    
@app.callback(Output('div_radio_dados','children'),[Input('btn_agro','n_clicks'),Input('btn_ivs','n_clicks')])
def dados_radio(btnagro,btnivs):
    idd = callback_context.triggered[0]['prop_id'].split('.')[0]
    if idd == 'btn_agro':
        html1 = html.Div(children=[
             dcc.RadioItems(id='radio_dados',options=[{'label':'Estab. Agropecuário','value':'V1'},{'label':'Área Média(ha)','value':'V2'},{'label':'Pessoal Ocupado','value':'V3'},{'label':'Ativ. Lavoura Temp.(%)','value':'V8'},{'label':'Ativ. Lavoura Perm.(%)','value':'V9'},{'label':'Pecuária (%)','value':'V10'},{'label':'Terras Pastagem (%)','value':'V17'},{'label':'Bovinos Corte (%)','value':'V20'},{'label':'Bovinos Leite (%)','value':'V21'},{'label':'Rendimento Milho (Kg/ha)','value':'V25'},{'label':'Rendimento Soja (Kg/ha)','value':'V26'},{'label':'Utilização Agrotóxicos(%)','value':'V34'},{'label':'Escolaridae até fundamental (%)','value':'V39'}],style=styles.styleradio)
        ])
        return html1
    elif idd == 'btn_ivs':
        return html.H3('Vazio')
    else:
        return html.H1('')

       

    
@app.callback(Output('graficos_dados','children'),[Input('radio_dados','value'),State('uf','value')])
def grafico_dados(var,uf):
    df = dataf.data_agro
    dfnovo = df[df['uf'] == uf].sort_values('municipio')
    fig = gerar_graficos(dfnovo,'municipio',var,'municipio','municipio')
    dfnovo = dfnovo.groupby(["municipio"])[var].apply(np.sum)
    tempo = time.time()
    dataf.buscar_shape(uf)
    cols = {'V1':'Estab. Agropecuário','V2':'Área Média(ha)','V3':'Pessoal Ocupado','V8':'Ativ. Lavoura Temp.(%)','V9':'Ativ. Lavoura Temp.(%)','V10':'Ativ. Lavoura Temp.(%)','V17':'Terras Pastagem (%)','V20':'Bovinos Corte (%)','V21':'Bovinos Leite (%)','V25':'Rendimento Milho (Kg/ha)','V26':'Rendimento Soja (Kg/ha)','V34':'Utilização Agrotóxicos(%)','V39':'Escolaridae até fundamental (%)'}
    coords = {'AC': [-8.77, -70.55],'AL': [-9.71, -35.73],'AM': [-3.47, -62.92],'AP': [1.41, -51.77],'BA': [-12.96, -38.51],'CE': [-3.71, -38.54],'DF': [-15.83, -47.86],'ES': [-19.19, -40.34],'GO': [-16.64, -49.31],'MA': [-2.55, -44.30],'MG': [-18.10, -44.38],'MS': [-20.51, -54.54],'MT': [-12.64, -55.42],'PA': [-5.53, -52.29],'PB': [-7.06, -35.55],'PE': [-8.28, -35.07],'PI': [-8.28, -43.68],'PR': [-24.89, -51.55],'RJ': [-22.25, -42.66],'RN': [-5.81, -36.59],'RO': [-11.22, -62.80],'RR': [1.99, -61.33],'RS': [-30.17, -53.50],'SC': [-27.45, -50.95],'SE': [-10.57, -37.45],'SP': [-22.19, -48.79],'TO': [-10.25, -48.25]}
    mapa = mp.gerar_mapa(dataf.gdf_uf,dfnovo,'municipio',var,coords[uf],cols[var],6)
    htmlmap = mapa.get_root().render()
    print(time.time()-tempo)
    html1 = gerar_layout('Area desmatada por município (ha)',fig,htmlmap)
    return html1
    


    

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)