"""
input1 : the level of difficulty of the previous week
input2 : the days the user trained the previous week

This function returns the days the user will train
the following week
"""


def algorithm(input1, input2):
    if input1 == 'Too Hard':
        return int(input2) - 1
    elif input1 == 'Too Easy':
        return int(input2) + 1
    else:
        return int(input2)
