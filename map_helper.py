#%%
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

schools_with_progi = pd.read_csv(os.path.join(
    THIS_FOLDER, 'assets', 'schools_with_progi.csv'))

access_metrics = {}

for t in os.listdir(os.path.join(THIS_FOLDER, 'assets/metrics')):
    access_metrics[t[:-4]] = pd.read_csv(os.path.join(THIS_FOLDER, 'assets/metrics', t)) 
#%%
def build_map(metric, options, schools_options, selceted_region):

    access = access_metrics[metric]

    gray_colorscale = [[0, 'gray'],
                    [1, 'gray']]
    fig = go.Figure()

    if "percentage" in metric:
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
                                 marker={'opacity': 0.7}, below=False)
        fig.add_choroplethmapbox(colorscale='Balance', geojson=rejony_borders, customdata=customdata,
                                 hovertemplate=hovertemplate,
                                 locations=access_true["index"],
                                 z=access_true["accessibility_index"],
                                 zmax=np.max(access_true["accessibility_index"]),
                                 zmin=0,
                                 featureidkey="properties.index",
                                 showscale=True, marker={'opacity': 0.7}, below=False)
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
                                 selectedpoints=selceted_region, below=False)
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
                                 selectedpoints=selceted_region, below=False)


    if "schools" in options:
        if 'all' in schools_options:
            selected_schools = schools_in_rejon
            fig.add_scattermapbox(
                lat=selected_schools['lat'],
                lon=selected_schools['lon'],
                mode='text',
                text=".",
                textfont={
                    "color": "blue",
                    "family": 'Verdana, sans-serif',
                    "size": 12,
                },
                name='',
                showlegend=False,
                hoverinfo='skip',
                below=True
            )
        else:
            if 'school_lic' in schools_options:
                selected_schools = schools_in_rejon.loc[np.isin(schools_in_rejon["Unnamed: 0"], np.array(schools_with_progi.loc[schools_with_progi.Typ == "Liceum ogólnokształcące"]["Unnamed: 0"]))]
                fig.add_scattermapbox(
                lat=selected_schools['lat'],
                lon=selected_schools['lon'],
                showlegend=False,
                hoverinfo='skip',
                marker=go.scattermapbox.Marker(
                    color="blue"
                    )
                )
            if 'school_podst' in schools_options:
                selected_schools = schools_in_rejon.loc[np.isin(schools_in_rejon["Unnamed: 0"], np.array(schools_with_progi.loc[schools_with_progi.Typ == "Szkoła podstawowa"]["Unnamed: 0"]))]
                fig.add_scattermapbox(
                lat=selected_schools['lat'],
                lon=selected_schools['lon'],
                showlegend=False,
                hoverinfo='skip',
                marker=go.scattermapbox.Marker(
                    color="blue"
                    )
                )
            if 'school_tech' in schools_options:
                selected_schools = schools_in_rejon.loc[np.isin(schools_in_rejon["Unnamed: 0"], np.array(schools_with_progi.loc[schools_with_progi.Typ == "Technikum"]["Unnamed: 0"]))]
                fig.add_scattermapbox(
                lat=selected_schools['lat'],
                lon=selected_schools['lon'],
                showlegend=False,
                hoverinfo='skip',
                marker=go.scattermapbox.Marker(
                    color="blue"
                    )
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
