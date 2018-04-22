import json
import pandas as pd


def get_preferences(user):
    """
    Given user object, return dictionary of preferences from appropriate file ---- JAKE

    NOTES:
    -This is bad practice because I am hardcoding a filepath, but I think that is fine for this project -JT
    """
    preferences = json.load(open('../users/' + user + '/preferences.txt'))
    return preferences


def get_run_vector(preferences):
    """
    Obtain appropriate run vector given specific preferences
    """
    runlevel = preferences['runner_type']
    typerace = preferences['race_distance']
    run_vector = pd.read_csv('../plan_vectors/' + str(runlevel) + '_' + str(typerace) + '.csv')
    return run_vector


def get_logged_training(user, weeks = 3):
    # Blah
    return training_df


def get_recent_planned_training(user, weeks = 3):
    planned_training = get_all_planned_training(user)
    #Blah
    return recent_planned_training_df


def get_all_planned_training(user):
    # Blah
    return planned_training_df
