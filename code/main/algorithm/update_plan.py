import pandas as pd
from datetime import *

import utils
import lib

import generate_plan_backup

def update_miles_per_week(preferences, summary, training_plan):
    """
    JUST THIS TO COMPLETE
    """
    return updated_miles_per_week


def update_days_per_week(preferences, summary, training_plan):
    """
    JUST THIS TO COMPLETE
    """
    return updated_days_per_week


def update_training_plans(user):

    preferences = utils.get_preferences(user)

    recent_logged_training = utils.get_recent_logged_training(user, n_weeks=3)

    recent_planned_training = utils.get_recent_planned_training(user, n_weeks=3)
    training_plan = utils.get_all_planned_training(user)

    summary = lib.generate_week_summary_stats(recent_planned_training, recent_logged_training)

    updated_miles_per_week = update_miles_per_week(preferences, summary, training_plan)
    updated_days_per_week = update_days_per_week(preferences, summary, training_plan)

    run_vector = utils.get_run_vector(preferences)

    return generate_plan_backup.combine_miles_days(updated_miles_per_week, updated_days_per_week,
                                                   preferences, run_vector)


if __name__ == "__main__":

    user = 'alex'  # Adapt this
    training_plan = update_training_plan(user)
    training_plan.to_csv('../users/{}/planned_training.csv'.format(user), index = False)
