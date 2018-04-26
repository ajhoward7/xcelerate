import json
import pandas as pd
from datetime import *


def get_preferences(user):
    """
    Given user object, return dictionary of preferences from appropriate file ---- JAKE

    NOTES:
    -This is bad practice because I am hardcoding a filepath, but I think that is fine for this project -JT
    """
    preferences = json.load(open('main/users/' + user + '/preferences.txt'))
    return preferences


def get_run_vector(preferences):
    """
    Obtain appropriate run vector given specific preferences
    """
    runlevel = preferences['runner_type']
    typerace = preferences['race_distance']
    run_vector = pd.read_csv('main/plan_vectors/' + str(runlevel) + '_' + str(typerace) + '.csv')
    return run_vector


def get_recent_logged_training(user, n_weeks=3):

    x_weeks_before = date.today() - timedelta(days=7 * n_weeks)

    logged_training = get_all_logged_training(user)

    recent_logged_training = logged_training[(logged_training.run_date >= x_weeks_before) &
                                               (logged_training.run_date <= date.today())]

    return recent_logged_training


def get_recent_planned_training(user, n_weeks=3):

    planned_training = get_all_planned_training(user)

    x_weeks_before = date.today() - timedelta(days=7 * n_weeks)

    recent_planned_training = planned_training[(planned_training.run_date >= x_weeks_before) &
                                               (planned_training.run_date <= date.today())]

    return recent_planned_training


def get_all_planned_training(user):

    return pd.read_csv('../users/{}/planned_training.csv'.format(user), parse_dates = ['run_date','week_start'])


def get_all_logged_training(user):

    return pd.read_csv('../users/{}/logged_training.csv'.format(user), parse_dates=['run_date'])
