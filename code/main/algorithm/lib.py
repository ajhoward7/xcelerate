import pandas as pd
from datetime import *

import constants


def get_baseline_mileage(preferences, first_week_days):
    """
    1. Novice, no prior training - pre-defined constants
    2. Novice, prior training - prior training levels
    3. Intermediate - prior training levels
    """

    if 'prior_miles_per_week' in preferences.keys():
        return preferences['prior_miles_per_week']
    else:
        if preferences['race_distance'] == 0:
            return constants.novice_5k_baseline_mpd * first_week_days
        if preferences['race_distance'] == 1:
            return constants.novice_10k_baseline_mpd * first_week_days
        if preferences['race_distance'] == 2:
            return constants.novice_half_baseline_mpd * first_week_days
        if preferences['race_distance'] == 3:
            return constants.novice_full_baseline_mpd * first_week_days


def get_limit_mileage(preferences):
    """
    1. Novice - pre-defined constants
    2. Intermediate, keep same levels - set to previous level
    3. Intermediate, increase level - pre-defined constants
    """

    if preferences['runner_type'] == 0:
        if preferences['race_distance'] == 0:
            return constants.novice_5k_limit
        if preferences['race_distance'] == 1:
            return constants.novice_10k_limit
        if preferences['race_distance'] == 2:
            return constants.novice_half_limit
        if preferences['race_distance'] == 3:
            return constants.novice_full_limit

    else:
        if preferences['training_level_increase'] == 0:
            return preferences['prior_miles_per_week']

        else:
            if preferences['race_distance'] == 0:
                return constants.inter_5k_limit
            if preferences['race_distance'] == 1:
                return constants.inter_10k_limit
            if preferences['race_distance'] == 2:
                return constants.inter_half_limit
            if preferences['race_distance'] == 3:
                return constants.inter_full_limit


def weeks_of_plan(preferences):
    """
    Calculate the number of weeks until the race
    """
    today = date.today()
    start_of_first_week = today - timedelta(days=today.weekday())

    end_date = datetime.strptime(preferences['race_date'], '%Y-%m-%d')
    end_date = end_date.date()
    start_of_last_week = end_date - timedelta(days=end_date.weekday())

    interval = start_of_last_week - start_of_first_week

    total_days_left = interval.days + 8

    weeks = total_days_left/7

    return int(weeks)


def get_race_distance(preferences):
    """
    Return number of miles of race from preferences
    """
    race_distance = preferences['race_distance']

    if race_distance == 0:
        return 3.1
    if race_distance == 1:
        return 6.2
    if race_distance == 2:
        return 13.1
    if race_distance == 3:
        return 26.2


def generate_week_summary_stats(planned, logged):
    """
    For each number of weeks before present day, generate summary statistics for planned and logged training and merge
    into a single data frame.
    """
    # Bucket weeks based on integer number of weeks before today:
    planned['weeks_before_now'] = planned.run_date.apply(lambda x : int((date.today() - x.date()).days/7))
    logged['weeks_before_now'] = logged.run_date.apply(lambda x: int((date.today() - x.date()).days / 7))

    # Group data frames based on 'weeks_before_now':
    planned_grouped = planned.groupby(['weeks_before_now'],as_index = False).agg({'miles':'sum','run_date':'count'})
    logged_grouped = logged.groupby(['weeks_before_now'],as_index = False).agg({'miles':'sum','run_date':'count'})

    # Join appropriately to return:
    output = pd.merge(planned_grouped, logged_grouped, how='left',
                      on='weeks_before_now', suffixes=['_planned','_logged'])

    return output


def retrieve_summary_stats(planned):
    """
    Read in the planned_training dataframe and retrieve summary statistics (miles per week, days per week) to work from
    when updated training plans.
    """
    future_training = planned[planned.run_date >= date.today() - timedelta(days=date.today().weekday())]

    future_by_week = future_training.groupby(['week_start'], as_index = False).agg({'miles':'sum','run_date':'count'}).\
                        sort_values('week_start',ascending = True)

    return future_by_week
