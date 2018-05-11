import plotly.graph_objs as go
import plotly
import pandas as pd
from pandas.io.json import json_normalize
import polyline
import json


def generate_map(user, date):

    mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'
    data = json.load(open('../users/{}/strava_activities.json').format(user))
    activities_df = json_normalize(data)
    activities_df = activities_df[
        ['average_speed', 'distance', 'moving_time', 'name', 'start_date_local', 'id', 'workout_type', 'type',
         'map.summary_polyline']]
    activities_df['date'] = activities_df.start_date_local.apply(lambda x: x.split('T')[0])
    map_polyline = activities_df[activities_df.date == date]['map.summary_polyline'][0]

    gps = polyline.decode(map_polyline)
    df = pd.DataFrame(gps, columns=['lat', 'long'])

    data = go.Data([
        go.Scattermapbox(
            lat=df.lat,
            lon=df.long,
            mode='lines',
            hoverinfo='text',
            marker=go.Marker(
                size=17,
                color='rgb(255, 0, 0)',
                opacity=0.7
            )
        )])

    layout = go.Layout(
        autosize=False,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=df.lat[int(len(df) / 4)],
                lon=df.long[int(len(df) / 4)]
            ),
            pitch=0,
            zoom=10.5,
            style='light'
        ),
    )

    fig = go.Figure(data=data, layout=layout)

    path = '../code/main/users/{}/{}.html'.format(user, date)

    return plotly.offline.plot(fig, filename=path, auto_open=False)


def generate_mileage_line(user):

    return True
