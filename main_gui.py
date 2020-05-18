#########################
## 2020-4-30           ##
## Barrington Venables ##
#########################

from tkinter import *
from classes_gui import *
from year import *
from database import *
import datetime as dt

def main():
    
    database = Database('expenseRecords.db')
    currentYear = dt.datetime.now().year
    year = Year(currentYear, database)

    w = Tk()
    w.geometry('500x500')
    # Home(w, title='Expense Tracker 2.0', database=database, year=year)
    # Enter(w, title='Expense Tracker 2.0', database=database, year=year)


    View(w, title='Expense Tracker 2.0', database=database, year=year)
    w.mainloop()

if __name__ == "__main__":
    main()