import utils


def update_training_plans(user):

    preferences = utils.get_preferences(user)

    logged_training = utils.get_logged_training(user)

    planned_training = utils.get_planned_training(user)

    """
    Idea:
        Take weighted average difference from last 3 weeks between logged and planned and curve back towards mean.

        Adjust factor by "difficulty" preference.
    
    """


    return updated_training_plan
