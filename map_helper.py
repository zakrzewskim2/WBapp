import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import json

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(THIS_FOLDER, 'assets', 'rejony_in_warsaw_indexed.geojson'), encoding='utf8') as json_file:
    rejony_borders = json.load(json_file)

with open(os.path.join(THIS_FOLDER, 'assets', 'raw_node_pos.json'), encoding='utf8') as file:
    stops_pos = pd.read_json(file).transpose()

with open(os.path.join(THIS_FOLDER, 'assets', 'stops_in_rejon.json'), encoding='utf8') as json_file:
    stops_in_rejon = json.load(json_file)

schools_in_rejon = pd.read_csv(os.path.join(
    THIS_FOLDER, 'assets', 'schools_in_rejon.csv'))

access_mm = pd.read_csv("assets/metrics/access_mm.csv")
access_pdwc = pd.read_csv("assets/metrics/access_pdwc.csv")


def build_map(metric, options, selceted_region):
    if metric == "mm":
        access = access_mm
    else:
        access = access_pdwc


    gray_colorscale = [[0, 'gray'],
                    [1, 'gray']]
    fig = go.Figure()

    if metric != "mm":
        str_access = access.assign(accessibility_index = np.where(access.accessibility_index == -1, "n/a", (access.accessibility_index*100).round(2).astype(str) + "%"))
    else:
        str_access = access.assign(accessibility_index = np.where(access.accessibility_index == -1, "n/a", (access.accessibility_index).round(3).astype(str)))
    access_true = access.assign(accessibility_index = np.where(access.accessibility_index == -1, None, access.accessibility_index))
    access_false = access.assign(accessibility_index = np.where(access.accessibility_index == -1, access.accessibility_index, None))
    customdata = str_access[['index', 'accessibility_index']]
    hover_text = "Dostępność komunikacyjna: " if metric=="mm" else "Procent dostępnych szkół: "
    hovertemplate = 'Rejon %{customdata[0]}<br>' + \
                    hover_text + '<b>%{customdata[1]}</b><br>' + "<extra></extra>"

    if not selceted_region:
        fig.add_choroplethmapbox(colorscale=gray_colorscale, geojson=rejony_borders, customdata=customdata,
                                 hovertemplate=hovertemplate,
                                 locations=access_false["index"],
                                 z=access_false["accessibility_index"],
                                 zmax=0,
                                 zmin=0,
                                 showscale=False,
                                 featureidkey="properties.index",
                                 marker={'opacity': 0.7}, below=True)
        fig.add_choroplethmapbox(colorscale='Balance', geojson=rejony_borders, customdata=customdata,
                                 hovertemplate=hovertemplate,
                                 locations=access_true["index"],
                                 z=access_true["accessibility_index"],
                                 zmax=np.max(access_true["accessibility_index"]),
                                 zmin=0,
                                 featureidkey="properties.index",
                                 showscale=True, marker={'opacity': 0.7}, below=True)
    else:
        fig.add_choroplethmapbox(colorscale=gray_colorscale, geojson=rejony_borders, customdata=customdata,
                                 hovertemplate=hovertemplate,
                                 locations=access_false["index"],
                                 z=access_false["accessibility_index"],
                                 zmax=0,
                                 zmin=0,
                                 marker={'opacity': 0.5},
                                 featureidkey="properties.index",
                                 selected={'marker': {'opacity': 0.7}},
                                 unselected={'marker': {'opacity': 0.2}},
                                 showscale=False,
                                 selectedpoints=selceted_region, below=True)
        fig.add_choroplethmapbox(colorscale='Balance', geojson=rejony_borders, customdata=customdata,
                                 hovertemplate=hovertemplate,
                                 locations=access_true["index"],
                                 z=access_true["accessibility_index"],
                                 zmax=np.max(access_true["accessibility_index"]),
                                 zmin=0,
                                 marker={'opacity': 0.5},
                                 featureidkey="properties.index",
                                 showscale=True,
                                 selected={'marker': {'opacity': 0.7}},
                                 unselected={'marker': {'opacity': 0.2}},
                                 selectedpoints=selceted_region, below=True)
    if "stops" in options:
        if "subway" in options:
            stops = stops_pos.iloc[np.where(~stops_pos.index.astype(
                str).str.zfill(4).str.startswith("0"))]
        else:
            stops = stops_pos
        fig.add_scattermapbox(
            lat=stops[1],
            lon=stops[0],
            showlegend=False,
            hoverinfo='skip'
        )

    if "schools" in options:
        fig.add_scattermapbox(
            lat=schools_in_rejon['lat'],
            lon=schools_in_rejon['lon'],
            showlegend=False,
            hoverinfo='skip',
            marker=go.scattermapbox.Marker(
                color="blue"
            ),
        )
    if "subway" in options:
        subway_pos = stops_pos.iloc[np.where(
            stops_pos.index.astype(str).str.zfill(4).str.startswith("0"))]
        fig.add_scattermapbox(
            lat=subway_pos[1],
            lon=subway_pos[0],
            showlegend=False,
            hoverinfo='skip',
            marker=go.scattermapbox.Marker(
                color="black"
            ),
        )

    # for i, color in zip([black_indexes, white_indexes], ["black", "white"]):
    #     fig.add_scattermapbox(
    #         lat=df.lat[i],
    #         lon=df.lon[i],
    #         mode='text',
    #         text=label_text[i],
    #         textfont={
    #             "color": color,
    #             "family": 'Verdana, sans-serif',
    #             "size": 12,
    #         },
    #         name='',
    #         showlegend=False,
    #         hoverinfo='skip'
    #     )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 35},
        mapbox=dict(
            accesstoken='pk.eyJ1Ijoid2QydGVhbSIsImEiOiJja2E0MjMyNDcwcHliM2VvZ25ycTV4MTBuIn0.7pvFq64tRzS_FgMCGcBljQ',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=52.2297,
                lon=21.0122
            ),
            pitch=0,
            zoom=10
        ),
        clickmode='event+select'
    )

    return fig
