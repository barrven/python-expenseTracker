##########################################
# Barrington Venables                    #
# 101189284                              #
# comp2152 assignment - Expense manager  #
##########################################

class Month:
    def __init__(self, number, rent, groceries, utilities, transit, shopping, entertainment):
        self.number = number
        self.rent = rent
        self.groceries = groceries
        self.utilities = utilities
        self.transit = transit
        self.shopping = shopping
        self.entertainment = entertainment
        self.totalExpenses = rent + groceries + utilities + transit + shopping + entertainment
        monthNames = ['January', 'February', 'March', 'April',
                      'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.monthName = monthNames[number-1]

    def getCategory(self, category):
        if category == 'rent':
            return self.rent
        if category == 'groceries':
            return self.groceries
        if category == 'utilities':
            return self.utilities
        if category == 'transit':
            return self.transit
        if category == 'shopping':
            return self.shopping
        if category == 'entertainment':
            return self.entertainment
        if category == 'totalExpenses':
            return self.totalExpenses
        if category == 'monthName':
            return self.monthName

    def getCategoryPercent(self, category):
        cat = self.getCategory(category)
        return (cat / self.totalExpenses) * 100
