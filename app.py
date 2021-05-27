# -*- coding: utf-8 -*-
import dash
from dash_bootstrap_components._components.Row import Row
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from plotly.graph_objs.layout import Margin
from map_helper import build_map
import os
from joblib import load
import visdcc
import base64
import json

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# LOAD DATA
with open(os.path.join(THIS_FOLDER, 'assets', 'stops_in_rejon.json'), encoding='utf8') as json_file:
    stops_in_rejon = json.load(json_file)

METRIC_MAPPING = [
    {'label': 'procentowa dostępność w czasie', 'value': 'pdwc'},
    {'label': 'metryka Maćkowa', 'value': 'mm'}
]

map_type_options = ['Active companies', '% of terminated companies']
external_scripts = [
    'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js'
]
# Treemap init

app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    './styles.css',
], external_scripts=external_scripts)

server = app.server


def generate_table(dataframe, max_rows=26):
    return html.Table(
        # Header
        [html.Tr([html.Th(col, style={
            "border" : "1px solid black"
        }) for col in dataframe.columns],style={
            "border" : "1px solid black"
        })] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col],style={
            "border" : "1px solid black"
        }) for col in dataframe.columns
        ],style={
            "border" : "1px solid black"
        }) for i in range(min(len(dataframe), max_rows))],
        style={
            "border" : "1px solid black"
        }
    )


df = pd.DataFrame({"asd": [2, 21], "asdf": [3, 5]})

app.layout = html.Div(
    children=[
        html.Section(
            id='map-section',
            children=html.Div(
               className='screen-height',
               children=[
                   html.Div(
                       className='section',
                       children=[
                           dbc.Row(
                               id='map-filters',
                               no_gutters=True,
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
                               ]
                           ),
                           dbc.Row(
                               className='top',
                               no_gutters=True,
                               children=[
                                   dbc.Col(md=6,
                                           className='box',
                                           children=[
                                               dcc.Graph(
                                                   id='map',
                                                   className='fill-height',
                                                   config={
                                                       'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
                                                       'scrollZoom': True
                                                   },
                                               ),
                                               html.Div(id="output")
                                           ]
                                           ),
                                   dbc.Col(
                                       generate_table(df),
                                       style={
                                           'margin': "0px 0px 0px 30px"
                                       },
                                       id="info-table"
                                   )
                               ]),
                           dbc.Row(
                               className='bottom',
                               children=[
                                   dbc.Col(md=6,
                                           className='box',
                                           children=[
                                               dcc.Dropdown(
                                                   id='metric',
                                                   options=METRIC_MAPPING,
                                                   value='mm',
                                               )
                                           ]
                                           )
                               ]
                           ),
                           html.Div(id='selected-region',
                                    style={'display': 'none'}, children=''),
                           html.Div(id='selected-region-indices',
                                    style={'display': 'none'}, children=''),
                           html.Div(id='scroll-blocker',
                                    className='scroll')
                       ]
                   ),
               ]
            )

        )
    ]
)


@app.callback(
    [
        Output('map', 'figure'),
        Output('info-table', 'children'),
    ],
    [
        Input('metric', 'value'),
        Input('map-type-checklist', 'value'),
        Input('selected-region-indices', 'children'),
    ])
def update_map(metric, options, selceted_region):
    stops = {}
    max_len = 0
    for i in selceted_region:
        if str(i) not in stops_in_rejon:
            stops[i] = []
            continue
        stops[i] = stops_in_rejon[str(i)]
        if len(stops_in_rejon[str(i)]) > max_len:
            max_len = len(stops_in_rejon[str(i)])
    #print("outer dupa",stops)
    for k,v in stops.items():
        v.extend([""]*(max_len-len(v)))
#        print("inner dupa",stops)

    return build_map(metric, options, selceted_region), generate_table(pd.DataFrame(stops))


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
