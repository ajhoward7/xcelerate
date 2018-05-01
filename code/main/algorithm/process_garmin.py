# Script to process Garmin files

import pandas as pd

filename = 'activities.csv'

training = pd.read_csv(filename)

def update_preferences(training):
	"""
	Holly: update preferences with prior_miles_per_week and prior_days_per_week based on Garmin file
	"""

	return True


def write_planned_training(training):
	"""
	Alex: write planned training with file
	"""
	
	return True
