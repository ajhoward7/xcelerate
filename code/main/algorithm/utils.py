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


def get_run_vector(user):
    """
    Obtain appropriate run vector given specific preferences ----- JAKE

    NOTES:
    -I changed the input of this function to be a user instead of distances.  The output is a dataframe -JT
    -We should standardize the runner types and run levels so that the labels in the preferences match the names of the vector files -JT
    """
    preferences = get_preferences(user)
    runlevel = preferences['runlevel']
    typerace = preferences['typerace']
    run_vector = pd.read_csv('../plan_vectors/' + runlevel + '_' + typerace + '.csv')
    return run_vector
