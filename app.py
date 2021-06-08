# -*- coding: utf-8 -*-
#%%
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
from numpy.lib.shape_base import column_stack
import pandas as pd
import numpy as np
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
stops_info = stops_info.astype({'Unnamed: 0':'str'})

METRIC_MAPPING = [
    {'label': 'nowa', 'value': 'new_metric'},
    {'label': 'procentowa', 'value': 'percentage_metric'}
]

button_names = []
#%%
METRIC_SCHOOL_TYPE_MAPPING = [
    {'label': 'dowolnych szkół', 'value': 'ALL'},
    {'label': 'szkół podstawowych', 'value': 'POD'},
    {'label': 'liceów ogólnokształcących', 'value': 'LIC'},
    {'label': 'techników', 'value': 'TEC'},
    {'label': 'szkół zawodowych', 'value': 'ZAW'},
    {'label': 'szkół podstawowych i zawodowych oraz liceów i techników', 'value': 'POD-LIC-ZAW-TEC'},
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
                                html.Button(row["Nazwa"], style={"width":"100%"}, id="collapse_button_" + row["Nazwa"] + name), style={
                                    "border": "1px solid black",
                                    'textAlign': 'center'},
                                colSpan=2
                            )
                        )
                    )] +
                    # Body
                    [html.Tbody([html.Tr([
                        html.Td(index, style={"border": "1px solid black", "verticalAlign" : "top"}),
                        generate_table(value, "auto", row["Nazwa"]) if type(value) is dict else html.Td(value)
                    ], style={
                        "border": "1px solid black"
                    }) for index, value in row.items()], style={'display' : 'none', 'width' : '100%'}, id="table_to_collapse_"  + row["Nazwa"] + name)]
                ) for _, row in df_dict[col].items()
            ], style={
                "border": "1px solid black",
                'verticalAlign': 'top',
                'width': width
            }
            ) for col in df_dict.keys()])])]
    )], style={
        'width': width,
        'height': '96%',
        'overflow-y': 'scroll',
        'overflow': 'scroll',
        'margin' : '0px 5px 0px 0px'
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
                                                   style={"height" : "100%"}
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
                                                           'height' : '100%'
                                                       }
                                                   )
                                               ],
                                               style={
                                                   'border': '1px solid black',
                                                   'float': 'left',
                                                   'width': '50%',
                                                   'height' : '100%'
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
                                                           'height' : '100%'
                                                       }
                                                   ),

                                               ],
                                               style={
                                                   'border': '1px solid black',
                                                   'float': 'left',
                                                   'width': '50%',
                                                   'height' : '100%'
                                               }
                                           )
                                       ],
                                       style={
                                           'border': '1px solid black',
                                           'height' : '100%',
                                           'max-height': '100%',
                                           'width' : '65%'
                                       })     
                           ], style={"height":"60%", "display": "flex"}),
                           html.Div(
                               className='bottom',
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

                                   html.Plaintext(", dostępnych w czasie nie większym niż ", id="plaintext-time"),
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
                                    html.Plaintext(" progi.", id="plaintext-thresholds", style=dict(display='none'))
                               ]
                           ),
                           html.Div(id='selected-region',
                                    style={'display': 'none'}, children=''),
                           html.Div(id='selected-region-indices',
                                    style={'display': 'none'}, children=''),
                           html.Div(id='scroll-blocker',
                                    className='scroll'),
                           html.Div(id='all_button_ids', style={'display': 'none'}),
                           html.Div(id='empty', style={'display': 'none'})
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

@app.callback(
    [
        Output('map', 'figure'),
        Output('schools-info-table', 'children'),
        Output('stops-info-table', 'children'),
        Output('all_button_ids', 'children'),
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
    ])
def update_map(metric, metric_weight, metric_type, metric_time, metric_thresholds, options, schools_options, selceted_region):
    stops = {}
    schools = {}
    new_button_ids = []
    for i in selceted_region:
        try:
            stops[i] = {}
            for stop in stops_in_rejon[str(i)]:
                stops[i][stop] = {}
                stop_df = stops_info.loc[stops_info["Unnamed: 0"] == str(stop).zfill(4)]
                if stop_df.empty:
                    stops[i][stop]["Nazwa"] = f"N/A (numer {stop})"
                    stops[i][stop]["Numer"] = "N/A"
                    stops[i][stop]["Linie"] = {}
                    continue
                stops[i][stop]["Nazwa"] = stop_df["name"].values[0]
                new_button_ids.append("button_id_" + stop_df["name"].values[0])
                stops[i][stop]["Numer"] = stop_df["Unnamed: 0"].values[0]
                stops[i][stop]["Linie"] = {}
                for k,v in ast.literal_eval(stop_df["lines"].values[0]).items():
                    stops[i][stop]["Linie"][k] = {}
                    stops[i][stop]["Linie"][k]["Informacje"] = {}
                    stops[i][stop]["Linie"][k]["Informacje"]["Nazwa"] = k
                    new_button_ids.append("button_id_" + k + stop_df["name"].values[0])
                    stops[i][stop]["Linie"][k]["Informacje"]["Typ"] = v["type"]
                    stops[i][stop]["Linie"][k]["Informacje"]["Godziny odjazdu"] = v["hours"]
                    stops[i][stop]["Linie"][k]["Informacje"]["Odjazd z przystanku"] = "Poza granicami Warszawy" if not stops_info.loc[stops_info["Unnamed: 0"]==str(v["direction_from"])]["name"].values else stops_info.loc[stops_info["Unnamed: 0"]==str(v["direction_from"])]["name"].values[0]
                    stops[i][stop]["Linie"][k]["Informacje"]["Kierunek"] = "Poza granicami Warszawy" if not stops_info.loc[stops_info["Unnamed: 0"]==str(v["direction_to"])]["name"].values else stops_info.loc[stops_info["Unnamed: 0"]==str(v["direction_to"])]["name"].values[0]
        except:
            stops[i] = {}
        try:
            schools[i] = {}
            for school in schools_in_rejon[str(i)]:
                schools[i][school] = schools_with_progi.iloc[school]
                new_button_ids.append("button_id_" + schools_with_progi.iloc[school]["Nazwa"])
        except:
            schools[i] = {}

    selected_metric = "_".join(["metric", metric, metric_type, metric_time]) if metric == "percentage_metric" else "_".join(["metric", metric, metric_type, metric_weight, metric_thresholds])
    return build_map(selected_metric, options, schools_options, selceted_region), generate_table(schools, "99%"), generate_table(stops, "99%"), new_button_ids


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
                {'width': 170, 'display': 'inline-block', 'verticalAlign': "middle", 'textAlign': "left"}

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


if __name__ == '__main__':
    app.run_server(debug=True)
#%%

