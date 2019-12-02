#!/usr/bin/python3
"keyboard.py - a simulation of the Apollo DiSplayKeYboard"

import tkinter as tk

class DSKY(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()


def p_verb():
    print('VERB')

def p_noun():
    print('NOUN')

def p_entr():
    print('ENTR')

def p_rset():
    print('RSET')

def p_clr():
    print('CLR')

def p_pro():
    print('PRO')

def p_key():
    print('KEY REL')



def push_p():
    print('+')

def push_m():
    print('-')

def push_0():
    print('0')

def push_1():
    print('1')

def push_2():
    print('2')

def push_3():
    print('3')

def push_4():
    print('4')

def push_5():
    print('5')

def push_6():
    print('6')

def push_7():
    print('7')

def push_8():
    print('8')

def push_9():
    print('9')

topwin = DSKY()

numbers = tk.Frame(topwin, width=400, height=300)
numbers.pack()

byebye = tk.Button(topwin, fg='red', text="QUIT", command=topwin.destroy)
byebye.pack()



verb = tk.Button(numbers, fg='White', bg='Black', text="VERB", command=p_verb)
noun = tk.Button(numbers, fg='White', bg='Black', text="NOUN", command=p_noun)
entr = tk.Button(numbers, fg='White', bg='Black', text="ENTR", command=p_entr)
rset = tk.Button(numbers, fg='White', bg='Black', text="RSET", command=p_rset)
clr = tk.Button(numbers, fg='White', bg='Black', text="CLR", command=p_clr)
pro = tk.Button(numbers, fg='White', bg='Black', text="PRO", command=p_pro)
key = tk.Button(numbers, fg='White', bg='Black', text="KEY\nREL", command=p_key)
nump = tk.Button(numbers, fg='White', bg='Black', text="+", command=push_p)
numm = tk.Button(numbers, fg='White', bg='Black', text="-", command=push_m)
num0 = tk.Button(numbers, fg='White', bg='Black', text="0", command=push_0)
num1 = tk.Button(numbers, fg='White', bg='Black', text="1", command=push_1)
num2 = tk.Button(numbers, fg='White', bg='Black', text="2", command=push_2)
num3 = tk.Button(numbers, fg='White', bg='Black', text="3", command=push_3)
num4 = tk.Button(numbers, fg='White', bg='Black', text="4", command=push_4)
num5 = tk.Button(numbers, fg='White', bg='Black', text="5", command=push_5)
num6 = tk.Button(numbers, fg='White', bg='Black', text="6", command=push_6)
num7 = tk.Button(numbers, fg='White', bg='Black', text="7", command=push_7)
num8 = tk.Button(numbers, fg='White', bg='Black', text="8", command=push_8)
num9 = tk.Button(topwin, fg='White', bg='Black', text="9", command=push_9)


verb.place(x=10, y=125, width=42, height=42)
noun.place(x=10, y=170, width=42, height=42)

nump.place(x=55, y=100, width=42, height=42)
numm.place(x=55, y=150, width=42, height=42)
num0.place(x=55, y=200, width=42, height=42)

num7.place(x=100, y=100, width=42, height=42)
num4.place(x=100, y=150, width=42, height=42)
num1.place(x=100, y=200, width=42, height=42)

num8.place(x=145, y=100, width=42, height=42)
num5.place(x=145, y=150, width=42, height=42)
num2.place(x=145, y=200, width=42, height=42)

num9.place(x=190, y=100, width=42, height=42)
num6.place(x=190, y=150, width=42, height=42)
num3.place(x=190, y=200, width=42, height=42)

clr.place(x=235, y=100, width=42, height=42)
pro.place(x=235, y=150, width=42, height=42)
key.place(x=235, y=200, width=42, height=42)

entr.place(x=280, y=125, width=42, height=42)
rset.place(x=280, y=170, width=42, height=42)


topwin.mainloop()
