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
        self.menu.add_command(label='Home', command=lambda:self.home(title, database, year))
        self.menu.add_command(label='Enter', command=lambda:self.enter(title, database, year))
        self.menu.add_command(label='View', command=lambda:self.view(title, database, year))
        self.menu.add_command(label='Display', command=lambda:self.change_year(title, database, year))

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
        self.months_dropdown['values'] = self.year.getEmptyMonths()  # get list of month numbers that have no associated data
        self.months_dropdown.grid(column=1, row=0)

        # sets up method to make sure only number are allowed in the input boxes
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
        
        self.top_frame = Frame(master=self, relief=SUNKEN, bg='red', borderwidth=5)
        self.top_frame.pack_propagate(0)
        self.top_frame.pack(pady=10)

        Label(self.top_frame, text='Fuck you, thkinter', width=10, height=10).grid(row=0, column=0)
        Label(self.top_frame, text='Fuck you, thkinter').grid(row=1, column=1)
        Label(self.top_frame, text='Fuck you, thkinter').grid(row=2, column=2)


        self.middle_frame = Frame(master=self, relief=SUNKEN, bg='red', borderwidth=5)
        self.middle_frame.pack_propagate(0)
        self.middle_frame.pack(pady=10)

        Label(self.middle_frame, text='Fuck you, thkinter', width=10, height=10).grid(row=0, column=0)
        Label(self.middle_frame, text='Fuck you, thkinter').grid(row=1, column=1)
        Label(self.middle_frame, text='Fuck you, thkinter').grid(row=2, column=2)


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
    def __init__(self, master, num_rows, num_cols, header_titles, rows):
        Frame.__init__(self, master)






class Row(Frame):
    def __init__(self, master, records_list, row_padding=0, col_padding=0, borderwidth=0):
        Frame.__init__(self, master)

        self.records_list = records_list
        self.num_records = len(records_list)

        for i in range(self.num_records):
            cell = Cell(master=self, data=self.records_list[i], border_width=1)
            cell.grid(row=0, column=i, pady=row_padding, padx=col_padding)

class Cell(Frame):
    def __init__(self, master, data, border_color='black', border_width=0):
        Frame.__init__(self, master, highlightbackground=border_color, highlightthickness=border_width)
        self.master = master
        self.data = str(data)
        self.border_color = border_color
        self.border_width = border_width
        self.label = Label(self, text=self.data)
        self.placeLabel()

    def placeLabel(self):
        self.label.pack(expand=YES, pady=2, padx=2)
