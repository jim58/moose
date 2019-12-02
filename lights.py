#!/usr/bin/python3
"LightFrame.py - status lights for the DiSplay KeYboard emulator"

import tkinter as tk

class LightFrame(tk.Frame):
    "class docstring"
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        "create the lights"

        # White LightFrame

        self.uplink = tk.Label(self, bg="white", width=8, height=3)
        self.uplink["text"] = "UPLINK\nACTY"
        self.uplink.grid(row=0, column=0)

        self.noatt = tk.Label(self, bg="white", width=8, height=3)
        self.noatt["text"] = "NO ATT"
        self.noatt.grid(row=1, column=0)

        self.stby = tk.Label(self, bg="white", width=8, height=3)
        self.stby["text"] = "STBY"
        self.stby.grid(row=2, column=0)

        self.keyrel = tk.Label(self, bg="white", width=8, height=3)
        self.keyrel["text"] = "KEY REL"
        self.keyrel.grid(row=3, column=0)

        self.oprerr = tk.Label(self, bg="white", width=8, height=3)
        self.oprerr["text"] = "OPR ERR"
        self.oprerr.grid(row=4, column=0)

        self.empty1 = tk.Label(self, bg="white", width=8, height=3)
        self.empty1["text"] = ""
        self.empty1.grid(row=5, column=0)

        self.empty2 = tk.Label(self, bg="white", width=8, height=3)
        self.empty2["text"] = ""
        self.empty2.grid(row=6, column=0)


        # Yellow LightFrame

        self.temp = tk.Label(self, bg="yellow", width=8, height=3)
        self.temp["text"] = "TEMP"
        self.temp.grid(row=0, column=1)

        self.gimbal = tk.Label(self, bg="yellow", width=8, height=3)
        self.gimbal["text"] = "GIMBAL\nLOCK"
        self.gimbal.grid(row=1, column=1)

        self.prog = tk.Label(self, bg="yellow", width=8, height=3)
        self.prog["text"] = "PROG"
        self.prog.grid(row=2, column=1)

        self.restart = tk.Label(self, bg="yellow", width=8, height=3)
        self.restart["text"] = "RESTART"
        self.restart.grid(row=3, column=1)

        self.tracker = tk.Label(self, bg="yellow", width=8, height=3)
        self.tracker["text"] = "TRACKER"
        self.tracker.grid(row=4, column=1)

        self.alt = tk.Label(self, bg="yellow", width=8, height=3)
        self.alt["text"] = "ALT"
        self.alt.grid(row=5, column=1)

        self.vel = tk.Label(self, bg="yellow", width=8, height=3)
        self.vel["text"] = "VEL"
        self.vel.grid(row=6, column=1)



        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=topwin.destroy)
        self.quit.grid(row=18, column=1)


topwin = tk.Tk()
lights = LightFrame(master=topwin)
lights.master.title("DSKY LightFrame")
lights.master.minsize(200, 400)
lights.mainloop()
