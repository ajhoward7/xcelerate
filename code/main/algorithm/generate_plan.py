from datetime import * # Used in how_many_weeks_left

import constants
import lib


def generate_training_plan(user):
    """
    Steps:
    1. Read in users preferences
    2. Choose appropriate run vector
    3. Generate training plan
    """
    preferences = lib.get_preferences(user)  # Jake

    run_vector = lib.get_run_vector(user)  # Jake

    training_plan = build_plan(preferences, run_vector)

    return training_plan


def build_plan(preferences, run_vector):
    """
    Steps:
    1. Decide how many days to run on each week up until race day
    2. Decide how many miles to run on each week
    3. Select appropriate proportion of run vector
    4. Return plan, divided by week
    """

    weeks_of_plan = how_many_weeks_left(preferences['race_date'], preferences['start_date'])  # Jake

    days_per_week = days_per_week(preferences, weeks_of_plan)  # Holly

    mileage_baseline = get_baseline_mileage(preferences)
    mileage_limit = get_limit_mileage(preferences)

    if mileage_limit <= mileage_baseline + 5:
        mileage_limit = mileage_baseline + 5

    miles_per_week = generate_mpw(mileage_baseline, mileage_limit, weeks_of_plan)

    training_plan = construct_plan(days_per_week, miles_per_week, run_vector, weeks_of_plan)

    return training_plan


def generate_mpw(mileage_baseline, mileage_limit, weeks_of_plan):
    """
    Given the preferences dictionary and number of weeks in the plan, this function returns a list of weekly mileages
    for the individual.
    """

    miles_per_week = [0 for _ in range(weeks_of_plan)]

    current_mileage = mileage_baseline

    for i in range(weeks_of_plan):
        miles_per_week[i] = current_mileage
        if i % constants.increase_period == 0 and current_mileage < mileage_limit:
            current_mileage *= constants.increase_factor

    for i in range(weeks_of_plan):
        if i+1 % constants.easy_week_frequency == 0:
            miles_per_week[i] *= constants.easy_week_cycle_adjustment

    return miles_per_week


def get_baseline_mileage(preferences):
    """
    1. Novice, no prior training - pre-defined constants
    2. Novice, prior training - prior training levels
    3. Intermediate - prior training levels
    """

    if 'prior_miles_per_week' in preferences.keys():
        return preferences['prior_miles_per_week']
    else:
        if preferences['race_distance'] == 0:
            return constants.novice_5k_baseline
        if preferences['race_distance'] == 1:
            return constants.novice_10k_baseline
        if preferences['race_distance'] == 2:
            return constants.novice_half_baseline
        if preferences['race_distance'] == 3:
            return constants.novice_full_baseline


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


def how_many_weeks_left(user):
    """
    Calculate the number of weeks until the race
    """
    preferences = get_preferences(user)
    enddate = datetime.strptime(preferences['enddate'], '%Y-%m-%d')
    today = datetime.today()
    interval = enddate - today
    total_days_left = interval.days
    weeks_left = total_days_left/7
    return weeks_left


def days_per_week(preferences, weeks_of_plan):
    """
    INPUTS
    max_days: number of days per week the user wants to run
    level: intermediate or novice
    increase: boolean to indicate whether the user (intermediate only) wants to increase training. Will be True
                if level = novice
    weeks_of_plan: number of weeks left until race day
    previous_days: number of training days per week from previous training. Will be -1 if no previous data

    OUTPUTS
    plan: vector of number of days per week for remaining training

    """

    max_days = preferences['max_days_per_week']
    level = preferences['runner_type']
    try:
        increase = preferences['training_level_increase']
    except:
        pass
    try:
        previous_days = preferences['prior_days_per_week']
    except:
        previous_days = 0

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
        plan = [initial] * (weeks_of_plan)

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

        last = [max_days] * (weeks_of_plan - len(plan))
        plan = plan + last

    return plan


def construct_plan(days_per_week, miles_per_week, run_vector, weeks_of_plan):

    training_plan = True

    return training_plan
