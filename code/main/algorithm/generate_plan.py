import constants
import lib
import utils

import pandas as pd
from datetime import *
import numpy as np

import sys


def generate_mpw(mileage_baseline, mileage_limit, weeks):
    """
    Given the preferences dictionary and number of weeks in the plan, this function returns a list of weekly mileages
    for the individual.
    """
    miles_per_week = [0 for _ in range(weeks)]

    current_mileage = mileage_baseline

    for i in range(weeks):
        miles_per_week[i] = current_mileage
        if i % constants.increase_period == 0 and current_mileage < mileage_limit:
            current_mileage *= (1+constants.increase_factor)

    for i in range(weeks):
        if i+1 % constants.easy_week_frequency == 0:
            miles_per_week[i] *= constants.easy_week_cycle_adjustment

    return miles_per_week


def generate_days_per_week(preferences, weeks):
    """
    Given the preferences dictionary and the number of weeks in the plan, this function returns
    a list of the number of training days per week for each week of the training plan.

    INPUTS
    max_days: number of days per week the user wants to run
    level: intermediate or novice
    increase: boolean to indicate whether the user (intermediate only) wants to increase training. Will be True
                if level = novice
    weeks: number of weeks left until race day
    previous_days: number of training days per week from previous training. Will be -1 if no previous data

    OUTPUTS
    plan: vector of number of days per week for remaining training

    """

    max_days = preferences['max_days_per_week']
    level = preferences['runner_type']
    try:
        increase = preferences['training_level_increase']
    except:
        increase = 'NaN'
    try:
        previous_days = preferences['prior_days_per_week']
    except:
        previous_days = 0

    ### ADDED #####################
    if max_days == 99:
        max_days = previous_days
    ###############################

    if level == 0:
        initial = int(round(max_days * .666))

    elif level == 1:
        if previous_days > 0:
            initial = previous_days
        else:
            initial = int(round(max_days * .666))

    if initial > max_days:  # Handles edge case of previous days per week > max_days
        initial = max_days

    if increase == False:
        plan = [initial] * (weeks)

    else:
        plan = []

        plan.append(initial)
        plan.append(initial)

        days = initial

        i = 0

        while plan[i] < max_days:
            days = plan[i] + 1
            plan.append(days)
            plan.append(days)
            i += 2

        last = [max_days] * int(weeks - len(plan))
        plan = plan + last

    return plan


def combine_miles_days(miles_per_week, days_per_week, preferences, run_vector):

    number_of_runs = sum(days_per_week)

    run_miles = run_vector['run_miles'][:number_of_runs][::-1]
    run_workout = run_vector['workout'][:number_of_runs][::-1]
    run_long_run = run_vector['long_run'][:number_of_runs][::-1]

    week_of_run = []
    adj_run_vector = []
    run_day = []
    run_date = []

    k = 0

    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # Initialise start_of_week

    available_days = preferences['available_days']

    for i in range(len(days_per_week)):
        days_this_week = days_per_week[i]
        miles_this_week = miles_per_week[i]
        runs_this_week = []
        try:
            which_days_this_week = np.sort(np.random.choice(available_days, days_this_week, False))

        except:
            raise(ValueError("Individual can't run on this many days"))

        for j in range(days_this_week):
            week_of_run.append(i)
            runs_this_week.append(run_miles[k])
            run_day.append(which_days_this_week[j])
            if which_days_this_week[j] == 0:
                run_date.append(start_of_week)
            else:
                run_date.append(start_of_week + timedelta(days=int(which_days_this_week[j])))

            k += 1

        factor = float(miles_this_week) / sum(runs_this_week)

        adj_run_vector += [int(round(run * factor)) for run in runs_this_week]

        start_of_week += timedelta(days=7)

    training_plan = pd.DataFrame([])

    training_plan['week_of_run'] = week_of_run
    training_plan['miles'] = adj_run_vector
    training_plan['run_day'] = run_day
    training_plan['run_date'] = [this_date.date() for this_date in run_date]
    training_plan['workout'] = run_workout[:len(run_date)][::-1]
    training_plan['long_run'] = run_long_run[:len(run_date)][::-1]
    training_plan['week_start'] = training_plan.run_date.apply(lambda x : (x - timedelta(days=x.weekday())))

    race_day = datetime.strptime(preferences['race_date'], '%Y-%m-%d').date()

    #training_plan = training_plan[training_plan['run_date'] > datetime.today().date()]
    training_plan = training_plan[training_plan['run_date'] <= race_day]

    training_plan.miles = training_plan['miles'].astype('float')

    training_plan = training_plan[:-1]

    training_plan = training_plan.append({'miles': lib.get_race_distance(preferences),
                                          'week_of_run': week_of_run[-1],
                                          'run_date': race_day,
                                          'run_day': race_day.weekday(),
                                          'week_start': race_day - timedelta(days = race_day.weekday()),
                                          'workout':0,'long_run':0},
                                         ignore_index = True)

    return training_plan


def build_plan(user):
    """
    Steps:
    1. Decide how many days to run on each week up until race day
    2. Decide how many miles to run on each week
    3. Select appropriate proportion of run vector
    4. Return plan, divided by week
    """

    # Part 1: Read in preferences and appropriate run vector
    preferences = utils.get_preferences(user)
    run_vector = utils.get_run_vector(preferences)

    # Part 2: Calculate weeks of plan
    weeks = lib.weeks_of_plan(preferences)  # Jake

    # Part 3: Generate number of days per week to run on each week
    days_per_week = generate_days_per_week(preferences, weeks)  # Holly
    print(days_per_week)

    # Part 4: Generate mileage per week for each week
    mileage_baseline = lib.get_baseline_mileage(preferences)
    mileage_limit = lib.get_limit_mileage(preferences)

    if mileage_limit <= mileage_baseline + 5:
        mileage_limit = mileage_baseline + 5

    miles_per_week = generate_mpw(mileage_baseline, mileage_limit, weeks)
    print(miles_per_week)

    # Part 5: concatenate Part 3 & 4 to create full plan with run vector

    return combine_miles_days(miles_per_week, days_per_week, preferences, run_vector)


def generate_plan(user):
    training_plan = build_plan(user)
    training_plan.to_csv('main/users/{}/planned_training.csv'.format(user), index = False)

    return training_plan


# if __name__ == "__main__":

#     user = 'alex'  # Adapt this
#     training_plan = build_plan(user)
#     training_plan.to_csv('../users/{}/planned_training.csv'.format(user), index = False)
