# python program demonstrating 
# Combobox widget using tkinter 


# import tkinter as tk
# from tkinter import ttk

# # Creating tkinter window 
# window = tk.Tk()
# window.title('Combobox')
# window.geometry('500x250')

# # label text for title 
# ttk.Label(window, text="GFG Combobox Widget", background='green', foreground="white", font=("Times New Roman", 15)).grid(row=0, column=1)
# # label 
# ttk.Label(window, text="Select the Month :", font=("Times New Roman", 10)).grid(column=0, row=5, padx=10, pady=25)

# # Combobox creation 
# n = tk.StringVar()
# month_chosen = ttk.Combobox(window, width=27, textvariable=n, state='readonly')

# # Adding combobox drop down list
# month_chosen['values'] = (' January',
#                           ' February',
#                           ' March',
#                           ' April',
#                           ' May',
#                           ' June',
#                           ' July',
#                           ' August',
#                           ' September',
#                           ' October',
#                           ' November',
#                           ' December')

# month_chosen.grid(column=1, row=5)
# # month_chosen.current()

# def checkVal():
#     print(month_chosen.current())
#     print(month_chosen.get())

# tk.Button(window, text='Check Value', command=checkVal).grid(column=0, row=6, pady=25)

# window.mainloop()



####################################################################################################################################



# import tkinter as tk

# class window2:
#     def __init__(self, master1):
#         self.panel2 = tk.Frame(master1)
#         self.panel2.grid()
#         self.button2 = tk.Button(self.panel2, text = "Quit", command = self.panel2.quit)
#         self.button2.grid()
#         vcmd = (master1.register(self.validate),
#                 '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
#         self.text1 = tk.Entry(self.panel2, validate = 'key', validatecommand = vcmd)
#         self.text1.grid()
#         self.text1.focus()

#     def validate(self, action, index, value_if_allowed,
#                        prior_value, text, validation_type, trigger_type, widget_name):
#         if value_if_allowed:
#             try:
#                 float(value_if_allowed)
#                 return True
#             except ValueError:
#                 return False
#         else:
#             return False

# root1 = tk.Tk()
# window2(root1)
# root1.mainloop()


# import tkinter as tk

# w = tk.Tk()
# w.geometry('500x500')


# x = tk.Entry(w)
# x.pack(pady=20)


# def test():
#     temp = x.get()
#     print(temp)


# tk.Button(w, text='Try', command=test).pack(pady=20)


# w.mainloop()


############################################################################################################################


from tkinter import *


# create a root window. 
top = Tk() 

# create listbox object 
listbox = Listbox(top, height = 10, 
				width = 15, 
				bg = "grey", 
				activestyle = 'dotbox', 
				font = "Helvetica", 
				fg = "yellow") 

# Define the size of the window. 
top.geometry("300x250") 

# Define a label for the list. 
label = Label(top, text = " FOOD ITEMS") 

# insert elements by their 
# index and names. 
listbox.insert(1, "Nachos") 
listbox.insert(2, "Sandwich") 
listbox.insert(3, "Burger") 
listbox.insert(4, "Pizza") 
listbox.insert(5, "Burrito")

for i in range(6, 100):
    listbox.insert(i, 'Test ' + str(i))

# pack the widgets 
label.pack() 
listbox.pack() 


# Display untill User 
# exits themselves. 
top.mainloop() 
