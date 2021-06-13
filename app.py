# -*- coding: utf-8 -*-
# %%
import dash
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
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
import visdcc
import base64
import json
import math
import ast

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# LOAD DATA
with open(os.path.join(THIS_FOLDER, 'assets', 'stops_in_rejon.json'), encoding='utf8') as json_file:
    stops_in_rejon = json.load(json_file)

with open(os.path.join(THIS_FOLDER, 'assets', 'schools_in_rejon.json'), encoding='utf8') as json_file:
    schools_in_rejon = json.load(json_file)

schools_with_progi = pd.read_csv(os.path.join(
    THIS_FOLDER, 'assets', 'schools_with_progi.csv'))

stops_info = pd.read_csv(os.path.join(
    THIS_FOLDER, 'assets', 'stops_info.csv'), encoding='utf-8')
stops_info = stops_info.astype({'Unnamed: 0': 'str'})

dojazdy_info = pd.read_csv(os.path.join(
    THIS_FOLDER, 'assets', 'best_stats.csv'), encoding='utf-8', index_col=0)

dojazdy_info.fillna(float("inf"), inplace=True)

METRIC_MAPPING = [
    {'label': 'nowa', 'value': 'new_metric'},
    {'label': 'procentowa', 'value': 'percentage_metric'}
]

# schools_with_progi_with_S = schools_with_progi
# schools_with_progi_with_S['Id'] = np.char.add(
#     'S', schools_with_progi_with_S.Numer.astype(int))
schools_with_progi_Num_Type = schools_with_progi.loc[:, ['Numer', 'Typ']]

dojazdy_merged = schools_with_progi_Num_Type.merge(
    dojazdy_info, left_on='Numer', right_on='school')

button_names = []
# %%
METRIC_SCHOOL_TYPE_MAPPING = [
    {'label': 'dowolnych szkół', 'value': 'ALL'},
    {'label': 'szkół podstawowych', 'value': 'POD'},
    {'label': 'liceów ogólnokształcących', 'value': 'LIC'},
    {'label': 'techników', 'value': 'TEC'},
    {'label': 'szkół zawodowych', 'value': 'ZAW'},
    {'label': 'szkół podstawowych i zawodowych oraz liceów i techników',
        'value': 'POD-LIC-ZAW-TEC'},
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
        'height': '96%',
        'overflow-y': 'scroll',
        'overflow': 'scroll',
        'margin': '0px 5px 0px 0px'
    }
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
                                       'Filtry:'),
                                   dcc.Checklist(
                                       id='map-type-checklist',
                                       labelClassName='map-type-checklist-items',
                                       options=[
                                           {'label': 'Przystanki',
                                            'value': 'stops'},
                                           {'label': 'Szkoły',
                                            'value': 'schools'},
                                           {'label': 'Metro',
                                            'value': 'subway'}
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
                                       'Filtry szkoły:'),
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
                                            'value': 'school_tech'}
                                       ],
                                       value=['all']
                                   )
                               ],
                               style={
                                   'display': 'none'
                               }
                           ),
                           html.Div(children=[
                               html.Div(
                                   children=[
                                       dcc.Graph(
                                           id='map',
                                           className='fill-height',
                                           config={
                                               'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
                                               'scrollZoom': False
                                           },
                                           style={"height": "100%"}
                                       ),
                                       html.Div(id="output")
                                   ], style={'max-height': '100%', 'width': '35%'}
                               ),
                               html.Div(
                                   children=[
                                       html.Div(
                                           children=[
                                               html.Div(
                                                   html.Plaintext(
                                                       "Informacje o przystankach",
                                                       style={
                                                           'font': '14pt Arial Black',
                                                           'margin': "0px 0px 0px 15px",
                                                       }
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
                                               'height': '100%'
                                           }
                                       ),
                                       html.Div(
                                           children=[
                                               html.Div(
                                                   html.Plaintext(
                                                       "Informacje o szkołach",
                                                       style={
                                                           'font': '14pt Arial Black',
                                                           'margin': "0px 0px 0px 15px",
                                                       }
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
                                               'height': '100%'
                                           }
                                       )
                                   ],
                                   style={
                                       'border': '1px solid black',
                                       'height': '100%',
                                       'max-height': '100%',
                                       'width': '65%'
                                   })
                           ], style={"height": "60%", "display": "flex"}),
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
                            [
                                html.Plaintext(id='hist-interval-output', style={
                                    'display': 'inline-block', 'fontSize': '12pt'}),
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
                                ),
                            ],
                            style={"display": "grid", "grid-template-columns": "20% 80%"}),
                           html.Div(
                               children=[
                                   html.Div(children=[
                                       dcc.Graph(
                                           id='histogram',
                                           config={
                                               'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
                                               'scrollZoom': False
                                           },
                                           style={"height": "100%"}
                                       ),
                                   ]),
                                   html.Div(
                                       children=[
                                           html.Div(
                                               html.Button(
                                                   "Wyświetl informacje dojazdowe",
                                                   style={
                                                       'font': '14pt Arial Black',
                                                               'margin': "0px 0px 0px 15px",
                                                   },
                                                   id="dojazdy-info-button"
                                               )
                                           ),
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
                                           'height': '100%'
                                       }
                                   )
                               ], style={"display": "flex", "height": "30%"}
                           ),
                           html.Div("[10,20,30,40,50,60,70,80,90,100,110,120]",
                                    id='widelki-selection', style={'display': 'none'}),
                           html.Div(id='selected-region',
                                    style={'display': 'none'}, children=''),
                           html.Div(id='selected-region-indices',
                                    style={'display': 'none'}, children=''),
                           html.Div(id='scroll-blocker',
                                    className='scroll'),
                           html.Div(id='all_button_ids',
                                    style={'display': 'none'}),
                           html.Div(id='dojazdy_button_ids',
                                    style={'display': 'none'}),
                           html.Div(id='empty', style={'display': 'none'}),
                           html.Div(id='empty2', style={'display': 'none'})
                       ]
                   ),
               ]
            )
        )
    ]
)

app.clientside_callback(
    """
    function setup_stuff(ids) {
        for (let i = 0; i < ids.length; i++) {
            var collapse_button = document.getElementById("collapse_button_" + ids[i].substring(10));
            collapse_button.addEventListener("click", collapse, false);
        }
        console.log("asd")
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
    function setup_stuff(ids) {
        for (let i = 0; i < ids.length; i++) {
            var collapse_button = document.getElementById("collapse_button_" + ids[i].substring(10));
            collapse_button.addEventListener("click", collapse, false);
        }
        console.log("asd")
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
    [Output("empty2", "children")],
    [
        Input("dojazdy_button_ids", "children"),
    ]
)


@ app.callback(
    [
        Output('map', 'figure'),
        Output('schools-info-table', 'children'),
        Output('stops-info-table', 'children'),
        Output('all_button_ids', 'children'),
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
    stops={}
    schools={}
    stop_numbers=[]
    new_button_ids=[]
    for i in selceted_region:
        reg_num="Rejon numer: " + str(i)
        try:
            stops[reg_num]={}
            for stop in stops_in_rejon[str(i)]:
                stop_numbers.append(int(stop))
                stops[reg_num][stop]={}
                stop_df=stops_info.loc[stops_info["Unnamed: 0"] == str(
                    int(stop))]
                if stop_df.empty:
                    stops[reg_num][stop]["Nazwa"]=f"N/A (numer {stop})"
                    stops[reg_num][stop]["Numer"]="N/A"
                    stops[reg_num][stop]["Linie"]={}
                    continue
                stops[reg_num][stop]["Nazwa"]=stop_df["name"].values[0]
                new_button_ids.append("button_id_" + stop_df["name"].values[0])
                stops[reg_num][stop]["Numer"]=stop_df["Unnamed: 0"].values[0]
                stops[reg_num][stop]["Linie"]={}
                for k, v in ast.literal_eval(stop_df["lines"].values[0]).items():
                    linia_num="Linia numer: " + str(k)
                    stops[reg_num][stop]["Linie"][linia_num]={}
                    stops[reg_num][stop]["Linie"][linia_num]["Informacje"]={}
                    stops[reg_num][stop]["Linie"][linia_num]["Informacje"]["Nazwa"]=k
                    new_button_ids.append(
                        "button_id_" + k + stop_df["name"].values[0])
                    stops[reg_num][stop]["Linie"][linia_num]["Informacje"]["Typ"]=v["type"]
                    stops[reg_num][stop]["Linie"][linia_num]["Informacje"]["Godziny odjazdu"]=v["hours"]
                    stops[reg_num][stop]["Linie"][linia_num]["Informacje"]["Odjazd z przystanku"]="Poza granicami Warszawy" if not stops_info.loc[stops_info["Unnamed: 0"] == str(
                        v["direction_from"])]["name"].values else stops_info.loc[stops_info["Unnamed: 0"] == str(v["direction_from"])]["name"].values[0]
                    stops[reg_num][stop]["Linie"][linia_num]["Informacje"]["Kierunek"]="Poza granicami Warszawy" if not stops_info.loc[stops_info["Unnamed: 0"] == str(
                        v["direction_to"])]["name"].values else stops_info.loc[stops_info["Unnamed: 0"] == str(v["direction_to"])]["name"].values[0]
        except:
            stops[reg_num]={}
        try:
            schools[reg_num] = {}
            for school in schools_in_rejon[str(i)]:
                schools[reg_num][school] = schools_with_progi.loc[schools_with_progi.Numer == school].squeeze()
                new_button_ids.append(
                    "button_id_" + schools_with_progi.loc[schools_with_progi.Numer == school]["Nazwa"].values[0])
        except:
            schools[reg_num] = {}


    widelki = np.array([]) if widelki_string is None else np.array(
        eval(widelki_string))
    widelki_labels = gen_widelki_labels(widelki)
    
    if metric_type != 'ALL':
        school_types = []
        for part in metric_type.split('-'):
            school_types += SCHOOL_TYPE_MAPPING[part]
        
        dojazdy_merged_filtered = dojazdy_merged.loc[np.isin(dojazdy_merged.Typ, school_types)]
    else:
        dojazdy_merged_filtered = dojazdy_merged

    if len(selceted_region) > 0:
        dojazdy = np.array(dojazdy_merged_filtered.loc[np.isin(
            dojazdy_merged_filtered.source_stop, stop_numbers)]["TOTAL_LEN"])
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
    
    if len(dojazdy) > 0:
        dojazdy_no_inf = dojazdy
        dojazdy_no_inf[np.isinf(dojazdy)] = 120

        mean_value = dojazdy_no_inf.mean()
        fig.add_vline(x=convert_number_to_hist_x(widelki, mean_value), 
                    line_dash="dot",
                    line_color="#d80000",
                    annotation_text=f"Średnia: {round(mean_value, 2)} minuty", 
                    annotation_position="top right",
                    annotation_font_size=12,
                    annotation_font_color="#d80000"
                )

    selected_metric = "_".join(["metric", metric, metric_type, metric_time]) if metric == "percentage_metric" else "_".join(
        ["metric", metric, metric_type, metric_weight, metric_thresholds])
    return build_map(selected_metric, options, schools_options, selceted_region), generate_table(schools, "99%"), generate_table(stops, "99%"), new_button_ids, fig


@app.callback(
    [
        Output('dojazdy-info-table', 'children'),
        Output('dojazdy-info-table', 'style'),
        Output('dojazdy_button_ids', 'children')
    ],
    [
        Input('dojazdy-info-button', 'n_clicks'),
        Input('widelki-selection', 'children'),
    ],
    [
        State('selected-region-indices', 'children')
    ])
def display_dojazdy_table(n_click, widelki_string, selceted_region):
    if n_click is None or n_click % 2 == 0:
        return html.Div(), {"display": "none"}, []

    new_button_ids = []
    stop_numbers = []
    for i in selceted_region:
        for stop in stops_in_rejon[str(i)]:
            stop_numbers.append(int(stop))

    widelki = np.array([]) if widelki_string is None else np.array(
        eval(widelki_string))
    widelki_labels = gen_widelki_labels(widelki)
    
    dojazdy = {}
    for v in widelki_labels.values():
        dojazdy[v] = {}
    for i, dojazd in dojazdy_info.loc[np.isin(dojazdy_info.source_stop, stop_numbers)].iterrows():
        proper_widelek = np.sum(dojazd["TOTAL_LEN"] >= np.array(widelki))
        new_button_ids.append("button_id_" + dojazd["school"])
        dojazdy[widelki_labels[proper_widelek]][dojazd["school"]] = {}
        dojazdy[widelki_labels[proper_widelek]
                ][dojazd["school"]]["Nazwa"] = dojazd["school"]
        dojazdy[widelki_labels[proper_widelek]][dojazd["school"]
                                                ]["Czas dojazdu"] = dojazd["TOTAL_LEN"]

    return generate_table(dojazdy, "99%"), {"display": "block"}, new_button_ids


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
        Output('selected-region', 'children'),
        Output('selected-region-indices', 'children')
    ],
    [
        Input('map', 'selectedData')
    ])
def select_region(selectedregion):
    if selectedregion is None:
        return [], []
    selected_region = [item['location'] for item in selectedregion['points']]
    selected_region_indices = [item['pointIndex']
                               for item in selectedregion['points']]
    return selected_region, selected_region_indices


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


if __name__ == '__main__':
    app.run_server(debug=True)


# %%
