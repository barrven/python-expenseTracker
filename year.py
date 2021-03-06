##########################################
# Barrington Venables                    #
# 101189284                              #
# comp2152 assignment - Expense manager  #
##########################################

class Year:
    def __init__(self, yearNum, database):
        self.yearNum = yearNum
        self.database = database
        self.months = database.getMonths(self.yearNum)  # list of month objects

    def getCatAvg(self, category):
        count = 0
        sum = 0
        for month in self.months:
            count += 1
            sum += month.getCategory(category)
        return sum / count

    def addMonth(self, number, rent, groceries, utilities, transit, shopping, entertainment):
        success = self.database.addMonthToDb(  # addMonthToDb returns a boolean
            self.yearNum,
            number,
            rent,
            groceries,
            utilities,
            transit,
            shopping,
            entertainment
        )

        if success:
            self.months = self.database.getMonths(self.yearNum)
            return True

        return False

    def addMonth_flex(self, month_num, categories_list):
        success = self.database.addMonthToDb_flex(self.yearNum, month_num, categories_list)
        
        if success:
            self.months = self.database.getMonths(self.yearNum)
            return True

        return False

    def getMonthByNumber(self, monthNum):
        for month in self.months:
            if month.number == monthNum:
                return month
        return None

    def getMonthReport(self, monthNum):
        m = self.getMonthByNumber(monthNum)
        if m is None:
            return 'No month data found'

        # setup the items needed to compile the report
        s = ''
        catNames = ['rent', 'groceries', 'utilities', 'transit', 'shopping', 'entertainment']
        catTitles = ['Rent: ', 'Groceries: ', 'Utilities: ', 'Transit: ', 'Shopping: ', 'Entertainment: ']

        # report header
        s += '\n# ' + m.getCategory('monthName') + ' Expense Report #\n'
        s += pad('|Category ', 16) + pad('|Amount ', 15) + pad('|Year Avg ', 15) + pad('|% of total ', 5) + '\n'

        # get the data for each category: |title|amt|yrAvg|percentTtl|
        for i in range(len(catNames)):
            current = catNames[i]
            s += pad(catTitles[i], 16, '.')  # number arg is column width
            s += pad('$' + customFormat(m.getCategory(current)), 15, '.')  # expense amount
            s += pad('$' + customFormat(self.getCatAvg(current)), 15, '.')  # average
            s += pad(customFormat(m.getCategoryPercent(current)), 5)
            s += '\n'

        total = m.getCategory('totalExpenses')
        avgTotalForYear = self.getCatAvg('totalExpenses')
        s += 'Total Expenses: $' + customFormat(total) + '\n'
        if total < avgTotalForYear:
            s += 'This month is below average for the year ($' + customFormat(avgTotalForYear) + ')'
        elif total > avgTotalForYear:
            s += 'This month is above average for the year ($' + customFormat(avgTotalForYear) + ')'
        else:
            s += 'This month is average for the year ($' + customFormat(avgTotalForYear) + ')'

        return s

    def getMonthData(self, monthNum):
        m = self.getMonthByNumber(monthNum)
        if m is None:
            return [[]]

        catNames = ['rent', 'groceries', 'utilities', 'transit', 'shopping', 'entertainment']
        catTitles = ['Rent: ', 'Groceries: ', 'Utilities: ', 'Transit: ', 'Shopping: ', 'Entertainment: ']
        data = []
        for i in range(len(catNames)):
            current = catNames[i]
            data_row = [
                catTitles[i],  # number arg is column width
                '$' + customFormat(m.getCategory(current)),  # expense amount
                '$' + customFormat(self.getCatAvg(current)),  # average
                customFormat(m.getCategoryPercent(current))
            ]
            data.append(data_row)

        return data

            
    def getEmptyMonths(self):
        month_nums = []
        for month in self.months:
            month_nums.append(month.number)

        empty_months = []
        for i in range(1, 13):
            if i in month_nums:
                continue
            else:
                empty_months.append(i)

        return tuple(empty_months)

    # returns a list of strings or list of integers
    # based on types in the list passed to it.
    def switchMonthStringsAndNums(self, stringOrNums):
        strings = {
            'January' : 1,
            'February' : 2,
            'March' : 3,
            'April' : 4,
            'May' : 5,
            'June': 6,
            'July' : 7,
            'August' : 8,
            'September' : 9,
            'October' : 10,
            'November' : 11,
            'December' : 12 
        }
        nums = {
            '1' : 'January',
            '2' : 'February',
            '3' : 'March',
            '4' : 'April',
            '5' : 'May',
            '6' : 'June',
            '7' : 'July',
            '8' : 'August',
            '9' : 'September',
            '10' : 'October',
            '11' : 'November',
            '12' : 'December'
        }
        
        output = []
        # check if the list has strings or nums
        # build list of corresponding strings or nums
        for item in stringOrNums:
            if type(item) is int:
                output.append(nums[str(item)])
            else:
                output.append(strings[item])
        
        return output

    # returns an integer
    def switchMonthStringToInt(self, monthString):
        strings = {
            'January' : 1,
            'February' : 2,
            'March' : 3,
            'April' : 4,
            'May' : 5,
            'June': 6,
            'July' : 7,
            'August' : 8,
            'September' : 9,
            'October' : 10,
            'November' : 11,
            'December' : 12 
        }

        return strings[monthString]

    def getMonthNamesList(self):
        monthNames = []
        for month in self.months:
            monthNames.append(month.monthName)

        return monthNames

    def getTotalMonthExpenses(self, monthNum):
        total = self.getMonthByNumber(monthNum).getCategory('totalExpenses')
        return total

# Static Functions #
def customFormat(amt):
    return '{:0,.2f}'.format(float(amt))

def pad(string, width, padChar=' '):
    return string.ljust(width, padChar)