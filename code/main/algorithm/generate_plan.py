import constants
import lib
import utils


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


def generate_days_per_week(preferences, weeks_of_plan):
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
    run_vector = utils.get_run_vector(user)

    # Part 2: Calculate weeks of plan
    weeks_of_plan = lib.how_many_weeks_left(user)  # Jake

    # Part 3: Generate number of days per week to run on each week
    days_per_week = generate_days_per_week(preferences, weeks_of_plan)  # Holly

    # Part 4: Generate mileage per week for each week
    mileage_baseline = lib.get_baseline_mileage(preferences)
    mileage_limit = lib.get_limit_mileage(preferences)

    if mileage_limit <= mileage_baseline + 5:
        mileage_limit = mileage_baseline + 5

    miles_per_week = generate_mpw(mileage_baseline, mileage_limit, weeks_of_plan)

    # Part 5: concatenate Part 3 & 4 to create full plan with run vector
    training_plan = construct_plan(days_per_week, miles_per_week, run_vector, weeks_of_plan)
    # Probably just put this bit within the function

    return training_plan
