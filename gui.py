from tkinter import *
from tkinter import ttk
import simObjects as so
import populationManager as pm

def runPlayback(*args):
    if not simRunning.get():
        simRunning.set(True)
        try:
            testPop = pm.loadPop("fastTest", genNumber.get())
            simRunning.set(so.playback(0, testPop.creatures))
        except:
            print("something went wrong with the sim")
            simRunning.set(False)

root = Tk()
root.title("Python EvoSim GUI")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

simRunning = BooleanVar()
simRunning.set(False)

genName = StringVar()
gen_name_entry = ttk.Entry(mainframe, width = 7, textvariable = genName)
gen_name_entry.grid(column=1, row=3, sticky=(W, E))

genNumber = IntVar()
gen_num_entry = ttk.Entry(mainframe, width = 7, textvariable = genNumber)
gen_num_entry.grid(column=2, row=3, sticky=(W, E))

ttk.Button(mainframe, text="Playback", command=runPlayback).grid(column=3, row=3, sticky=W)


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()