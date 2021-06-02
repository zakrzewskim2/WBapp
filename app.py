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

schools_with_progi = pd.read_csv(os.path.join(
    THIS_FOLDER, 'assets', 'schools_with_progi.csv'))

METRIC_MAPPING = [
    {'label': 'nowa', 'value': 'new_metric'},
    {'label': 'procentowa', 'value': 'percentage_metric'}
]

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


def generate_table(dict, width):
    return html.Div([html.Table(
        # Header
        [html.Tr([html.Th(col, style={
            "border": "1px solid black",
            'text-align': 'center'
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
                'vertical-align': 'top',
                'width': width
            }
            ) for col in dict.keys()])]
    )], style={
        'height': '500px',
        'width': width,
        'overflow': 'scroll'
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
                                   'display': 'block'
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
                                   'display': 'none'
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
                                                       'scrollZoom': False
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
                                   html.Plaintext("Typ metryki ", style={
                                       'display': 'inline-block', 'font-size': '12pt'}),
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
                                       'display': 'inline-block', 'font-size': '12pt'}),
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
    selected_metric = "_".join(["metric", metric, metric_type, metric_time]) if metric == "percentage_metric" else "_".join(["metric", metric, metric_type, metric_weight, metric_thresholds])
    return build_map(selected_metric, options, schools_options, selceted_region), generate_table(schools, "820px"), generate_table(stops, "340px")


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
                {'display': 'inline-block', 'font-size': '12pt'}, \
                {'width': 170, 'display': 'inline-block', 'verticalAlign': "middle", 'textAlign': "left"}, \
                {'display': 'none'}, \
                {'display': 'none'}
    else:
        return {'width': 110, 'display': 'inline-block', 'verticalAlign': "middle", 'textAlign': "left"}, \
                {'display': 'none'}, \
                {'display': 'none'}, \
                {'display': 'inline-block', 'font-size': '12pt'}, \
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

