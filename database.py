##########################################
# Barrington Venables                    #
# 101189284                              #
# comp2152 assignment - Expense manager  #
##########################################

import sqlite3
from contextlib import closing
from month import *

class Database:
    def __init__(self, filePath):
        self.conn = sqlite3.connect(filePath)
        self.conn.row_factory = sqlite3.Row

    # returns list of month objects from specific year
    def getMonths(self, year):
        with closing(self.conn.cursor()) as c:
            query = '''select * from master where year = ? order by month asc'''
            c.execute(query, (year,))
            months = c.fetchall()
            monthsList = []  # list of month objects
            for month in months:
                temp = Month(
                    month['month'],
                    month['rent'],
                    month['groceries'],
                    month['utilities'],
                    month['transit'],
                    month['shopping'],
                    month['entertainment']
                )
                monthsList.append(temp)
        return monthsList  # items in this list are month objects

    def addMonthToDb(self, year, number, rent, groceries, utilities, transit, shopping, entertainment):
        args = (year, number, rent, groceries, utilities, transit, shopping, entertainment)

        try:
            with closing(self.conn.cursor()) as c:
                query = '''insert into master values(?, ?, ?, ?, ?, ?, ?, ?)'''
                c.execute(query, args)
                self.conn.commit()
            return True
        except sqlite3.Error as e:
            print('An error occurred: ', e)
            return False

    def addMonthToDb_flex(self, year_num, month_num, categories_list):
        temp = categories_list
        temp.insert(0, month_num)
        temp.insert(0, year_num)
        args = tuple(temp)
        print(args)
        query = 'insert into master values(' + '?, ' * len(args)
        query = query[:-2] + ')'

        try:
            with closing(self.conn.cursor()) as c:
                c.execute(query, args)
                self.conn.commit()
            return True
        except sqlite3.Error as e:
            print('An error occurred: ', e)
            return False