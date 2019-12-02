#!/usr/bin/python3
# dsky.py - a DiSplay KeYboard emulator

import tkinter as tk

root = tk.Tk()
root.geometry("200x400+30+30")

comp = tk.Label(root, fg='Black', bg='lightgrey', text="COMP\nACTY")
prog_name = tk.Label(root, fg='Black', bg='lightgrey', text="PROG")
prog_value = tk.Label(root, fg='Black', bg='lightgrey', text="13")
verb_name = tk.Label(root, fg='Black', bg='lightgrey', text="VERB")
verb_value = tk.Label(root, fg='Black', bg='lightgrey', text="33")
noun_name = tk.Label(root, fg='Black', bg='lightgrey', text="NOUN")
noun_value = tk.Label(root, fg='Black', bg='lightgrey', text="13")

num1 = tk.Label(root, fg='Black', bg='lightgrey', text="-92311")
num2 = tk.Label(root, fg='Black', bg='lightgrey', text="+13270")
num3 = tk.Label(root, fg='Black', bg='lightgrey', text="-46514")
num1['font'] = "terminal 36 bold"
num2['font'] = "terminal 36 bold"
num3['font'] = "terminal 36 bold"

verb_name['font'] = "terminal 12 bold"
verb_value['font'] = "terminal 26 bold"
noun_name['font'] = "terminal 12 bold"
noun_value['font'] = "terminal 26 bold"
noun_name['font'] = "terminal 12 bold"
prog_value['font'] = "terminal 26 bold"

quit = tk.Button(root, text="QUIT", fg="red",
                command=root.destroy)

comp.place(x =  10, y = 10, width=100, height=50)
prog_name.place(x = 115, y = 10, width=100, height=15)
prog_value.place(x = 115, y = 25, width=100, height=35)
verb_name.place(x =  10, y = 70, width=100, height=15)
verb_value.place(x =  10, y = 85, width=100, height=35)
noun_name.place(x = 115, y = 70, width=100, height=15)
noun_value.place(x = 115, y = 85, width=100, height=35)

num1.place(x =  10, y = 120, width=205, height=50)
num2.place(x =  10, y = 170, width=205, height=50)
num3.place(x =  10, y = 220, width=205, height=50)

quit.place(x=100, y = 300)


root.title("DSKY Numeric")
root.minsize(280, 400)
root.mainloop()

