# -*- coding: utf-8 -*-
import dash
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
from dash_html_components.Div import Div
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

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# LOAD DATA
with open(os.path.join(THIS_FOLDER, 'assets', 'stops_in_rejon.json'), encoding='utf8') as json_file:
    stops_in_rejon = json.load(json_file)

with open(os.path.join(THIS_FOLDER, 'assets', 'schools_in_rejon.json'), encoding='utf8') as json_file:
    schools_in_rejon = json.load(json_file)

schools_with_progi = pd.read_csv(os.path.join(THIS_FOLDER, 'assets', 'schools_with_progi.csv'))

METRIC_MAPPING = [
    {'label' : 'metric_new_metric_all_30', 'value' : 'metric_new_metric_all_30'},
    {'label' : 'metric_percentage_all_30', 'value' : 'metric_percentage_all_30'},
    {'label' : 'metric_new_metric_Liceumogólnokształcące Szkołapodstawowa_weight-False_thresholds-False', 'value' : 'metric_new_metric_Liceumogólnokształcące Szkołapodstawowa_weight-False_thresholds-False'},
    {'label' : 'metric_new_metric_Liceumogólnokształcące Szkołapodstawowa_weight-False_thresholds-True', 'value' : 'metric_new_metric_Liceumogólnokształcące Szkołapodstawowa_weight-False_thresholds-True'},
    {'label' : 'metric_new_metric_Liceumogólnokształcące Szkołapodstawowa_weight-True_thresholds-False', 'value' : 'metric_new_metric_Liceumogólnokształcące Szkołapodstawowa_weight-True_thresholds-False'},
    {'label' : 'metric_new_metric_Liceumogólnokształcące Szkołapodstawowa_weight-True_thresholds-True', 'value' : 'metric_new_metric_Liceumogólnokształcące Szkołapodstawowa_weight-True_thresholds-True'},
    {'label' : 'metric_new_metric_Liceumogólnokształcące_weight-False_thresholds-False', 'value' : 'metric_new_metric_Liceumogólnokształcące_weight-False_thresholds-False'},
    {'label' : 'metric_new_metric_Liceumogólnokształcące_weight-False_thresholds-True', 'value' : 'metric_new_metric_Liceumogólnokształcące_weight-False_thresholds-True'},
    {'label' : 'metric_new_metric_Liceumogólnokształcące_weight-True_thresholds-False', 'value' : 'metric_new_metric_Liceumogólnokształcące_weight-True_thresholds-False'},
    {'label' : 'metric_new_metric_Liceumogólnokształcące_weight-True_thresholds-True', 'value' : 'metric_new_metric_Liceumogólnokształcące_weight-True_thresholds-True'},
    {'label' : 'metric_new_metric_Szkołapodstawowa_weight-False_thresholds-False', 'value' : 'metric_new_metric_Szkołapodstawowa_weight-False_thresholds-False'},
    {'label' : 'metric_new_metric_Szkołapodstawowa_weight-False_thresholds-True', 'value' : 'metric_new_metric_Szkołapodstawowa_weight-False_thresholds-True'},
    {'label' : 'metric_new_metric_Szkołapodstawowa_weight-True_thresholds-False', 'value' : 'metric_new_metric_Szkołapodstawowa_weight-True_thresholds-False'},
    {'label' : 'metric_new_metric_Szkołapodstawowa_weight-True_thresholds-True', 'value' : 'metric_new_metric_Szkołapodstawowa_weight-True_thresholds-True'},
    {'label' : 'metric_percentage_metric_Liceumogólnokształcące Szkołapodstawowa_time-15', 'value' : 'metric_percentage_metric_Liceumogólnokształcące Szkołapodstawowa_time-15'},
    {'label' : 'metric_percentage_metric_Liceumogólnokształcące Szkołapodstawowa_time-30', 'value' : 'metric_percentage_metric_Liceumogólnokształcące Szkołapodstawowa_time-30'},
    {'label' : 'metric_percentage_metric_Liceumogólnokształcące Szkołapodstawowa_time-60', 'value' : 'metric_percentage_metric_Liceumogólnokształcące Szkołapodstawowa_time-60'},
    {'label' : 'metric_percentage_metric_Liceumogólnokształcące Szkołapodstawowa_time-90', 'value' : 'metric_percentage_metric_Liceumogólnokształcące Szkołapodstawowa_time-90'},
    {'label' : 'metric_percentage_metric_Liceumogólnokształcące_time-15', 'value' : 'metric_percentage_metric_Liceumogólnokształcące_time-15'},
    {'label' : 'metric_percentage_metric_Liceumogólnokształcące_time-30', 'value' : 'metric_percentage_metric_Liceumogólnokształcące_time-30'},
    {'label' : 'metric_percentage_metric_Liceumogólnokształcące_time-60', 'value' : 'metric_percentage_metric_Liceumogólnokształcące_time-60'},
    {'label' : 'metric_percentage_metric_Liceumogólnokształcące_time-90', 'value' : 'metric_percentage_metric_Liceumogólnokształcące_time-90'},
    {'label' : 'metric_percentage_metric_Szkołapodstawowa_time-15', 'value' : 'metric_percentage_metric_Szkołapodstawowa_time-15'},
    {'label' : 'metric_percentage_metric_Szkołapodstawowa_time-30', 'value' : 'metric_percentage_metric_Szkołapodstawowa_time-30'},
    {'label' : 'metric_percentage_metric_Szkołapodstawowa_time-60', 'value' : 'metric_percentage_metric_Szkołapodstawowa_time-60'},
    {'label' : 'metric_percentage_metric_Szkołapodstawowa_time-90', 'value' : 'metric_percentage_metric_Szkołapodstawowa_time-90'},
]


app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    './styles.css',
])

server = app.server


def generate_table(dict, width):
    return html.Div([html.Table(
        # Header
        [html.Tr([html.Th(col, style={
            "border": "1px solid black",
            'text-align' : 'center'
        }) for col in dict.keys()]
        )] +
        # Body
        [html.Tr(
        [html.Td([
                html.Table(
                [html.Tr([html.Th(row["Nazwa"])], style={
                        "border": "1px solid black",
                    })] +
                    # Body
                    [html.Tr([
                        html.Td(index, style={"border": "1px solid black"}),
                        html.Td(value, style={"border": "1px solid black"})
                    ], style={
                        "border": "1px solid black"
                    }) for index, value in row.items()]
            ) for _, row in dict[col].items()
        ], style={
            "border": "1px solid black",
            'vertical-align' : 'top',
            'width' : width
        }
        ) for col in dict.keys()])]
    )            ], style={
                'height' : '500px',
                'width' : width,
                'overflow' : 'scroll'
            }
        )


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
                                   'display' : 'block'
                               }
                           ),
                           dbc.Row(
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
                                   'display' : 'none'
                               }
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
                                       children=[
                                           html.Div(
                                               children=[
                                                   dbc.Row(
                                                       html.Plaintext(
                                                           "Informacje o przystankach",
                                                           style={
                                                               'font': '14pt Arial Black',
                                                               'margin': "0px 0px 0px 35px",
                                                           }
                                                       )
                                                   ),
                                                   dbc.Row(
                                                       id="stops-info-table",
                                                       style={
                                                           'margin': "0px 0px 0px 35px",
                                                           'width': '100%',
                                                       }
                                                   )
                                               ],
                                               style={
                                                   'border': '1px solid black',
                                                    'float': 'left',
                                                    'width': '30%',
                                               }
                                           ),
                                           html.Div(
                                               children=[
                                                   dbc.Row(
                                                       html.Plaintext(
                                                           "Informacje o szkołach",
                                                           style={
                                                               'font': '14pt Arial Black',
                                                               'margin': "0px 0px 0px 35px",
                                                           }
                                                       )
                                                   ),
                                                   dbc.Row(
                                                       id="schools-info-table",
                                                       style={
                                                           'margin': "0px 0px 0px 35px",
                                                           'width': '100%',
                                                       }
                                                   ),
                                                   
                                               ],
                                               style={
                                                   'border': '1px solid black',
                                                    'float': 'left',
                                                    'width': '70%',
                                               }
                                           )
                                       ],
                                       style={
                                           'border': '1px solid black',
                                           'overflow': 'hidden',
                                       }
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
                                                   value='metric_new_metric_all_30',
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
        Output('schools-info-table', 'children'),
        Output('stops-info-table', 'children'),
    ],
    [
        Input('metric', 'value'),
        Input('map-type-checklist', 'value'),
        Input('school-type-checklist', 'value'),
        Input('selected-region-indices', 'children'),
    ])
def update_map(metric, options,schools_options, selceted_region):
    stops = {}
    schools = {}
    for i in selceted_region:
        try:
            stops[i] = {}
            for stop in stops_in_rejon[str(i)]:
                stops[i][stop] = pd.Series({"Nazwa": "n/a", "nr": stop})
        except:
            stops[i] = {}
        try:
            schools[i] = {} 
            for school in schools_in_rejon[str(i)]:
                schools[i][school] = schools_with_progi.iloc[school] 
        except:
            schools[i] = {}

    return build_map(metric, options, schools_options, selceted_region), generate_table(schools, "820px"), generate_table(stops, "340px")

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
