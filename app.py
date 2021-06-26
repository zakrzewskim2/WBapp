# %%
import dash
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash_html_components.Button import Button
from dash_html_components.Div import Div
from numpy.core.defchararray import count
from numpy.lib.shape_base import column_stack
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.graph_objs.layout import Margin
from map_helper import build_map
import os
from joblib import load
import json
import ast

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# LOAD DATA
with open(os.path.join(THIS_FOLDER, 'assets', 'stops_in_rejon.json'), encoding='utf8') as json_file:
    stops_in_rejon = json.load(json_file)

with open(os.path.join(THIS_FOLDER, 'assets', 'schools_in_rejon.json'), encoding='utf8') as json_file:
    schools_in_rejon = json.load(json_file)

with open(os.path.join(THIS_FOLDER, 'assets', 'veturillo_in_rejon.json'), encoding='utf8') as json_file:
    veturillo_in_rejon = json.load(json_file)

schools_with_progi = pd.read_csv(os.path.join(
    THIS_FOLDER, 'assets', 'schools_with_progi.csv'))

stops_info = pd.read_csv(os.path.join(
    THIS_FOLDER, 'assets', 'stops_info.csv'), encoding='utf-8')
stops_info = stops_info.astype({'Unnamed: 0': 'str'})

dojazdy_info = pd.read_csv(os.path.join(
    THIS_FOLDER, 'assets', 'best_stats.csv'), encoding='utf-8', index_col=0)

stops_name_info = stops_info.rename(columns={"Unnamed: 0": "number"})
stops_name_info = stops_name_info[["number", "name"]]
dojazdy_info.fillna(float("inf"), inplace=True)
dojazdy_info.source_stop = dojazdy_info.source_stop.astype(float)
stops_name_info.number = stops_name_info.number.astype(float)

METRIC_MAPPING = [
    {'label': 'nowa', 'value': 'new_metric'},
    {'label': 'procentowa', 'value': 'percentage_metric'}
]

schools_with_progi_Num_Type = schools_with_progi.loc[:, [
    'Numer szkoły', 'Typ']]

dojazdy_merged = schools_with_progi_Num_Type.merge(
    dojazdy_info, left_on='Numer szkoły', right_on='school')

button_names = []
# #%%
# sir = [item for sublist in schools_in_rejon.values() for item in sublist]
# st = [float(item) for sublist in stops_in_rejon.values() for item in sublist]
# vt = [float(item) for sublist in veturillo_in_rejon.values() for item in sublist]
# st.extend(vt)
# di = dojazdy_info.loc[np.isin(dojazdy_info.school, sir)]
# dis = di.loc[np.isin(di.source_stop, st)]
# dis = dis.loc[np.isin(dis.best_end_stop, st)]
# dis.to_csv("assets/best_stats_new.csv")
# %%
METRIC_SCHOOL_TYPE_MAPPING = [
    {'label': 'dowolnych szkół', 'value': 'ALL'},
    {'label': 'szkół podstawowych', 'value': 'POD'},
    {'label': 'liceów ogólnokształcących', 'value': 'LIC'},
    {'label': 'techników', 'value': 'TEC'},
    {'label': 'szkół zawodowych', 'value': 'ZAW'},
    {'label': 'szkół podstawowych i zawodowych oraz liceów i techników','value': 'POD-LIC-ZAW-TEC'},
    {'label': 'szkół artystycznych', 'value': 'MUZ'},
    {'label': 'przedszkoli', 'value': 'PRZ'},
    {'label': 'szkół podstawowych i liceów', 'value': 'POD-LIC'},
    {'label': 'szkół podstawowych i zawodowych', 'value': 'POD-ZAW'},
    {'label': 'szkół podstawowych i techników', 'value': 'POD-TEC'},
    {'label': 'liceów i techników', 'value': 'LIC-TEC'},
    {'label': 'liceów i szkół zawodowych', 'value': 'LIC-ZAW'},
    {'label': 'techników i szkół zawodowych', 'value': 'ZAW-TEC'},
    {'label': 'szkół podstawowych, liceów i techników', 'value': 'POD-LIC-TEC'},
    {'label': 'szkół podstawowych, zawodowych i techników', 'value': 'POD-ZAW-TEC'},
    {'label': 'szkół zawodowych, liceów i techników', 'value': 'LIC-ZAW-TEC'},
]

SCHOOL_TYPE_MAPPING = {'OUT': ['Placówka doskonalenia nauczycieli',
                               'Młodzieżowy Ośrodek Socjoterapii ze szkołami',
                               'Biblioteki pedagogiczne',
                               'Pozaszkolna placówka specjalistyczna',
                               'Bursa',
                               'Młodzieżowy Ośrodek Wychowawczy',
                               'Zespół szkół i placówek oświatowych',
                               'Specjalny Ośrodek Szkolno-Wychowawczy',
                               'Poradnia specjalistyczna',
                               'Szkoła policealna',
                               'Szkolne schronisko młodzieżowe',
                               'Młodzieżowy dom kultury',
                               'Niepubliczna placówka oświatowo-wychowawcza w systemie oświaty',
                               'Poradnia psychologiczno-pedagogiczna',
                               'Szkoła specjalna przysposabiająca do pracy',
                               'Ognisko pracy pozaszkolnej',
                               'Policealna szkoła plastyczna',
                               'Ogród jordanowski',
                               'Ośrodek Rewalidacyjno-Wychowawczy',
                               'Międzyszkolny ośrodek sportowy',
                               'Specjalny Ośrodek Wychowawczy',
                               'Pałac młodzieży',
                               'Policealna szkoła muzyczna'],
                       'PRZ': ['Przedszkole',
                               'Punkt przedszkolny',
                               'Zespół wychowania przedszkolnego'],
                       'POD': ['Szkoła podstawowa'],
                       'ZAW': ['Branżowa szkoła I stopnia',
                               'Placówka Kształcenia Ustawicznego - bez szkół',
                               'Placówka Kształcenia Ustawicznego ze szkołami',
                               'Centrum Kształcenia Zawodowego',
                               'Bednarska Szkoła Realna',
                               'Branżowa szkoła II stopnia'],
                       'LIC': ['Liceum ogólnokształcące'],
                       'TEC': ['Technikum'],
                       'MUZ': ['Szkoła muzyczna I stopnia',
                               'Szkoła muzyczna II stopnia',
                               'Ogólnokształcąca szkoła muzyczna II stopnia',
                               'Ogólnokształcąca szkoła muzyczna I stopnia',
                               'Inna szkoła artystyczna',
                               'Ogólnokształcąca szkoła baletowa',
                               'Placówki artystyczne (ognisko artystyczne)',
                               'Liceum sztuk plastycznych']}

METRIC_TIME_MAPPING = [
    {'label': '15 minut.', 'value': 'time-15'},
    {'label': '30 minut.', 'value': 'time-30'},
    {'label': '60 minut.', 'value': 'time-60'},
    {'label': '90 minut.', 'value': 'time-90'}
]

METRIC_THRESHOLDS_MAPPING = [
    {'label': 'uwzględniając', 'value': 'thresholds-True'},
    {'label': 'pomijając', 'value': 'thresholds-False'}
]

METRIC_WEIGHT_MAPPING = [
    {'label': 'ważona', 'value': 'weight-True'},
    {'label': 'nie ważona', 'value': 'weight-False'}
]


def gen_widelki_labels(widelki):
    labels = {}
    for i, (s, e) in enumerate(zip([0] + list(widelki[:-1]), widelki)):
        labels[i] = f'[{s}, {e}) minut'
    labels[len(widelki)] = 'ponad 120 minut'
    return labels


def convert_number_to_hist_x(widelki, number):
    for i, (s, e) in enumerate(zip([0] + list(widelki[:-1]), widelki)):
        if number >= s and number < e:
            return i - .5 + (number - s) / (e - s)


app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    './styles.css',
])

server = app.server


def generate_table(df_dict, width, name=""):
    return html.Div([html.Table(
        # Header
        [html.Thead(
            [html.Tr([html.Th(col, style={
                "border": "1px solid black",
                'textAlign': 'center'
            }) for col in df_dict.keys()]
            )])] +
        [html.Tbody(
            # Body
            [html.Tr(
                [html.Td([
                    html.Table(
                        [html.Thead(
                            html.Tr(
                                html.Th(
                                    html.Button(row["Nazwa"], style={"width": "100%"}, id="collapse_button_" + row["Nazwa"] + name), style={
                                        "border": "1px solid black",
                                        'textAlign': 'center'},
                                    colSpan=2
                                )
                            )
                        )] +
                        # Body
                        [html.Tbody([html.Tr([
                            html.Td(index, style={
                                "border": "1px solid black", "verticalAlign": "top"}),
                            generate_table(value, "auto", row["Nazwa"]) if type(
                                value) is dict else html.Td(value)
                        ], style={
                            "border": "1px solid black"
                        }) for index, value in row.items()], style={'display': 'none', 'width': '100%'}, id="table_to_collapse_" + row["Nazwa"] + name)]
                    ) for _, row in df_dict[col].items()
                ], style={
                    "border": "1px solid black",
                    'verticalAlign': 'top',
                    'width': "auto"
                }
                ) for col in df_dict.keys()])])]
    )], style={
        'width': width,
        'height': '93%',
        'overflow-y': "auto",
        'overflow-x': "auto",
        'margin': '0px 5px 0px 0px'
    }
    )


def generate_almost_static_table(df_dict):
    num_col = df_dict.shape[1]
    return html.Table(
        # Header
        [html.Tr([html.Th(style={"width": "20%"})] + [html.Th(col, style={"width": f"{80/num_col}%"}) for col in df_dict.columns])] +
        # Body
        [html.Tr(
            [html.Td(html.Button("Zaznacz",  id={'type': 'select-region', 'index': f'{df_dict.iloc[i,0]}'}, style={"background-color": "#36ba3d", "width": "100%"}), style={"width": "20%"})] + [
                html.Td(df_dict.iloc[i][col], style={"width": f"{80/num_col}%"}) for col in df_dict.columns
            ], style={"border": "1px solid black"}
        ) for i in range(len(df_dict))], style={"border": "1px solid black"}
    )


def generate_static_table(df_dict):
    return html.Table(
        # Header
        [html.Tr([html.Th(col, style={"paddingRight": "10px", "border": "1px solid black", "background": "white", "position": "sticky", "top": "0"}) for col in df_dict.columns], style={"position": "relative", "width": "100%", "border": "1px solid black"})] +
        # Body
        [html.Tr([
            html.Td(df_dict.iloc[i][col], style={"paddingRight": "10px"}) for col in df_dict.columns
        ], style={"border": "1px solid black"}) for i in range(len(df_dict))]
    )


app.layout = html.Div(
    children=[
        html.Div(
            id='map-section',
            children=html.Div(
               className='screen-height',
               children=[
                   html.Div(
                       className='section',
                       children=[
                           html.Div(
                               id='map-filters',
                               children=[
                                   html.H5(
                                       'Zaznacz na mapie:'),
                                   dcc.Checklist(
                                       id='map-type-checklist',
                                       labelClassName='map-type-checklist-items',
                                       options=[
                                           {'label': 'Przystanki',
                                            'value': 'stops'},
                                           {'label': 'Szkoły',
                                            'value': 'schools'},
                                           {'label': 'Metro',
                                            'value': 'subway'},
                                           {'label': 'Stacje Veturilo',
                                            'value': 'veturilo'}
                                       ],
                                       value=[]
                                   )
                               ],
                               style={
                                   'display': 'block'
                               }
                           ),
                           html.Div(
                               id='schools-filters',
                               children=[
                                   html.H5(
                                       'Typ szkoły:'),
                                   dcc.Checklist(
                                       id='school-type-checklist',
                                       labelClassName='school-type-checklist-items',
                                       options=[
                                           {'label': 'Wszystkie',
                                            'value': 'all'},
                                           {'label': 'Szkoły podstawowe',
                                            'value': 'school_podst'},
                                           {'label': 'Licea ogólnokształcące',
                                            'value': 'school_lic'},
                                           {'label': 'Szkoły techniczne',
                                            'value': 'school_tech'},
                                            {'label': 'Szkoły zawodowe',
                                            'value': 'school_zaw'},
                                            {'label': 'Szkoły artystyczne',
                                            'value': 'school_art'},
                                            {'label': 'Przedszkola',
                                            'value': 'kindergardens'}
                                       ],
                                       value=['all']
                                   )
                               ],
                               style={
                                   'display': 'none'
                               }
                           ),
                           html.Div(children=[
                               html.Div(children=[
                                   html.Div(
                                    id="metric-values-table",
                                    style={"width": "400px", "flexGrow": "1", "overflow": "auto"}
                                    ),
                                   html.Div(children=[
                                       html.Div(
                                           children=[
                                               html.Div(
                                                   children=[
                                                       dcc.Slider(
                                                           id='show-top-x-interval',
                                                           value=20,
                                                           min=1,
                                                           max=50,
                                                           # step=None,
                                                           marks={
                                                               1: '1%',
                                                               5: '5%',
                                                               10: '10%',
                                                               15: '15%',
                                                               20: '20%',
                                                               25: '25%',
                                                               30: '30%',
                                                               35: '35%',
                                                               40: '40%',
                                                               45: '45%',
                                                               50: '50%',
                                                           }
                                                       ),
                                                       html.Button(
                                                           "Zaznacz górne 20% rejonów", id="show-top-x-button")
                                                   ], style={"margin": "10px 0px 10px 0px"}
                                               ),
                                               html.Div(
                                                   children=[
                                                       dcc.Slider(
                                                           id='show-bottom-x-interval',
                                                           value=20,
                                                           min=1,
                                                           max=50,
                                                           # step=None,
                                                           marks={
                                                               1: '1%',
                                                               5: '5%',
                                                               10: '10%',
                                                               15: '15%',
                                                               20: '20%',
                                                               25: '25%',
                                                               30: '30%',
                                                               35: '35%',
                                                               40: '40%',
                                                               45: '45%',
                                                               50: '50%',
                                                           }
                                                       ),
                                                       html.Button(
                                                           "Zaznacz dolne 20% rejonów", id="show-bottom-x-button")
                                                   ], style={"margin": "10px 0px 10px 0px"}
                                               )]
                                       )
                                   ], style={"height": "30%", "minHeight" : "150px", "width" : "400px", "textAlign" : "center"}
                                   )], style={"display": "flex", "flexDirection": "column", "height" : "100%", "width" : "400px"}),
                               html.Div(
                                   children=[
                                       dcc.Graph(
                                           id='map',
                                           className='fill-height',
                                           config={
                                               'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
                                               'scrollZoom': False
                                           },
                                           style={"height": "100%"},
                                       ),
                                       html.Div(id="output")
                                   ], style={'max-height': '100%', 'width': '60%', "margin": "0px 0px 0px 20px"}
                               ),
                               html.Div(children=[
                                   html.Plaintext(id='hist-interval-output', style={
                                       'display': 'inline-block', 'fontSize': '12pt'}),
                                   html.Div(
                                       dcc.Slider(
                                           id='hist-interval',
                                           value=10,
                                           min=3,
                                           max=60,
                                           # step=None,
                                           marks={
                                               3: '3',
                                               5: '5',
                                               10: '10',
                                               15: '15',
                                               20: '20',
                                               30: '30',
                                               40: '40',
                                               60: '60',
                                           },
                                           # tooltip = { 'placement': 'bottom' }
                                       ), style={"width": "100%"}
                                   ),
                                    html.Div(style={"flexGrow": "1"}),
                                   html.Div(children=[
                                       dcc.Graph(
                                           id='histogram',
                                           config={
                                               'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
                                               'scrollZoom': False
                                           },
                                           style={"height": "100%", "width" : "100%"},
                                       )
                                   ], style={"overflow" : "auto", "width" : "100%", "minHeight" : "50%"}),
                                   html.Div(style={"flexGrow": "1"}),
                               ], style={"flex-grow": "1", "display": "flex", "flex-direction": "column", "width" : "40%", "minWidth" : "300px", "align-items": "center"})

                           ], style={"height": "60%", "display": "flex"}
                           ),
                           html.Div(
                               children=[
                                   html.Plaintext("Typ metryki ", style={
                                       'display': 'inline-block', 'fontSize': '12pt'}),
                                   dcc.Dropdown(
                                       id='metric',
                                       options=METRIC_MAPPING,
                                       value='percentage_metric',
                                       style=dict(
                                           width=110,
                                           display='inline-block',
                                           verticalAlign="middle",
                                           textAlign="left"
                                       )
                                   ),
                                   dcc.Dropdown(
                                       id='metric-weight',
                                       options=METRIC_WEIGHT_MAPPING,
                                       value='weight-True',
                                       style=dict(display='none')
                                   ),

                                   html.Plaintext(", dla ", style={
                                       'display': 'inline-block', 'fontSize': '12pt'}),
                                   dcc.Dropdown(
                                       id='metric-school-type',
                                       options=METRIC_SCHOOL_TYPE_MAPPING,
                                       value='ALL',
                                       style=dict(
                                           width=460,
                                           display='inline-block',
                                           verticalAlign="middle",
                                           textAlign="left"
                                       )
                                   ),

                                   html.Plaintext(
                                       ", dostępnych w czasie nie większym niż ", id="plaintext-time"),
                                   dcc.Dropdown(
                                       id='metric-time',
                                       options=METRIC_TIME_MAPPING,
                                       value='time-30'
                                   ),

                                   dcc.Dropdown(
                                       id='metric-thresholds',
                                       options=METRIC_THRESHOLDS_MAPPING,
                                       value='thresholds-True',
                                       style=dict(display='none')
                                   ),
                                   html.Plaintext(
                                       " progi.", id="plaintext-thresholds", style=dict(display='none'))
                               ]
                           ),
                           html.Div(
                               children=[
                                   html.Div(
                                       children=[
                                           html.Div(
                                               children=[
                                                   html.Div(
                                                       html.Button(
                                                           "Wyświetl informacje o przystankach",
                                                           style={
                                                               'font': '14pt Arial Black',
                                                               'margin': "0px 0px 0px 15px",
                                                           },
                                                           id="stops-info-button"
                                                       )
                                                   ),
                                                   html.Div(
                                                       id="stops-info-table",
                                                       style={
                                                           'margin': "0px 0px 0px 5px",
                                                           'width': '100%',
                                                           'height': '100%'
                                                       }
                                                   )
                                               ],
                                               style={
                                                   'border': '1px solid black',
                                                   'float': 'left',
                                                   'width': '50%',
                                                   'height': '100%',
                                                   'overflow-y': "auto",
                                                   'overflow-x': "auto"
                                               }
                                           ),
                                           html.Div(
                                               children=[
                                                   html.Div(
                                                       html.Button(
                                                           "Wyświetl informacje o szkołach",
                                                           style={
                                                               'font': '14pt Arial Black',
                                                               'margin': "0px 0px 0px 15px",
                                                           },
                                                           id="schools-info-button"
                                                       )
                                                   ),
                                                   html.Div(
                                                       id="schools-info-table",
                                                       style={
                                                           'margin': "0px 0px 0px 5px",
                                                           'width': '100%',
                                                           'height': '100%'
                                                       }
                                                   ),

                                               ],
                                               style={
                                                   'border': '1px solid black',
                                                   'float': 'left',
                                                   'width': '50%',
                                                   'height': '100%',
                                                   'overflow-y': "auto",
                                                   'overflow-x': "auto"
                                               }
                                           )
                                       ],
                                       style={
                                           'border': '1px solid black',
                                           'height': '100%',
                                           'max-height': '100%',
                                           'width': '65%'
                                       }),
                                   html.Div(
                                       children=[
                                           html.Div([
                                               html.Button(
                                                   "Wyświetl informacje dojazdowe",
                                                   style={
                                                       'font': '14pt Arial Black',
                                                               'margin': "0px 0px 0px 15px",
                                                   },
                                                   id="dojazdy-info-button"
                                               ),
                                               html.A(
                                                    id="download",
                                                    download="dojazdy_inf.csv",
                                                    style={"float" : "right"}
                                                ),
                                                dcc.Store("dojazdy-csv-store")
                                            ], style={"display": "flex", "flex-direction":"row", "justify-content" : "space-between"}),
                                           html.Div(
                                               id="dojazdy-info-table",
                                               style={
                                                   'margin': "0px 0px 0px 5px",
                                                   'width': '100%',
                                                   'height': '100%'
                                               }
                                           ),
                                       ],
                                       style={
                                           'border': '1px solid black',
                                           'float': 'left',
                                           'width': '50%',
                                           'height': '100%',
                                           'overflow-y': "auto",
                                           "overflow-x": "auto"
                                       }
                                   )
                               ], style={"display": "flex", "height": "30%"}
                           ),
                           html.Div("[10,20,30,40,50,60,70,80,90,100,110,120]",
                                    id='widelki-selection', style={'display': 'none'}),
                           html.Div(id='selected-region-indices',
                                    style={'display': 'none'}, children=''),
                           html.Div(id='selected-button-indices',
                                    style={'display': 'none'}, children=''),
                           html.Div(id='scroll-blocker',
                                    className='scroll'),
                           html.Div(id='all_button_ids',
                                    style={'display': 'none'}),
                           html.Div(id='dojazdy_button_ids',
                                    style={'display': 'none'}),
                           html.Div(id='region_numbers_sorted_by_metric',
                                    style={'display': 'none'}),
                           html.Div(id='empty', style={'display': 'none'}),
                           html.Div(id='empty2', style={'display': 'none'}),
                           html.Div(id='empty3', style={'display': 'none'}),
                           html.Div(id='empty4', style={'display': 'none'})
                       ]
                   ),
               ]
            )
        )
    ]
)

app.clientside_callback(
    """
function(the_store_data) {
    var t = the_store_data.split('\\n');
    var s = t[0].split(/\s+/).join(",").replaceAll("_"," ") + '\\n';
    s = s.substring(1);
    for(let i=1; i < t.length; i++) {
        var row = t[i].split(/\s{2,}/).join(",") + '\\n';
        if(row.startsWith(',') || row.startsWith(' ')){
            s += row.substring(1);
        }
        else {
            s += row;
        }
    }
    let b = new Blob([s],{type: 'text/csv;charset=utf-8;'});
    let url = URL.createObjectURL(b);
    return url;
}
""",
    Output("download", "href"),
    [Input("dojazdy-csv-store", "data")],
)


@app.callback(
    Output('download','children'),
    [Input('download','href')]
)
def update_download_children(_): # we probably won't use the href
    # fill the children with a download button
    return html.Button(id='download-button', style={"background-image" : "url('assets/csv-file.svg')", "width" : "30px", "height" : "30px", "background-color": "transparent",  "border": "none"})

app.clientside_callback(
    """
    function setup_stuff(ids) {
        for (let i = 0; i < ids.length; i++) {
            var collapse_button = document.getElementById("collapse_button_" + ids[i].substring(10));
            collapse_button.addEventListener("click", collapse, false);
        }
        return 0;
    }
    function collapse(event) {
        var id = event.target.id.substring(16);
        var table_to_collapse = document.getElementById("table_to_collapse_" + id);
        if (table_to_collapse.style.display == "block") {
        table_to_collapse.style.display = "none";
        } else {
        table_to_collapse.style.display = "block";
        }
    }
    """,
    [Output("empty", "children")],
    [
        Input("all_button_ids", "children"),
    ]
)
app.clientside_callback(
    """
    function setup_new_stuff() {
        for (let i = 0; i < 800; i++) {
            var button = document.getElementById('{"index":"' + i + '","type":"select-region"}');
            if (button === null || button === undefined) {
                continue;
            }
            button.addEventListener("click", change_button, false);
        }
        return 0;
    }
    function change_button(event) {
        var button_to_change = document.getElementById(event.target.id);
        if (button_to_change.innerHTML == "Zaznacz") {
            button_to_change.innerHTML = "Ukryj";
            button_to_change.style.backgroundColor = "#de4545";
        } else {
            button_to_change.innerHTML = "Zaznacz";
            button_to_change.style.backgroundColor = "#36ba3d";
        }
    }
    """,
    [Output("empty2", "children")],
    [
        Input("metric-values-table", "children"),
    ]
)
app.clientside_callback(
    """
    function change_buttons_top(n_clicks, percentage, sorted_regions) {
        if (sorted_regions === null || sorted_regions === undefined) {
            return 0;
        }
        indices = sorted_regions.slice(0, Math.floor(percentage/100*sorted_regions.length));
        for (let i = 0; i < indices.length; i++) {
            var button_to_change = document.getElementById('{"index":"' + indices[i] + '","type":"select-region"}');
            if (n_clicks === undefined || n_clicks % 2 == 0) {
                button_to_change.innerHTML = "Zaznacz";
                button_to_change.style.backgroundColor = "#36ba3d";
            }
            else {
                button_to_change.innerHTML = "Ukryj";
                button_to_change.style.backgroundColor = "#de4545";
            }
        }
        return 0;
    }
    """,
    [Output("empty3", "children")],
    [
        Input('show-top-x-button', 'n_clicks'),
    ],
    [
        State('show-top-x-interval', 'value'),
        State('region_numbers_sorted_by_metric', 'children'),
    ]
)
app.clientside_callback(
    """
    function change_buttons_bottom(n_clicks, percentage, sorted_regions) {
        if (sorted_regions === null || sorted_regions === undefined) {
            return 0;
        }
        indices = sorted_regions.slice(sorted_regions.length - Math.ceil(percentage/100*sorted_regions.length), sorted_regions.length);
        for (let i = 0; i < indices.length; i++) {
            var button_to_change = document.getElementById('{"index":"' + indices[i] + '","type":"select-region"}');
            if (n_clicks === undefined || n_clicks % 2 == 0) {
                button_to_change.innerHTML = "Zaznacz";
                button_to_change.style.backgroundColor = "#36ba3d";
            }
            else {
                button_to_change.innerHTML = "Ukryj";
                button_to_change.style.backgroundColor = "#de4545";
            }
        }
        return 0;
    }
    """,
    [Output("empty4", "children")],
    [
        Input('show-bottom-x-button', 'n_clicks'),
    ],
    [
        State('show-bottom-x-interval', 'value'),
        State('region_numbers_sorted_by_metric', 'children'),
    ]
)


@app.callback(
    [
        Output('selected-region-indices', 'children'),
        Output('selected-button-indices', 'children'),
    ],
    [
        Input({'type': 'select-region', 'index': ALL}, 'n_clicks'),
        Input('selected-region-indices', 'children'),
        Input('map', 'selectedData'),
        Input('selected-button-indices', 'children'),
        Input('show-top-x-button', 'n_clicks'),
        Input('show-bottom-x-button', 'n_clicks'),
    ],
    [
        State('show-top-x-interval', 'value'),
        State('show-bottom-x-interval', 'value'),
        State('region_numbers_sorted_by_metric', 'children'),
    ])
def multi_select_region(values, selectedindices, selectedregion, buttonindices, top_n_clicks, bottom_n_clicks, top_threshold, bottom_threshold, sorted_rejony):
    if selectedindices == '':
        selectedindices = []
    if buttonindices == '':
        buttonindices = []
    if sorted_rejony is None:
        sorted_rejony = []
    ctx = dash.callback_context
    if selectedregion is None:
        output_indices = buttonindices
    else:
        selected_region_indices = [item['pointIndex']
                                   for item in selectedregion['points']]
        output_indices = list(
            set(selected_region_indices).union(set(buttonindices)))

    if not ctx.triggered:
        return output_indices, buttonindices
    else:
        if len(values) > 0 and values == [None]*len(values) and top_n_clicks is None and bottom_n_clicks is None:
            return output_indices, buttonindices
        for triggered in ctx.triggered:
            try:
                eval_result = eval(triggered["prop_id"].split(".")[0])
                clicked_region = eval_result["index"]
                if int(clicked_region) in buttonindices:
                    buttonindices.remove(int(clicked_region))
                else:
                    buttonindices.append(int(clicked_region))
                if selectedregion is None:
                    output_indices = buttonindices
                else:
                    selected_region_indices = [item['pointIndex']
                                               for item in selectedregion['points']]
                    output_indices = list(
                        set(selected_region_indices).union(set(buttonindices)))
                return output_indices, buttonindices
            except:
                if triggered["prop_id"].split(".")[0] == "show-top-x-button":
                    if top_n_clicks % 2 == 1:
                        buttonindices = list(set(buttonindices).union(
                            set(np.array(sorted_rejony)[:int(top_threshold/100*len(sorted_rejony))])))
                        output_indices = list(
                            set(output_indices).union(set(buttonindices)))
                    else:
                        selected_top_regions = list(np.array(sorted_rejony)[:int(top_threshold/100*len(sorted_rejony))])
                        buttonindices = [
                            elem for elem in buttonindices if elem not in selected_top_regions]
                        output_indices = [
                            elem for elem in output_indices if elem not in selected_top_regions]
                    
                if triggered["prop_id"].split(".")[0] == "show-bottom-x-button":
                    if bottom_n_clicks % 2 == 1:
                        buttonindices = list(set(buttonindices).union(
                            set(np.array(sorted_rejony)[-int(bottom_threshold/100*len(sorted_rejony))-1:])))
                        output_indices = list(
                            set(output_indices).union(set(buttonindices)))
                    else:
                        selected_top_regions = list(np.array(sorted_rejony)[-int(bottom_threshold/100*len(sorted_rejony))-1:])
                        buttonindices = [
                            elem for elem in buttonindices if elem not in selected_top_regions]
                        output_indices = [
                            elem for elem in output_indices if elem not in selected_top_regions]
                return output_indices, buttonindices

@ app.callback(
    [
        Output('map', 'figure'),
        Output('histogram', 'figure')
    ],
    [
        Input('metric', 'value'),
        Input('metric-weight', 'value'),
        Input('metric-school-type', 'value'),
        Input('metric-time', 'value'),
        Input('metric-thresholds', 'value'),
        Input('map-type-checklist', 'value'),
        Input('school-type-checklist', 'value'),
        Input('selected-region-indices', 'children'),
        Input('widelki-selection', 'children')
    ])
def update_map(metric, metric_weight, metric_type, metric_time, metric_thresholds, options, schools_options, selceted_region, widelki_string):
    stop_numbers = []
    for i in selceted_region:
        if str(i) in stops_in_rejon:
            for stop in stops_in_rejon[str(i)]:
                stop_numbers.append(int(stop))

    widelki = np.array([]) if widelki_string is None else np.array(eval(widelki_string))
    widelki_labels = gen_widelki_labels(widelki)

    if metric_type != 'ALL':
        school_types = []
        for part in metric_type.split('-'):
            school_types += SCHOOL_TYPE_MAPPING[part]

        dojazdy_merged_filtered = dojazdy_merged.loc[np.isin(dojazdy_merged.Typ, school_types)]
    else:
        dojazdy_merged_filtered = dojazdy_merged

    if len(selceted_region) > 0:
        dojazdy = np.array(dojazdy_merged_filtered.loc[np.isin(dojazdy_merged_filtered.source_stop, stop_numbers)]["TOTAL_LEN"])
    else:
        dojazdy = np.array(dojazdy_merged_filtered["TOTAL_LEN"])

    columns = np.sum(np.repeat(dojazdy, len(widelki)).reshape(len(dojazdy), len(
        widelki)) >= np.repeat(widelki.reshape(-1, 1), len(dojazdy), axis=1).transpose(), axis=1)
    unique, counts = np.unique(columns, return_counts=True)

    new_unique = []
    new_counts = []
    counts_index = 0
    for i, _ in enumerate(widelki_labels):
        new_unique.append(i)
        if i in unique:
            new_counts.append(counts[counts_index])
            counts_index += 1
        else:
            new_counts.append(0)
    counts = new_counts
    unique = new_unique

    fig = go.Figure([go.Bar(x=[widelki_labels[u] for u in unique], y=counts)])
    fig.update_layout(margin=dict(l=15, r=15, t=20, b=15),)

    if len(dojazdy) > 0:
        dojazdy_no_inf = dojazdy
        dojazdy_no_inf[np.isinf(dojazdy)] = 120

        mean_value = dojazdy_no_inf.mean()
        fig.add_vline(x=convert_number_to_hist_x(widelki, mean_value),
                      line_dash="dot",
                      line_color="#d80000",
                      annotation_text=f"Średnia: {round(mean_value, 2)} minuty",
                      annotation_position="top",
                      annotation_font_size=12,
                      annotation_font_color="#d80000"
                      )

    selected_metric = "_".join(["metric", metric, metric_type, metric_time]) if metric == "percentage_metric" else "_".join(
        ["metric", metric, metric_type, metric_weight, metric_thresholds])
    return build_map(selected_metric, options, schools_options, selceted_region), fig #, generate_table(schools, "99%"), generate_table(stops, "99%"), new_button_ids, fig

@app.callback(
    [
        Output('dojazdy-info-table', 'children'),
        Output('dojazdy-info-table', 'style'),
        Output("dojazdy-csv-store", "data")
    ],
    [
        Input('dojazdy-info-button', 'n_clicks'),
        Input('metric-school-type', 'value'),
    ],
    [
        State('selected-region-indices', 'children')
    ])
def display_dojazdy_table(n_click, school_type, selceted_region):
    if n_click is None or n_click % 2 == 0:
        return html.Div(), {"display": "none"}, ""
    stop_numbers = []
    for i in selceted_region:
        if str(i) in stops_in_rejon:
            #return html.Div("Brak informacji"), {"display": "block"}
            for stop in stops_in_rejon[str(i)]:
                stop_numbers.append(int(stop))
        if str(i) in veturillo_in_rejon:
            for veturillo in veturillo_in_rejon[str(i)]:
                stop_numbers.append(int(veturillo))

    dojazdy = dojazdy_info.loc[np.isin(dojazdy_info.source_stop, stop_numbers)].sort_values("TOTAL_LEN")
    best_lens = dojazdy.groupby("school")["TOTAL_LEN"].min().rename(
        "best_len").reset_index(drop=False)
    dojazdy = dojazdy.merge(best_lens, on="school")
    df = dojazdy.loc[dojazdy.TOTAL_LEN == dojazdy.best_len]
    if school_type == "ALL":
        df = df.merge(schools_with_progi, left_on="school",
                  right_on="Numer szkoły")
    else:
        df = df.merge(schools_with_progi.loc[np.isin(schools_with_progi.Typ, SCHOOL_TYPE_MAPPING[school_type])], left_on="school",
                  right_on="Numer szkoły")
    df = df.merge(stops_name_info, left_on="source_stop", right_on="number")
    df = df.merge(stops_name_info, left_on="best_end_stop", right_on="number", how="left")
    df.loc[df.source_stop > 10000000, "name_x"] = "Punkt Veturilo"
    df.loc[df.best_end_stop > 10000000, "name_y"] = "Punkt Veturilo"

    df = df[["Nazwa", "name_x", "name_y", "PUBLIC", "WALK", "WAIT", "GETON", "LEN", "WALK_TO_SCHOOL", "TOTAL_LEN", "BIKE", "ONBIKE", "OFFBIKE"]] \
        .rename(columns={"Nazwa": "Nazwa szkoły", "name_x": "Najlepszy przystanek początkowy", "name_y": "Najlepszy przystanek końcowy",
                         "TOTAL_LEN": "Całkowita długość dojazdu", "LEN": "Czas dojazdu do przystanku końcowego", "PUBLIC": "Przejazdy komunikacją miejską",
                         "WALK": "Przejścia piesze", "WAIT": "Czas oczekiwania", "GETON": "Rezerwa na przesiadki", "WALK_TO_SCHOOL": "Czas dojścia do szkoły z przystanku końcowego",
                         "BIKE": "Czas podróży rowerem", "ONBIKE" : "Czas wypożyczania roweru", "OFFBIKE" : "Czas odstawiania roweru"})
    df = df.sort_values("Całkowita długość dojazdu")
    df.fillna("n/a", inplace=True)
    df = pd.DataFrame(np.where(df == np.inf, "n/a", df), columns=df.columns)
    df["Całkowita długość dojazdu"] = np.where(
        df["Całkowita długość dojazdu"] == "n/a", "powyżej 120 min", df["Całkowita długość dojazdu"])
    df = df.reset_index(drop=True).reset_index(
        drop=False).rename(columns={"index": "No."})
    df["No."] += 1
    dfto_stringify = df.copy()
    dfto_stringify.columns = [colname.replace(" ", "_") for colname in df.columns]
    return generate_static_table(df), {"display": "block"}, dfto_stringify.to_string(index=False) 

@ app.callback(
    [
        Output('schools-info-table', 'children'),
        Output('schools-info-table', 'style'),
        Output('stops-info-table', 'children'),
        Output('stops-info-table', 'style'),
        Output('all_button_ids', 'children'),
    ],
    [
        Input('schools-info-button', 'n_clicks'),
        Input('stops-info-button', 'n_clicks'),
        Input('metric-school-type', 'value'),
    ],
    [
        State('selected-region-indices', 'children'),
    ])
def display_schools_stops_table(schools_n_click, stops_n_click, school_type, selceted_region):
    stops = {}
    schools = {}
    stop_numbers = []
    new_button_ids = []
    stops_display, schools_display = {"display": "block"}, {"display": "block"}
    for i in selceted_region:
        reg_num = "Rejon numer: " + str(i)
        if stops_n_click is not None and stops_n_click % 2 == 1:
            try:
                stops[reg_num] = {}
                for stop in stops_in_rejon[str(i)]:
                    stop_numbers.append(int(stop))
                    stops[reg_num][stop] = {}
                    stop_df = stops_info.loc[stops_info["Unnamed: 0"] == str(
                        int(stop))]
                    if stop_df.empty:
                        stops[reg_num][stop]["Nazwa"] = f"N/A (numer {stop})"
                        stops[reg_num][stop]["Numer"] = "N/A"
                        stops[reg_num][stop]["Linie"] = {}
                        continue
                    stops[reg_num][stop]["Nazwa"] = stop_df["name"].values[0]
                    new_button_ids.append("button_id_" + stop_df["name"].values[0])
                    stops[reg_num][stop]["Numer"] = stop_df["Unnamed: 0"].values[0]
                    stops[reg_num][stop]["Linie"] = {}
                    for k, v in ast.literal_eval(stop_df["lines"].values[0]).items():
                        linia_num = "Linia numer: " + str(k)
                        stops[reg_num][stop]["Linie"][linia_num] = {}
                        stops[reg_num][stop]["Linie"][linia_num]["Informacje"] = {}
                        stops[reg_num][stop]["Linie"][linia_num]["Informacje"]["Nazwa"] = k
                        new_button_ids.append(
                            "button_id_" + k + stop_df["name"].values[0])
                        stops[reg_num][stop]["Linie"][linia_num]["Informacje"]["Typ"] = v["type"]
                        stops[reg_num][stop]["Linie"][linia_num]["Informacje"]["Godziny odjazdu"] = v["hours"]
                        stops[reg_num][stop]["Linie"][linia_num]["Informacje"]["Odjazd z przystanku"] = "Poza granicami Warszawy" if not stops_info.loc[stops_info["Unnamed: 0"] == str(
                            v["direction_from"])]["name"].values else stops_info.loc[stops_info["Unnamed: 0"] == str(v["direction_from"])]["name"].values[0]
                        stops[reg_num][stop]["Linie"][linia_num]["Informacje"]["Kierunek"] = "Poza granicami Warszawy" if not stops_info.loc[stops_info["Unnamed: 0"] == str(
                            v["direction_to"])]["name"].values else stops_info.loc[stops_info["Unnamed: 0"] == str(v["direction_to"])]["name"].values[0]
            except:
                stops[reg_num] = {}
        else:
            stops_display = {"display": "none"}
        if schools_n_click is not None and schools_n_click % 2 == 1:
            try:
                schools[reg_num] = {}
                for school in schools_in_rejon[str(i)]:
                    if school_type != 'ALL' and schools_with_progi.loc[schools_with_progi["Numer szkoły"] == school]["Typ"].values[0] not in SCHOOL_TYPE_MAPPING[school_type]:
                        continue
                    schools[reg_num][school] = schools_with_progi.loc[schools_with_progi["Numer szkoły"] == school].squeeze()
                    new_button_ids.append(
                        "button_id_" + schools_with_progi.loc[schools_with_progi["Numer szkoły"] == school]["Nazwa"].values[0])
            except:
                schools[reg_num] = {}
        else:
            schools_display = {"display": "none"}
    return generate_table(schools, "99%"), schools_display, generate_table(stops, "99%"), stops_display, new_button_ids

@app.callback(
    Output('schools-filters', 'style'),
    [
        Input('map-type-checklist', 'value')
    ])
def filter_update(selected_filters):
    if 'schools' in selected_filters:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    [
        Output('show-top-x-button', 'children'),
        Output('show-bottom-x-button', 'children'),
    ],
    [
        Input('show-top-x-interval', 'value'),
        Input('show-bottom-x-interval', 'value'),
        Input('show-top-x-button', 'n_clicks'),
        Input('show-bottom-x-button', 'n_clicks'),
    ])
def change_button_threshold(top, bottom, top_clicks, bottom_clicks):
    if top_clicks is None:
        top_clicks = 0
    if bottom_clicks is None:
        bottom_clicks = 0
    if top_clicks % 2 == 0 and bottom_clicks % 2 ==0:
        return f'Zaznacz górne {top}% rejonów', f'Zaznacz dolne {bottom}% rejonów'
    elif top_clicks % 2 == 0 and bottom_clicks % 2 == 1:
        return f'Zaznacz górne {top}% rejonów', f'Odznacz dolne {bottom}% rejonów'
    elif top_clicks % 2 == 1 and bottom_clicks % 2 == 0:
        return f'Odznacz górne {top}% rejonów', f'Zaznacz dolne {bottom}% rejonów'
    elif top_clicks % 2 == 1 and bottom_clicks % 2 == 1:
        return f'Odznacz górne {top}% rejonów', f'Odznacz dolne {bottom}% rejonów'

@app.callback(
    [
        Output('metric-weight', 'style'),
        Output('plaintext-time', 'style'),
        Output('metric-time', 'style'),
        Output('plaintext-thresholds', 'style'),
        Output('metric-thresholds', 'style')
    ],
    [
        Input('metric', 'value')
    ])
def metric_update(selected_metric):
    if selected_metric == "percentage_metric":
        return {'display': 'none'}, \
            {'display': 'inline-block', 'fontSize': '12pt'}, \
            {'width': 170, 'display': 'inline-block', 'verticalAlign': "middle", 'textAlign': "left"}, \
            {'display': 'none'}, \
            {'display': 'none'}
    else:
        return {'width': 110, 'display': 'inline-block', 'verticalAlign': "middle", 'textAlign': "left"}, \
            {'display': 'none'}, \
            {'display': 'none'}, \
            {'display': 'inline-block', 'fontSize': '12pt'}, \
            {'width': 170, 'display': 'inline-block',
             'verticalAlign': "middle", 'textAlign': "left"}

@app.callback(
    [
        Output('hist-interval-output', 'children'),
        Output('widelki-selection', 'children'),
    ],
    [
        Input('hist-interval', 'value'),
    ])
def change_interval(hist_interval):
    values = list(range(0, 120, hist_interval))[1:] + [120]
    return f'Podziałka histogramu: {hist_interval} minut', str(values)

@app.callback(
    [
        Output('metric-values-table', 'children'),
        Output('region_numbers_sorted_by_metric', 'children')
    ],
    [
        Input('metric', 'value'),
        Input('metric-weight', 'value'),
        Input('metric-school-type', 'value'),
        Input('metric-time', 'value'),
        Input('metric-thresholds', 'value'),
        Input('metric', 'value')
    ])
def generate_metric_table(metric, metric_weight, metric_type, metric_time, metric_thresholds, selected_metric):
    selected_metric = "_".join(["metric", metric, metric_type, metric_time]) if metric == "percentage_metric" else "_".join(
        ["metric", metric, metric_type, metric_weight, metric_thresholds])
    selected_metric += ".csv"
    metric_values = pd.read_csv(
        f'assets/metrics/{selected_metric}', index_col=0)
    metric_values.rename(columns={
                         "index": "Numer rejonu", "accessibility_index": "Wartość metryki"}, inplace=True)
    metric_values = metric_values.loc[metric_values["Wartość metryki"] != -1]
    metric_values.sort_values("Wartość metryki", inplace=True, ascending=False)
    if "percentage" in selected_metric:
        metric_values["Wartość metryki"] = np.round(
            metric_values["Wartość metryki"]*100, decimals=2).astype(str) + "%"
    else:
        metric_values["Wartość metryki"] = np.round(
            metric_values["Wartość metryki"], decimals=3)
    return generate_almost_static_table(metric_values), list(metric_values["Numer rejonu"])


if __name__ == '__main__':
    app.run_server(debug=True)


# %%
