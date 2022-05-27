import os
from tkinter import *
from tkinter import ttk
import populationManager as pm
import simulations as sim

class Gui():
    def __init__(self, root):
        self.root = root
        self.root.title("Python EvoSim GUI")

        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.simRunning = BooleanVar()
        self.simRunning.set(False)

        self.dirs = os.listdir("Populations")
        self.gens = []
        for gen in os.listdir("Populations\\"+self.dirs[0]):
            gen = gen.split("_")[2].split(".")[0]
            self.gens.append(gen)

        ttk.Label(self.mainframe, text="Population Name").grid(column=1, row=2, sticky=(W, E))
        ttk.Label(self.mainframe, text="Gen Number").grid(column=2, row=2, sticky=(W, E))

        self.popName = StringVar()
        self.popName.set(self.dirs[0])
        self.pop_dropdown = ttk.OptionMenu(self.mainframe, self.popName, *self.dirs)
        self.pop_dropdown.grid(column=1, row=3, sticky=(W,E))

        self.genNumber = StringVar()
        self.genNumber.set(self.gens[0])
        self.gen_dropdown = ttk.OptionMenu(self.mainframe, self.genNumber, *self.gens)
        self.gen_dropdown.grid(column=2, row=3, sticky=(W,E))

        ttk.Button(self.mainframe, text="Playback", command=self.runPlayback).grid(column=1, row=5, sticky=W)
        ttk.Button(self.mainframe, text="Show Creatures", command=self.showCreatures).grid(column=2, row=5, sticky=W)
        ttk.Button(self.mainframe, text="Show Preview", command=self.showPreview).grid(column=3, row=5, sticky=W)

        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        self.pop_dropdown.bind("<Enter>", self.updatePopDropdown)
        self.gen_dropdown.bind("<Enter>", self.updateGenDropdown)

    def runPlayback(self,*args):
        if not self.simRunning.get():
            self.simRunning.set(True)
            try:
                testPop = pm.loadPop(self.popName.get(), int(self.genNumber.get()))
                self.simRunning.set(sim.playback(0, testPop.getPreview()))
            except:
                print("something went wrong with the sim")
                self.simRunning.set(False)

    def showCreatures(self, *args):
        if not self.simRunning.get():
            self.simRunning.set(True)
            try:
                testPop = pm.loadPop(self.popName.get(), int(self.genNumber.get()))
                self.simRunning.set(sim.showCreatures(0, testPop.creatures))
            except:
                print("something went wrong with the sim")
                self.simRunning.set(False)

    def showPreview(self, *args):
        if not self.simRunning.get():
            self.simRunning.set(True)
            try:
                testPop = pm.loadPop(self.popName.get(), int(self.genNumber.get()))
                self.simRunning.set(sim.showCreatures(0, testPop.getPreview()))
            except:
                print("something went wrong with the sim")
                self.simRunning.set(False)

    def updatePopDropdown(self, *args):
        self.dirs = os.listdir("Populations")
        menu = self.pop_dropdown["menu"]
        menu.delete(0, "end")
        for string in self.dirs:
            menu.add_command(label=string,
                             command=lambda value=string: self.popName.set(value))

    def updateGenDropdown(self, *args):
        self.gens = []
        for gen in os.listdir("Populations\\"+self.popName.get()):
            gen = gen.split("_")[2].split(".")[0]
            self.gens.append(gen)
        menu = self.gen_dropdown["menu"]
        menu.delete(0, "end")
        for string in self.gens:
            menu.add_command(label=string,
                             command=lambda value=string: self.genNumber.set(value))

if __name__ == "__main__":
    root = Tk()
    Gui(root)
    root.mainloop()