##########################################
# Barrington Venables                    #
# 101189284                              #
# comp2152 assignment - Expense manager  #
##########################################

from year import *
from menu import *
from database import *
import datetime

def main():
    database = Database('expenseRecords.db')
    currentYear = datetime.datetime.now().year
    year = Year(currentYear, database)

    while True:
        print('### Expense Manager for year: ' + str(currentYear) + ' ###')
        printMenu(['Enter an month\'s expenses', 'View expense report', 'Change current year', 'Exit'])
        choice = getIntInRange(1, 4, '\tEnter an integer between 1 and 4: ')

        if choice == 1:
            print(' ## Add Month ##')

            mth = getIntInRange(1, 12, '\tEnter the month number (1-12): ')
            monthString = datetime.datetime(currentYear, mth, 1).strftime("%B")
            rent = getFloatInRange(0, 9999999, '\tEnter rent expense for ' + monthString + ': ')
            grocer = getFloatInRange(0, 9999999, '\tEnter grocery expense for ' + monthString + ': ')
            util = getFloatInRange(0, 9999999, '\tEnter utilities expense for ' + monthString + ': ')
            trans = getFloatInRange(0, 9999999, '\tEnter transit expense for ' + monthString + ': ')
            shop = getFloatInRange(0, 9999999, '\tEnter shopping expense for ' + monthString + ': ')
            ent = getFloatInRange(0, 9999999, '\tEnter entertainment expense for ' + monthString + ': ')

            success = year.addMonth(mth, rent, grocer, util, trans, shop, ent)
            if success:
                print('\t' + monthString + ' expenses added successfully')
            else:
                print('\tCould not add month. Check that there is no current entry for '
                      + monthString + ' in year ' + str(currentYear))

        if choice == 2:
            print(' ## View Expense Reports ##')
            while True:
                monthChoice = getIntInRange(1, 13, '\tEnter a month to view (1-12 -- 13 to exit): ')
                if monthChoice == 13:
                    break
                print(year.getMonthReport(monthChoice))

        if choice == 3:
            print(' ## Change current year ##')
            maxYr = datetime.datetime.now().year
            currentYear = getIntInRange(2000, maxYr, '\tEnter a year between 2000 and ' + str(maxYr) + ': ')
            year = Year(currentYear, database)
        if choice == 4:
            break


if __name__ == '__main__':
    main()