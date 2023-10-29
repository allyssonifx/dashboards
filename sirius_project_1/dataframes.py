import re
import unicodedata
import pandas as pd
import geopandas as gpd


class Dataframes:
    def __init__(self):                     
        self.df_dic_uf = {'DC':pd.read_csv('dados\csv_area_estado\\deter_cerrado.csv'),'DA':pd.read_csv('dados\csv_area_estado\\deter_amazonia.csv'),'PC':pd.read_csv('dados\csv_area_estado\\prodes_cer.csv'),'PA':pd.read_csv('dados\csv_area_estado\\prodes_amz.csv'),'DM':pd.read_csv('dados\csv_area_estado\\desmatamento_mapbiomas.csv')}
        self.df_dic_mun = {'DC':pd.read_csv('dados\csv_area_municipio\deter_cerrado_m.csv'),'DA':pd.read_csv('dados\csv_area_municipio\deter_amazonia_m.csv'),'DM':pd.read_csv('dados\csv_area_municipio\desmatamento_m.csv')}
        self.df_uf = pd.DataFrame()
        self.gdf_br = gpd.read_file('dados\\shapes_brasil\\brasil\\br1.shp')
        self.data_agro = pd.read_csv('dados\\csv_agro\\agro.csv')
        self.gdf_uf = None
        self.ufs = []


    def data_config(self,check,divisor):
        df = pd.DataFrame({'municipio':[],'ano':[],'uf':[],'area_ha':[]})
        dados = {'DC':'DETER Cerrado','DA':'DETER Amazônia','PA':'PRODES Amazônia','PC':'PRODES Cerrado','DM':'Desmatamento MapBiomas'}
        if divisor:
            for c in check:
                dftemp = self.df_dic_uf[c]
                dftemp['tipo'] = dados[c]
                df = pd.concat([df,dftemp])
        else:
            for c in check:
                dftemp = self.df_dic_mun[c]
                dftemp['tipo'] = dados[c]
                df = pd.concat([df,dftemp]) 
        return df
    
    def remover_caracteres_especiais(self,texto):
        # Normaliza a string removendo acentos e caracteres especiais
        texto_normalizado = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        # Remove os caracteres não alfanuméricos
        texto_sem_especiais = re.sub(r'[^a-zA-Z0-9\s]', '', texto_normalizado)
        return texto_sem_especiais.upper()
    
    def buscar_shape(self,uf):
        caminho = 'dados/shapes_estados/'+uf+'/'+uf+'.shp'
        gdf = gpd.read_file(caminho)
        gdf.rename(columns={'MUNICIPIO':'municipio'},inplace=True)
        gdf['municipio']= gdf['municipio'].apply(self.remover_caracteres_especiais)
        self.gdf_uf = gdf
    

    def set_df_uf(self,df):
        self.df_uf = df

    def get_df_uf(self):
        return self.df_uf