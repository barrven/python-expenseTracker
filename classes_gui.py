from tkinter import *
from tkinter import ttk
import datetime as dt
import calendar as cal
from tkinter.font import Font

class Window(Frame):
    def __init__(self, master, title, database, year):
        Frame.__init__(self, master)
        
        self.master = master
        self.master.title(title)
        self.pack(fill = BOTH, expand = True)

        self.menu = Menu(self.master)
        self.master.config(menu = self.menu)

        self.database=database
        self.year=year
        self.now = dt.datetime.now()

        # todo: define customized font settings
        font = ('', 20)

        # commands to populate the menu bar
        # todo: fix bug where moving from view to enter generates error: "enter() takes 1 positional argument but 4 were given"
        # todo: remove lambdas
        self.menu.add_command(label='Home', command=lambda:self.home(title, database, year))
        self.menu.add_command(label='Enter', command=lambda:self.enter(title, database, year))
        self.menu.add_command(label='View', command=lambda:self.view(title, database, year))
        self.menu.add_command(label='Change Year', command=lambda:self.change_year(title, database, year))

    # desired functions for menu bar
    def home(self, title, database, year):
        self.destroy()
        Home(self.master, title, database, year)

    def enter(self, title, database, year):
        self.destroy()
        Enter(self.master, title, database, year)
    
    def view(self, title, database, year):
        self.destroy()
        View(self.master, title, database, year)

    def change_year(self, title, database, year):
        self.destroy()
        ChangeYear(self.master, title, database, year)

    def validate_number(self, char):
        return char.isdigit()


class Home(Window):
    def __init__(self, master, title, database, year):
        Window.__init__(self, master, title, database, year)
        
        # for each subclass of Window define contents here

        content_frame = Frame(master=self)
        content_frame.pack(expand = True, fill = BOTH, pady=180)


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
        # todo: change this so that months display to user as words rather than numbers
        self.months_dropdown['values'] = self.year.getEmptyMonths()  # get list of month numbers that have no associated data
        self.months_dropdown.grid(column=1, row=0)

        # sets up method to make sure only number are allowed in the input boxes
        # todo: modify so that decimal values are possible to enter. currently only integer values are poossible
        validation = self.master.register(self.validate_number)
        
        #setup loop to create labels and entry boxes
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

        # self.btn_check = Button(master=content_frame, text='Check Month Val', command=self.check, width=widget_width_val)
        # self.btn_check.grid(column=1, row=self.num_categories+2, pady=20, padx=col_pad_value)

    def clear(self):
        self.months_dropdown.set('')
        for cat in self.entry_category_objects:
            cat.delete(0, END)

    def submit(self):
        if self.is_valid_entry():
            entry_values = []
            for entry in self.entry_category_objects:
                entry_values.append(entry.get())
            success_check = self.year.addMonth_flex(self.months_dropdown.get(), entry_values) # try to add month to database via year object
            if success_check:
                msg = 'Data for month added'
                self.months_dropdown['values'] = self.year.getEmptyMonths()
                self.clear()
            else:
                msg = 'Data could not be added'

            Popup(msg)

    # def check(self):
    #     print(self.months_dropdown.get())

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
        content_frame = Frame(master=self, pady=20)
        content_frame.pack()
        
        # todo: figure out how to show a message here, e.g. "Select Month" as the initial value
        string_var = StringVar()
        self.months_dropdown = ttk.Combobox(content_frame, textvariable=string_var, state='readonly',  width=15)
        
        # todo: change this vals list to a list supplied by the year object (need month to number method first)
        vals = ['jan', 'feb', 'mar'] 
        self.months_dropdown['values'] = vals
        self.months_dropdown.grid(column=0, row=0, pady=20, sticky=W)

        # enter button....
        self.btn_enter = Button(content_frame, text='Enter', command=self.enter, width=10)
        self.btn_enter.grid(column=1, row=0, padx=5, sticky=W)

        # current year label....
        yrMsg = 'Current Year: ' + str(self.year.yearNum)
        self.lbl_currYear = Label(content_frame, text=yrMsg)
        self.lbl_currYear.grid(column=2, row=0, padx=5, sticky=W)

        # change year button....
        self.btn_changeYear = Button(content_frame, text='Change', command=self.change_year, width=8)
        self.btn_changeYear.grid(column=3, row=0, padx=5, sticky=W, )

        titles = ['', 'Amount', 'Year Avg', '% of Total']
        data = year.getMonthData(1)
        data_table = Table(content_frame, titles, data)
        data_table.grid(column=0, row=1, columnspan=4, padx=5)
        

        # self.btn_check = Button(master=content_frame, text='Check Month Val', command=self.check, width=widget_width_val)
        # self.btn_check.grid(column=1, row=self.num_categories+2, pady=20, padx=col_pad_value)


    def enter(self):
        print(self.months_dropdown.get())




class ChangeYear(Window):
    def __init__(self, master, title, database, year):
        Window.__init__(self, master, title, database, year)
        
        # for each subclass of Window define contents here
        lbl_hi = Label(self, text='Change the year here, motherfucker')
        lbl_hi.pack()
    


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
                # cell.grid(row=(i+1), column=j, pady=self.border_width, padx=self.border_width, sticky=NSEW)
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