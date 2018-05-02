# Script to process Garmin files

import pandas as pd

filename = 'activities.csv'
user = 'alex'

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

	training['run_date'] = pd.to_datetime(training['Date']).apply(lambda x : x.date())
	training['miles'] = training['Distance']

	training[['run_date','miles','Time','Title']].to_csv('../users/{}/logged_training.csv'.format(user), index=False)
	
	return True

write_planned_training(training)
