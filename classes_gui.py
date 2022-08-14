from tkinter import *
from tkinter import ttk
import datetime as dt
import calendar as cal
from tkinter.font import Font
import year

class Window(Frame):
    def __init__(self, master, title, database, year):
        Frame.__init__(self, master)
        
        self.master = master
        self.title = title
        self.database = database
        self.year = year
        
        self.master.title(self.title)
        self.pack(fill=BOTH, expand=True)

        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)

        self.now = dt.datetime.now()

        # todo: define customized font settings
        font = ('', 20)

        # commands to populate the menu bar
        self.menu.add_command(label='Home', command=self.home)
        self.menu.add_command(label='Enter', command=self.enter)
        self.menu.add_command(label='View', command=self.view)
        self.menu.add_command(label='Change Year', command=self.change_year)

    # desired functions for menu bar
    def home(self):
        self.destroy()
        Home(self.master, self.title, self.database, self.year)

    def enter(self):
        self.destroy()
        Enter(self.master, self.title, self.database, self.year)
    
    def view(self):
        self.destroy()
        View(self.master, self.title, self.database, self.year)

    def change_year(self):
        self.destroy()
        ChangeYear(self.master, self.title, self.database, self.year)

    def validate_number(self, char):
        return char.isdigit()


class Home(Window):
    def __init__(self, master, title, database, year):
        Window.__init__(self, master, title, database, year)
        
        # for each subclass of Window define contents here

        content_frame = Frame(master=self)
        content_frame.pack(expand = True, fill=BOTH, pady=180)


        lbl_year = Label(content_frame, text='The current year is: ' + str(self.year.yearNum))
        lbl_year.pack()

        curr_mth = self.year.getMonthByNumber(self.now.month)
        if curr_mth:
            curr_mth_exp = curr_mth.totalExpenses
            msg = 'The current month\'s expenses are: ' + "${:,.2f}".format(curr_mth_exp)
        else:
            msg = 'There are no expenses entered for ' + str(dt.datetime.now().strftime('%B'))
            
        lbl_currMonthExp = Label(content_frame, text=msg)
        lbl_currMonthExp.pack()

        days_in_month = cal.monthrange(self.now.year, self.now.month)[1]
        days_left_in_month = days_in_month - self.now.day

        lbl_daysLeft = Label(content_frame, text='Days to end of month: ' + str(days_left_in_month))
        lbl_daysLeft.pack()



class Enter(Window):
    def __init__(self, master, title, database, year):
        Window.__init__(self, master, title, database, year)
        
        # for each subclass of Window define contents here

        content_frame = Frame(master=self, padx=0, pady=20)
        content_frame.pack()

        row_pad_value = 10
        col_pad_value = 10
        widget_width_val = 12

        Label(master=content_frame, text='Select Month').grid(column=0, row=0, sticky='w', pady=row_pad_value, padx=row_pad_value)
        
        string_var = StringVar()
        self.months_dropdown = ttk.Combobox(content_frame, textvariable=string_var, state='readonly',  width=widget_width_val)
        
        empty_months_list = self.year.getEmptyMonths()
        self.months_dropdown['values'] = self.year.switchMonthStringsAndNums(empty_months_list)  # get list of month numbers that have no associated data
        self.months_dropdown.grid(column=1, row=0)

        # sets up method to make sure only number are allowed in the input boxes
        # todo: modify so that decimal values are possible to enter. currently only integer values are possible
        validation = self.master.register(self.validate_number)
        
        # setup loop to create labels and entry boxes
        self.entry_category_objects = []
        labels = ['Rent', 'Grocery', 'Utilities', 'Transit', 'Shopping', 'Entertainment']
        self.num_categories = len(labels)

        # add all the entry widgets into the frame
        for i in range(self.num_categories):
            Label(master=content_frame, text=labels[i]).grid(column=0, row=i+1, sticky='w', padx=col_pad_value, pady=row_pad_value)
            self.entry_category_objects.append(
                Entry(content_frame, validate='key', validatecommand=(validation, '%S'), width=widget_width_val+3)
            )
            self.entry_category_objects[i].grid(column=1, row=i+1)

        self.btn_clear = Button(master=content_frame, text='Clear', command=self.clear, width=widget_width_val)
        self.btn_clear.grid(column=0, row=self.num_categories+1, pady=20, padx=col_pad_value)
        
        self.btn_enter = Button(master=content_frame, text='Submit', command=self.submit, width=widget_width_val)
        self.btn_enter.grid(column=1, row=self.num_categories+1, pady=20, padx=col_pad_value)

    def clear(self):
        self.months_dropdown.set('')
        for cat in self.entry_category_objects:
            cat.delete(0, END)

    def submit(self):
        if self.is_valid_entry():
            entry_values = []
            for entry in self.entry_category_objects:
                entry_values.append(entry.get())

            # switch the month string back to an integer before adding to the DB
            month_num = self.year.switchMonthStringToInt(self.months_dropdown.get())
            success_check = self.year.addMonth_flex(month_num, entry_values)  # try to add month to database via year object
            if success_check:
                msg = 'Data for month added'
                self.months_dropdown['values'] = self.year.switchMonthStringsAndNums(self.year.getEmptyMonths())
                self.clear()
            else:
                msg = 'Data could not be added'

            Popup(msg)

    def is_valid_entry(self):
        if self.months_dropdown.get() == '':
            Popup('Please do not leave any entry blank')
            return False

        for entry in self.entry_category_objects:
            if entry.get() == '':
                Popup('Please do not leave any entry blank')
                return False
        
        return True
        


class View(Window):
    def __init__(self, master, title, database, year):
        Window.__init__(self, master, title, database, year)

        # for each subclass of Window define contents here
        self.content_frame = Frame(master=self, pady=20)
        self.content_frame.pack()

        vals = self.year.getMonthNamesList()
        vals.insert(0, 'Select Month')  # inserts the user instruction as the first value in the list (prob bad way of doing this)
        self.cmb_months = DropdownBox(self.content_frame, vals)
        self.cmb_months.grid(column=0, row=0, pady=20, sticky=W)

        # enter button....
        self.btn_enter = Button(self.content_frame, text='Submit', command=self.submit_sel_month, width=10)
        self.btn_enter.grid(column=1, row=0, padx=5, sticky=W)

        # current year label....
        yrMsg = 'Current Year: ' + str(self.year.yearNum)
        self.lbl_currYear = Label(self.content_frame, text=yrMsg)
        self.lbl_currYear.grid(column=2, row=0, padx=5, sticky=W)

        # change year button....
        self.btn_changeYear = Button(self.content_frame, text='Change', command=self.change_year, width=8)
        self.btn_changeYear.grid(column=3, row=0, padx=5, sticky=W, )

        # placeholder for data_table
        self.data_table = None
       
    def submit_sel_month(self):
        if self.cmb_months.get() == 'Select Month':
           Popup('No month selected')
        
        else:
            if self.data_table is not None:
                self.data_table.destroy()
            titles = ['', 'Amount', 'Year Avg', '% of Total']
            monthNum = self.year.switchMonthStringToInt(self.cmb_months.get())
            data = self.year.getMonthData(monthNum)
            self.data_table = Table(self.content_frame, titles, data)
            self.data_table.grid(column=0, row=1, columnspan=4, padx=5)

            # total expenses label....
            month_expenses = self.year.getTotalMonthExpenses(monthNum)
            
            tot_exp_msg = 'Total Expenses: $' + '{:0,.2f}'.format(float(month_expenses))
            self.lbl_totalExpenses = Label(self.content_frame, text=tot_exp_msg, pady=20)
            self.lbl_totalExpenses.grid(column=0, row=2, columnspan=4)

            # year avg compare with month label....
            year_avg = self.year.getCatAvg('totalExpenses')
            year_avg_string = '{:0,.2f}'.format(float(year_avg))
            if month_expenses < year_avg:
                year_avg_msg = 'This month is below average for the year (${})'.format(year_avg_string)
            elif month_expenses > year_avg:
                year_avg_msg = 'This month is above average for the year (${})'.format(year_avg_string)
            else:
                year_avg_msg = 'This month is exactly average for the year'

            self.lbl_yearAvg_msg = Label(self.content_frame, text=year_avg_msg, pady=10)
            self.lbl_yearAvg_msg.grid(column=0, row=3, columnspan=4)


    


class ChangeYear(Window):
    def __init__(self, master, title, database, year):
        Window.__init__(self, master, title, database, year)
        
        # for each subclass of Window define contents here
        self.content_frame = Frame(master=self, pady=20)
        self.content_frame.pack(pady=50)

        self.draw_currYear_label()

        import datetime as dt
        currentYear = dt.datetime.now().year
        vals = ['Select Year']  # default value of the select year dropdown
        for i in range(1999, (currentYear+1)):
            vals.append(i)

        self.year_dropdown = DropdownBox(self.content_frame, vals)
        self.year_dropdown.grid(column=0, row=2, pady=10, sticky=NSEW)

        btn_submit = Button(self.content_frame, text='Submit', command=self.exec_change_year, width=15)
        btn_submit.grid(column=0, row=3, pady=10, sticky=NSEW)
    
    def draw_currYear_label(self):
        msg = 'Current Year is: ' + str(self.year.yearNum)
        self.lbl_currYear = Label(self.content_frame, text=msg)
        self.lbl_currYear.grid(column=0, row=1, pady=10, sticky=NSEW)

    def exec_change_year(self):
        new_year = self.year_dropdown.get()
        if new_year == 'Select Year':
            return
        self.year = year.Year(new_year, self.database)
        self.lbl_currYear.destroy()
        self.draw_currYear_label()
        Popup('Year changed successfully to ' + str(new_year))

    


class Popup(Tk):
    def __init__(self, msg, size='300x150'):
        Tk.__init__(self)
        self.msg = msg
        self.geometry(size)
        Label(self, text=self.msg).pack(pady=10)
        Button(self, text='Ok', command=self.close, width=15).pack(pady=10)
        self.mainloop()

    def close(self):
        self.destroy()



class Table(Frame):
    def __init__(self, master, header_titles=[], data=[[]], border_width=1, border_color='black'):
        Frame.__init__(self, master)
        self.num_rows = len(data)
        self.num_cols = len(data[0])
        self.header_titles = header_titles
        self.data = data
        self.border_width = (border_width/2)
        self.border_color = border_color

        self.draw_table()
    

    def draw_table(self):
        borders = Frame(self, bg=self.border_color)
        borders.pack(expand=YES)

        # draw the header
        for i in range(self.num_cols):
            cell = Cell(borders, self.header_titles[i], bg_color='black', fg_color='white')
            cell.grid(row=0, column=i, pady=self.border_width, padx=self.border_width, sticky=NSEW)

        # draw the data records
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                cell = Cell(borders, self.data[i][j])
                cell.grid(row=(i+1), column=j, pady=0.5, padx=0.5, sticky=NSEW)



# todo: make Cell inherit from label instead of bothering with frame first
# todo: allow for left or right justification in cells
class Cell(Frame):
    def __init__(self, master, data, bg_color='white', fg_color='black'):
        Frame.__init__(self, master, bg=bg_color)
        self.master = master
        self.data = str(data)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.label = Label(self, text=self.data, bg=self.bg_color, fg=self.fg_color)
        self.place_label()

    def place_label(self):
        self.label.pack(expand=YES, pady=2, padx=2)


class DropdownBox(Frame):
    def __init__(self, master, values):
        Frame.__init__(self, master)
        self.master = master
        self.values = values
        self.combo()

    def combo(self):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self, textvariable=self.box_value, state='readonly')
        self.box['values'] = self.values
        self.box.current(0)
        self.box.pack(expand=YES)

    def get(self):
        return self.box.get()