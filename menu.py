
def getIntInRange(min, max, promptMessage):
    while True:
        choice = input(promptMessage)
        try:
            choiceInt = int(choice)
            if min <= choiceInt <= max:  # if input is in range return it
                return choiceInt
        except ValueError as e:
            print('Bad input:', e)
        print('Please try again')

def printMenu(options, indentLevel=1):
    i = 0
    for option in options:
        i += 1
        indent = '\t' * indentLevel
        print(indent + str(i) + ' : ' + option)

def getFloatInRange(min, max, promptMessage):
    while True:
        choice = input(promptMessage)
        try:
            choiceFloat = float(choice)
            if min <= choiceFloat <= max:  # if input is in range return it
                return choiceFloat
        except ValueError as e:
            print('Bad input:', e)
        print('Please try again')