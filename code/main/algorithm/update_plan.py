import pandas as pd
from datetime import *

import utils
import lib
import constants

import generate_plan


def update_miles_per_week(preferences, summary, miles_per_week):
    """
    Starting point: just use previous week training and halve distance to expect
    """
    updated_miles_per_week = miles_per_week.copy()

    previous_logged = summary[summary.weeks_before_now == 0].miles_logged
    previous_planned = summary[summary.weeks_before_now == 0].miles_planned


    for i in range(len(miles_per_week)):
        diff = float((previous_logged - previous_planned) / previous_planned)
        updated_miles_per_week[i] *= (1 + diff/2)

        previous_logged = updated_miles_per_week[i]
        previous_planned = miles_per_week[i]

    if preferences['difficulty'] == 2:
        updated_miles_per_week = [miles * (1+constants.increase_factor) for miles in updated_miles_per_week]

    if preferences['difficulty'] == 0:
        updated_miles_per_week = [miles * (1-constants.increase_factor) for miles in updated_miles_per_week]

    return updated_miles_per_week


def update_days_per_week(summary, days_per_week):
    """
    JUST THIS TO COMPLETE
    """
    updated_days_per_week = days_per_week.copy()

    previous_logged = summary[summary.weeks_before_now == 0].run_date_logged
    previous_planned = summary[summary.weeks_before_now == 0].run_date_planned

    for i in range(len(days_per_week)):
        diff = int((previous_logged - previous_planned) / previous_planned)
        updated_days_per_week[i] = int((1 + diff / 2) * updated_days_per_week[i])

        previous_logged = updated_days_per_week[i]
        previous_planned = days_per_week[i]

    return updated_days_per_week


def update_training_plan(user):

    preferences = utils.get_preferences(user)

    recent_logged_training = utils.get_recent_logged_training(user, n_weeks=3)

    recent_planned_training = utils.get_recent_planned_training(user, n_weeks=3)
    training_plan = utils.get_all_planned_training(user)

    summary = lib.generate_week_summary_stats(recent_planned_training, recent_logged_training)

    training_plan_summary = lib.retrieve_summary_stats(training_plan)

    updated_miles_per_week = update_miles_per_week(preferences, summary, training_plan_summary.miles.tolist())
    updated_days_per_week = update_days_per_week(summary, training_plan_summary.run_date.tolist())

    run_vector = utils.get_run_vector(preferences)

    return generate_plan.combine_miles_days(updated_miles_per_week, updated_days_per_week,
                                                   preferences, run_vector)


if __name__ == "__main__":

    user = 'alex'  # Adapt this
    training_plan = update_training_plan(user)
    training_plan.to_csv('../users/{}/planned_training.csv'.format(user), index=False)
