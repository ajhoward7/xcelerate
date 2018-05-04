# Script to process Garmin files

import pandas as pd
import numpy as np
import json
import os

# filename = '../users/' + user + '/activities.csv'
# user = 'alex'

# training = pd.read_csv(filename)


def update_preferences(training, user):
    """
    Holly: update preferences with prior_miles_per_week
    and prior_days_per_week based on Garmin file
    """
    training = pd.read_csv(training)

    training['Date'] = pd.to_datetime(training['Date'])
    training['Week'] = training['Date'].dt.week
    training['DOW'] = training['Date'].dt.day

    weeks = training.Week.unique()
    last_3_weeks = weeks[0:3]
    last_3_weeks_df = training.loc[training['Week'].isin(last_3_weeks)]

    days_per_week = last_3_weeks_df.groupby(['Week'],
                                            as_index=False)['DOW'].nunique()
    prior_days_per_week = int(round((np.mean(days_per_week))))

    miles_per_week = last_3_weeks_df.groupby(['Week'],
                                             as_index=False)['Distance'].sum()
    prior_miles_per_week = np.mean(miles_per_week['Distance'])

    filename = 'main/users/' + user + '/preferences.txt'
    with open(filename, 'r') as f:
        data = json.load(f)

    data['prior_days_per_week'] = prior_days_per_week
    data['prior_miles_per_week'] = prior_miles_per_week

    os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    return True


def write_planned_training(training, user):
    """
    Alex: write planned training with file
    """
    training = pd.read_csv(training)

    training['run_date'] = pd.to_datetime(training['Date']).\
        apply(lambda x: x.date())
    training['miles'] = training['Distance']

    training[['run_date', 'miles']].\
        to_csv('main/users/{}/logged_training.csv'.format(user), index=False)
    return True


def process_garmin(training, user):
    write_planned_training(training, user)
    update_preferences(training, user)

# if __name__=="__main__":
#     write_planned_training(training)
#     update_preferences(training)
