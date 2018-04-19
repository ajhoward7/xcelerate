from datetime import *


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


