from dash import html, dcc, callback_context


layouts =[html.Button(id='btn_uf', hidden=True),dcc.Checklist(id='ck',value=None,style={'display': 'none'}),dcc.RadioItems(id='ano',style={'display': 'none'}),dcc.RadioItems(id='uf',style={'display': 'none'}),
          html.Div(id='checklist', hidden=True),html.Div(id='anos', hidden=True),html.Div(id='graficos_br', hidden=True),html.Div(id='radio_uf', hidden=True),html.Div(id='graficos_uf', hidden=True),
          html.Div(id='dados', hidden=True),html.Button(id='btn_agro', hidden=True),    html.Button(id='btn_ivs',hidden=True),html.Div(id='div_radio_dados', hidden=True),dcc.RadioItems(id='radio_dados',style={'display': 'none'}),
          html.Div(id='graficos_dados', hidden=True)]

#STYLE SIDEBAR

style_sidebar = style={"box-shadow": "2px 2px 10px 0px rgba(10, 9, 7, 0.10)",
                    "margin": "10px",
                    "padding": "10px",
                    "height": "100vh"}

#Style CHECKBOX

optinonscheck = [{'label': 'DETER Cerrado', 'value': 'DC'},
        {'label': 'DETER Amazônia', 'value': 'DA'},
        {'label': 'PRODES Cerrado', 'value': 'PC'},
        {'label': 'PRODES Amazônia', 'value': 'PA'},
        {'label': 'Desmatamento Mapbiomas', 'value': 'DM'}]

stylecheck = {
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
        
    }

stylelabelcheck = {
        "display": "inline-block",
        "background-color": '#333333',
        "border-radius": "5px",
        "margin-top": "20px",
        "padding": "5px",
        "font-family": "Arial, sans-serif",
        "color": "white",
        "cursor": "pointer"
    }

styleinputcheck = {
        "margin-right": "5px",
        "margin-bottom": "5px",
        "vertical-align": "middle",
        'pointer-events': 'none'
    }

# RadioItemns


styleradio = {
                "margin-bottom": "10px",
                "margin-left": "20px",
                "margin-right": "20px",
                "margin-top": "15px",
                "display": "flex",
                "flex-wrap": "wrap",
                "width": "95%",
                "gap": "10px",
                "justify-content": "space-between",
                "font-family": "Arial, sans-serif",
                "color":"white"
            }