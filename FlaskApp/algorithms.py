def algorithm(input1, input2):
    if input1 == 'Too Hard':
        return int(input2) - 1
    elif input1 == 'Too Easy':
        return int(input2) + 1
    else:
        return int(input2)