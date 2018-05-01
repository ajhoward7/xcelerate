import utils
import lib
import constants

import generate_plan


"""
This code is used to update a training plan that has been generated for a particular user.

Training plans can be updated by calling: `update_training_plan(user)`

Method:
1. Update MpW
2. Update Days per Week
3. Combine identically as when producing initial training plan

This script in particular uses helper functions that generate summary statistics from lib.py (e.g.
`lib.retrieve_summary_statistics()`.

"""


def update_miles_per_week(preferences, summary, miles_per_week):
    """
    Update miles per week for new training plan - calculate difference for previous week and halve this difference
    iteratively
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
    Update days per week from initial training plan - compute difference for previous week and halve this iteratively
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
    """
    Method:
    1. Update MpW
    2. Update Days per Week
    3. Combine identically as when producing initial training plan

    Output re-writes 'planned_training.csv' file.
    """

    preferences = utils.get_preferences(user)

    recent_logged_training = utils.get_recent_logged_training(user, n_weeks=3)
    recent_planned_training = utils.get_recent_planned_training(user, n_weeks=3)

    training_plan = utils.get_all_planned_training(user)

    # Generate summary statistics from planned training and logged training:
    summary = lib.generate_week_summary_stats(recent_planned_training, recent_logged_training)
    training_plan_summary = lib.retrieve_summary_stats(training_plan)

    # Update MpW and days per week:
    updated_miles_per_week = update_miles_per_week(preferences, summary, training_plan_summary.miles.tolist())
    updated_days_per_week = update_days_per_week(summary, training_plan_summary.run_date.tolist())

    run_vector = utils.get_run_vector(preferences)

    # Combine these with function taken from `generate_plan` python script:
    updated_training_plan = generate_plan.combine_miles_days(updated_miles_per_week, updated_days_per_week,
                                                                preferences, run_vector)

    updated_training_plan.to_csv('main/users/{}/planned_training.csv'.format(user), index=False)

    return updated_training_plan


if __name__ == "__main__":

    user = 'alex'  # Adapt this
    training_plan = update_training_plan(user)
    training_plan.to_csv('../users/{}/planned_training.csv'.format(user), index=False)
