def gender_text2num(gender):
    if gender == 'Male':
        return 1
    elif gender == 'Female':
        return 2
    else:
        return 3

def pronoun_text2num(gender):
    if gender == 'He/Him':
        return 1
    elif gender == 'She/Her':
        return 2
    else:
        return 3

def pronoun_num2text(gender):
    if gender == '1':
        return 'He/Him'
    elif gender == '2':
        return 'She/Her'
    else:
        return 'They/Them'

def boolean_text2num(boolean):
    if boolean:
        return 1
    else:
        return 0