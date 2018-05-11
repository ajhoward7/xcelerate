import plotly.graph_objs as go
import plotly
from datetime import *
import pandas as pd

import utils

# import os
# os.chdir('/Users/alexhoward/Dropbox/xcelerate/code/')


def bar_plot(user):

    planned_training = utils.get_all_planned_training(user)
    logged_training = utils.get_all_logged_training(user)

    try:
        last_logged_day = max(list(logged_training.run_date))
    except BaseException:
        last_logged_day = date.today() - timedelta(days=1)
    planned_training = planned_training[
        planned_training.run_date > last_logged_day]

    planned_training = planned_training[['miles', 'week_start']]
    planned_training.columns = ['miles_planned', 'week_start']

    planned_training = planned_training.groupby(
        ['week_start'], as_index=False).miles_planned.sum()

    logged_training['week_start'] = logged_training.run_date.\
        apply(lambda x: x - timedelta(days=x.weekday()))
    logged_training = logged_training[['week_start', 'miles']]
    logged_training.columns = ['week_start', 'miles_logged']
    logged_training = logged_training.groupby(
        ['week_start'],
        as_index=False).miles_logged.sum()

    df = pd.merge(logged_training,
                  planned_training,
                  on='week_start',
                  how='outer').fillna(0)

    data = []
    custom_colours = ['black', 'blue']

    j = 0
    for type in ['planned', 'logged']:
        data.append(go.Bar(
            x=df['week_start'],
            y=df['miles_{}'.format(type)],
            marker=dict(color=custom_colours[j]),
            name=type))
        j += 1

    layout = dict(
        barmode='stack',
        hovermode='closest',
        title='Miles per week',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='YTD',
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='date'
        )
    )

    fig = go.Figure(data=data, layout=layout)

    path = '../code/main/users/'

    return plotly.offline.plot(fig, filename=path + user + '/plot.html', auto_open=False)
