import plotly.graph_objs as go
import plotly
import pandas as pd
from pandas.io.json import json_normalize
import polyline
import json
from datetime import *
import plotly.plotly as py
import utils

plotly.tools.set_credentials_file(username='t2liu', api_key='lTbNwAyxLOCeOxmJCVtX')


def generate_map(user, date):

    mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'
    data = json.load(open('../code/main/users/alex/strava_activities.json'))
    activities_df = json_normalize(data)
    activities_df = activities_df[
        ['average_speed', 'distance', 'moving_time', 'name', 'start_date_local', 'id', 'workout_type', 'type',
         'map.summary_polyline']]
    activities_df['date'] = activities_df.start_date_local.apply(lambda x: x.split('T')[0])

    print(activities_df)
    print('#####')
    print(date)
    print('#####')
    print(activities_df[activities_df.date == date]['map.summary_polyline'])

    map_polyline = activities_df[activities_df.date == date].reset_index()['map.summary_polyline'][0]

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
    print(user)

    # path = '../code/main/users/{}/map.html'.format(user)
    # return plotly.offline.plot(fig, filename=path, auto_open=False)
    return py.plot(fig, filename='testing2', auto_open=False)


def generate_mileage_line(user):
    planned_training = pd.read_csv('../code/main/users/{}/planned_training.csv'.format(user),
                                   parse_dates=['run_date', 'week_start'])
    logged_training = pd.read_csv('../code/main/users/{}/logged_training.csv'.format(user),
                                  parse_dates=['run_date'])

    planned_training = planned_training.groupby(['week_start'], as_index=False).miles.sum()
    logged_training['week_start'] = logged_training.run_date.apply(lambda x: x - timedelta(days=x.weekday()))
    logged_training = logged_training.groupby(['week_start'], as_index=False).miles.sum()

    trace0 = go.Scatter(
        x=logged_training.week_start,
        y=logged_training.miles,
        mode='lines+markers',
        name='Miles per Week Logged',
        hoverinfo='none',
        marker=dict(color='black',
                    size=10)
    )

    trace1 = go.Scatter(
        x=planned_training.week_start,
        y=planned_training.miles,
        mode='lines+markers',
        name='Miles per Week Planned',
        hoverinfo='none',
        marker=dict(color='blue',
                    size=10)
    )

    layout = go.Layout(
        title='Miles per Week',
        yaxis=dict(
            title='Total Miles'
        ),
        showlegend=True
    )

    data = [trace0, trace1]

    fig = go.Figure(data=data, layout=layout)

    # path = '../code/main/users/{}/mpw.html'.format(user)
    # return plotly.offline.plot(fig, filename=path, auto_open=False)
    return py.plot(fig, filename='testing', auto_open=False)
