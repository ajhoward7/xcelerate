import constants


def generate_training_plan(user):
    """
    Steps:
    1. Read in users preferences
    2. Choose appropriate run vector
    3. Generate training plan
    """
    preferences = get_preferences(user)  # Jake

    run_vector = get_run_vector(preferences['distance'], preferences['level'])  # Jake

    training_plan = build_plan(preferences, run_vector)

    return training_plan


def get_preferences(user):
    """
    Given user object, return dictionary of preferences from appropriate file ---- JAKE
    """
    return preferences


def get_run_vector(distance, level):
    """
    Obtain appropriate run vector given specific preferences ----- JAKE
    """

    return run_vector

def build_plan(preferences, run_vector):
    """
    Steps:
    1. Decide how many days to run on each week up until race day
    2. Decide how many miles to run on each week
    3. Select appropriate proportion of run vector
    4. Return plan, divided by week
    """

    weeks_of_plan = how_many_weeks_left(preferences['race_date'], preferences['start_date'])  # Jake

    days_per_week = generate_run_days(preferences, weeks_of_plan)  # Holly

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

