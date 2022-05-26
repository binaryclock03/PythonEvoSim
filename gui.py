from tkinter import *
from tkinter import ttk
import bin.simObjects as so
import bin.populationManager as pm
import bin.simulations as sim

def runPlayback(*args):
    if not simRunning.get():
        simRunning.set(True)
        try:
            testPop = pm.loadPop(popName.get(), genNumber.get())
            simRunning.set(sim.playback(0, testPop.getPreview()))
        except:
            print("something went wrong with the sim")
            simRunning.set(False)

def showCreatures(*args):
    if not simRunning.get():
        simRunning.set(True)
        try:
            testPop = pm.loadPop(popName.get(), genNumber.get())
            simRunning.set(sim.showCreatures(0, testPop.creatures))
        except:
            print("something went wrong with the sim")
            simRunning.set(False)

def showPreview(*args):
    if not simRunning.get():
        simRunning.set(True)
        try:
            testPop = pm.loadPop(popName.get(), genNumber.get())
            simRunning.set(sim.showCreatures(0, testPop.getPreview()))
        except:
            print("something went wrong with the sim")
            simRunning.set(False)

if __name__ == '__main__':
    root = Tk()
    root.title("Python EvoSim GUI")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    simRunning = BooleanVar()
    simRunning.set(False)

    popName = StringVar()
    pop_name_entry = ttk.Entry(mainframe, width = 16, textvariable = popName)
    pop_name_entry.grid(column=1, row=3, sticky=(W, E))

    genNumber = IntVar()
    gen_num_entry = ttk.Entry(mainframe, width = 8, textvariable = genNumber)
    gen_num_entry.grid(column=2, row=3, sticky=(W, E))

    ttk.Button(mainframe, text="Playback", command=runPlayback).grid(column=1, row=4, sticky=W)
    ttk.Button(mainframe, text="Show Creatures", command=showCreatures).grid(column=2, row=4, sticky=W)
    ttk.Button(mainframe, text="Show Preview", command=showPreview).grid(column=3, row=4, sticky=W)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    root.mainloop()