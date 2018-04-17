


def generate_training_plan(user):
    """
    Steps:
    1. Read in users preferences
    2. Choose appropriate run vector
    3. Generate training plan
    """
    preferences = get_preferences(user)  # Jake

    run_vector = get_run_vector(preferences['distance'], preferences['level'])

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

    miles_per_week = generate_mpw(preferences, weeks_of_plan)

    training_plan = construct_plan(days_per_week, miles_per_week)

    return training_plan