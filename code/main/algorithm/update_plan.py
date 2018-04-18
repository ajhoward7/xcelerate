import constants


def update_training_plans(user):

    preferences = get_preferences(user)

    logged_training = get_logged_training(user)

    planned_training = get_planned_training(user)

    updated_training_plan = construct_plan(logged_training, planned_training, preferences)

    return updated_training_plan


def get_preferences(user):
    """
    Given user object, return dictionary of preferences from appropriate file ---- JAKE -- identical to generate_plan
    """
    return preferences


def get_logged_training(user):
    """
    Return logged training file for user
    """

    return logged_training


def get_planned_training(user):
    """
    Return planned training file for user
    """

    return planned_training


def construct_updated_plan(logged_training, planned_training, preferences):
    """
    Idea:
        Take weighted average difference from last 3 weeks between logged and planned and curve back towards mean.

        Adjust factor by "difficulty" preference.
    """

    return updated_training_plan