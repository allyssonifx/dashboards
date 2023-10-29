import json
import folium
import pandas as pd
import geopandas as gpd

class Mapas:
    def gerar_mapa(self,gdf,df,col,var,coord,legenda,zoom):
        m = folium.Map(location=coord,zoom_start=zoom,tiles='CartoDB dark_matter')
        merged_df = pd.merge(gdf, df, on=col, how='outer')
        maior = merged_df[var].max()

        maior80 = round((maior*0.8))
        maior60 = round((maior*0.6))  
        maior40 = round((maior*0.4))
        maior20 = round((maior*0.2))

        geo3 = merged_df.to_json()

        folium.Choropleth(
        geo_data=geo3,
        data=merged_df,
        columns=(col, var),
        key_on="feature.properties."+col,
        bins=[0,maior20,maior40,maior60,maior80,maior],
        fill_color="Reds",
        fill_opacity=0.8,
        line_opacity=0.3,
        nan_fill_color="#212222",
        legend_name=legenda,
        ).add_to(m)
        print('chegou dnv')
        return m