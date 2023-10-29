import dash
import pdb
import styles
import dash_bootstrap_components as dbc
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State
from dataframes import Dataframes
 
# dataf = Dataframes()

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div(children=[ 
    dbc.Row([
        dbc.Col(children=[
            dbc.Card([
                html.H2("SIRIUS", style={'font-family': 'Voltaire', 'font-size': '40px'}),
                html.Hr(),
                html.Button(id='btn-home', children='Home'),
                html.Button(id='btn-desmat', children='Desmatamento'),
                html.Div(children=styles.layouts)
                # Botão inicialmente oculto
            ], style=styles.style_sidebar)
        ], md=2),
        dbc.Col(children=[
            html.Div(id='tela',children=[
            ]),
            html.H1(id='xxt')
        ], md=10)
    ])   
])

# @app.callback(Output('tela', 'children'), [Input('btn-desmat', 'n_clicks'), Input('btn-home', 'n_clicks'),State('tela','children')])
# def update_tela(btn, btn2,chil):
#     idd = callback_context.triggered[0]['prop_id'].split('.')[0]
#     if idd == 'btn-desmat':
#         html1 = html.Div(children=[
#                     dcc.Checklist(
#                         id="ck",
#                         options=layouts.optinonscheck,
#                         value=["DC"],
#                         style= layouts.stylecheck,
#                         labelStyle=layouts.stylelabelcheck,
#                         inputStyle=layouts.styleinputcheck
#                 )])
#         print(chil)
#         return html1
#     else:
#         return html.H1('Futuras atualizações')

# @app.callback([Output('ano','options'),Output('ano','value')],[Input('ck','value'),State('ano','value')])
# def slide(check,ano):
#     df = dataf.data_config(check,True)
#     dataf.set_df_uf(df)
#     if ano in df['ano'].unique():
#         valor = ano
#     else:
#         valor = df['ano'].max()
#     df = df.sort_values('ano')
#     return [{'label':i,'value':i} for i in df['ano'].unique()],valor

              





# if __name__ == "__main__":
#     app.run_server(port=8050, debug=True)