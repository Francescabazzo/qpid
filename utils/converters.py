def gender_text2num(gender):
    if gender == 'Male':
        return 1
    elif gender == 'Female':
        return 2
    else:
        return 3

def gender_num2text(gender):
    if gender == '1':
        return 'Male'
    elif gender == '2':
        return 'Female'
    else:
        return 'Other'

def boolean_text2num(boolean):
    if boolean:
        return 1
    else:
        return 0