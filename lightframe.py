#!/usr/bin/python3
# dsky.py - a DiSplay KeYboard emulator

import tkinter as tk

# docstring
class Lights(tk.Frame):
    # class docstring
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        # White Lights

        self.uplink = tk.Label(self, bg="white", bd=2, width=8, height=3)
        self.uplink["text"] = "UPLINK\nACTY"
        self.uplink.grid(row=0,column=0)

        self.noatt = tk.Label(self, bg="white", bd=2, width=8, height=3)
        self.noatt["text"] = "NO ATT"
        self.noatt.grid(row=1,column=0)

        self.stby = tk.Label(self, bg="white", bd=2, width=8, height=3)
        self.stby["text"] = "STBY"
        self.stby.grid(row=2,column=0)

        self.keyrel = tk.Label(self, bg="white", bd=2, width=8, height=3)
        self.keyrel["text"] = "KEY REL"
        self.keyrel.grid(row=3,column=0)

        self.oprerr = tk.Label(self, bg="white", bd=2, width=8, height=3)
        self.oprerr["text"] = "OPR ERR"
        self.oprerr.grid(row=4,column=0)

        self.empty1 = tk.Label(self, bg="white", bd=2, width=8, height=3)
        self.empty1["text"] = ""
        self.empty1.grid(row=5,column=0)

        self.empty2 = tk.Label(self, bg="white", bd=2, width=8, height=3)
        self.empty2["text"] = ""
        self.empty2.grid(row=6,column=0)


        # Yellow Lights

        self.temp = tk.Label(self, bg="yellow", bd=2, width=8, height=3)
        self.temp["text"] = "TEMP"
        self.temp.grid(row=0,column=1)

        self.gimbal = tk.Label(self, bg="yellow", bd=2, width=8, height=3)
        self.gimbal["text"] = "GIMBAL\nLOCK"
        self.gimbal.grid(row=1,column=1)

        self.prog = tk.Label(self, bg="yellow", bd=2, width=8, height=3)
        self.prog["text"] = "PROG"
        self.prog.grid(row=2,column=1)

        self.restart = tk.Label(self, bg="yellow", bd=2, width=8, height=3)
        self.restart["text"] = "RESTART"
        self.restart.grid(row=3,column=1)

        self.tracker = tk.Label(self, bg="yellow", bd=2, width=8, height=3)
        self.tracker["text"] = "TRACKER"
        self.tracker.grid(row=4,column=1)

        self.alt = tk.Label(self, bg="yellow", bd=2, width=8, height=3)
        self.alt["text"] = "ALT"
        self.alt.grid(row=5,column=1)

        self.vel = tk.Label(self, bg="yellow", bd=2, width=8, height=3)
        self.vel["text"] = "VEL"
        self.vel.grid(row=6,column=1)



        self.quit = tk.Button(self, text="QUIT", fg="red",
                command=topwin.destroy)
        self.quit.grid(row=18,column=1)

class Numerics(tk.Frame):
    # class docstring
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        # buttons

        self.bverb = tk.Button(self, fg='White',bg='Black', text="VERB")
        self.bnoun = tk.Button(self, fg='White',bg='Black', text="NOUN")
        self.bentr = tk.Button(self, fg='White',bg='Black', text="ENTR")
        self.brset = tk.Button(self, fg='White',bg='Black', text="RSET")
        self.bclr  = tk.Button(self, fg='White',bg='Black', text="CLR")
        self.bpro  = tk.Button(self, fg='White',bg='Black', text="PRO")

        self.bverb.place(x = 10, y =  25, width = 42, height = 42)
        self.bnoun.place(x = 10, y =  70, width = 42, height = 42)



#topwin = tk.Tk()
#app = Lights(master=topwin)
#app2 = Numerics(master=topwin)
#
##app.master.title("DSKY Lights")
#topwin.title("topwin DSKY Lights")
#topwin.minsize(600, 600)
#topwin.mainloop()
#
