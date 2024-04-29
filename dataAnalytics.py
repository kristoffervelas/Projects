import tkinter as tk
import os
import math
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import Label
from tkinter import Entry
from tkinter import filedialog
import pandas as pd
import lxml
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#maybe add a feature where you can store the information gathered on a file.

class Main():
    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Data Analysis")

        windowX = 1200
        windowY = 800
        #open dataset, user will do this once i implement
        self.dataset = pd.read_csv("WarFatalities.csv") 
        #"NFLX.csv"
        self.dropdownUsed = False        
        self.dropdownOptions = []
        self.datasetLength = len(self.dataset)
        self.bar1 = None
        self.window.geometry("%sx%s" % (str(windowX), str(windowY)))
        self.window.resizable(False, False)

        #for the graph type dropdown
        self.graphTypeOptions = ['line', 'bar', 'barh', 'hist', 'box', 'kde', 'density', 'area'] #pie and scatter cannot work rn

        self.wrangleDropdownOptions()

        #labels of columns as list
        #will be displayed for the user default
        self.datasetLabels = list(self.dataset.columns)

        self.datasetShape = self.dataset.shape #rowsxcols

        self.variableToRun = None  #functions will use this variable as output
        
        self.displayInit()

        self.window.mainloop()

        

    
    def displayInit(self):
        #run the display methods
        self.graphFrame()
        self.outputFrame()
        self.labelsFrame()
        self.optionsFrame()

    #will display all of these using grid
    #bg='color' for frame background
    #NOW YOU HAVE THE FRAMES, you can use the frame variables as the master window when packing the widgets inside each frame.
    def graphFrame(self):
        #im thinking this can either be a really long row showing the resultant row, but the whole thing can be turned into a graph too
        self.graphFrame = tk.Frame(self.window,borderwidth=2, height=350, width=1200, relief='flat')
        self.graphFrame.grid(row=0, column=0, columnspan=3)
        self.graphFrame.grid_propagate(False)

    #function to update text in outputFrame  WORKS!!!
    #use this when one of the options button is pressed
    def updateText(self):
        self.textWidget.config(state=tk.NORMAL)
        statement = ">> " + str(self.variableToRun) + "\n\n"
        self.textWidget.insert(tk.END, statement)
        self.textWidget.config(state=tk.DISABLED)

    def outputFrame(self):
        self.outputFrame = tk.Frame(self.window, bg='white',borderwidth=2, height=450, width=450, relief='sunken')
        self.outputFrame.grid(row=1, column=1)
        self.outputFrame.grid_propagate(False)
        self.textWidget = tk.Text(self.outputFrame, height=30, width=55, bg='black')
        self.textWidget.config(state=tk.DISABLED)
        self.textWidget.pack()
        #message output
        #DO NOT REMOVE
        self.variableToRun = "                   DATA OUTPUT\n-------------------------------------------------------"
        self.updateText()
        self.variableToRun = "OPERATIONS MENU GUIDE \n\nPULL VALUES A COLUMN WITH CONDITIONS:\n(Reference Column) (Condition in Reference Column) (Output Column)\nPress 'PULL' when ready.\n\nAVERAGE:\nEnter column to be averaged and press the 'Calculate Average' button.\n\nGET COLUMN:\n(Column Name) (Min Value) (Max Value)\nLeave the min and max empty if you want to pull all values in the column\n\nGRAPH:\n(X-Axis) (Y-Axis)\n\nDROPDOWN MENU:\nPick the starting index in the column(intervals of 100)\n\n-------------------------------------------------------\n"
        self.updateText()
        self.variableToRun = ""


    def labelsFrame(self):
        self.labelsFrame = tk.Frame(self.window, borderwidth=1, height=450, width=250, relief='groove')
        self.labelsFrame.grid(row=1, column=0)
        self.labelsFrame.grid_propagate(False)
    
        #selectmode will be a useful parameter for what im about to do
        self.labelsList = tk.Listbox(self.labelsFrame, height = 25, selectmode=tk.SINGLE)
        self.labelsList.pack(side=tk.LEFT)

        self.scrollbar = tk.Scrollbar(self.labelsFrame)
        self.scrollbar.pack(side=tk.RIGHT)

        self.labelsList.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command=self.labelsList.yview)

        for label in self.datasetLabels:
            self.labelsList.insert("end", label)

        #when an item is selected
        #self.labelsList.bind('<<ListboxSelect>>', functionName)

    def optionsFrame(self):

        #im thinking write the directions in the output frame
        #study tkinter StringVar()

        self.optionsFrame = tk.Frame(self.window,borderwidth=2, height=440, width=500, relief='raised')
        self.optionsFrame.grid(row=1, column=2)
        self.optionsFrame.grid_propagate(False)

        #use self.updateText() when putting the listbox selections into the text box
        #each row of operations will have its own frame

        #frame 1 (pull row using row from another column)
        self.pull_col_val_frame = tk.Frame(self.optionsFrame, width=500, borderwidth=0)
        self.pull_col_val_frame.pack(side=tk.TOP)
        
        self.pullFromThisCol = tk.Text(self.pull_col_val_frame, bd=2, height=1, width=20)
        self.pullFromThisCol.config(state=tk.NORMAL)
        self.pullFromThisCol.grid(row=0, column=0, padx=10, pady=10)

        self.nameOfPull = tk.Text(self.pull_col_val_frame, bd=2, height=1, width=20)
        self.nameOfPull.config(state=tk.NORMAL)
        self.nameOfPull.grid(row=0, column=1, padx=10, pady=10)

        self.colGrabFrom = tk.Text(self.pull_col_val_frame, bd=2, height=1, width=20)
        self.colGrabFrom.config(state=tk.NORMAL)
        self.colGrabFrom.grid(row=0, column=2, padx=10, pady=10)

        self.pullRowFromColButton = tk.Button(self.pull_col_val_frame, command=self.runPullRowFromCol, text="PULL", height=1, width=20)
        self.pullRowFromColButton.grid(row=1, columnspan=3, padx=3, pady=3)

        self.pullingDropdown = ttk.Combobox(self.pull_col_val_frame, state="readonly", values=["Pull Row", "Pull Column"])
        self.pullingDropdown.current(0)
        self.pullingDropdown.grid(row=2, columnspan=3, padx=10, pady=10)

        #frame 2 (average of column)
        self.averageOfColFrame = tk.Frame(self.optionsFrame, width=500, borderwidth=0)
        self.averageOfColFrame.pack(side=tk.TOP)

        self.colNameAve = tk.Text(self.averageOfColFrame, bd=2, height=1, width=20)
        self.colNameAve.config(state=tk.NORMAL)    
        self.colNameAve.grid(row=0, columnspan=2, padx=10, pady=10)

        self.getAveOfColButton = tk.Button(self.averageOfColFrame, text="Calculate Average",command=self.getAveOfColFunc, height=1, width=15)
        self.getAveOfColButton.grid(row=1, column=0, padx=3, pady=3)

        self.getMedianOfColButton = tk.Button(self.averageOfColFrame, text="Calculate Median", command=self.getMedianOfColFunc, height=1, width=15)
        self.getMedianOfColButton.grid(row=1, column=1, padx=3, pady=3)

        self.getMaxOfColButton = tk.Button(self.averageOfColFrame, command=self.getMaxOfColFunc, text='Get Max', height=1, width=15)
        self.getMaxOfColButton.grid(row=2, column=0, padx=3, pady=3)

        self.getMinOfColButton = tk.Button(self.averageOfColFrame, command=self.getMinOfColFunc, text='Get Min', height=1, width=15)
        self.getMinOfColButton.grid(row=2, column=1, padx=3, pady=3)
        #frame 3 (pull column)
        self.pullColumnFrame = tk.Frame(self.optionsFrame, width=500, borderwidth=0)
        self.pullColumnFrame.pack(side=tk.TOP)

        self.colNamePull = tk.Text(self.pullColumnFrame, bd=2, height=1, width=20)
        self.colNamePull.config(state=tk.NORMAL)
        self.colNamePull.grid(row=0, column=0, padx=10, pady=10)

        self.colMinPull = tk.Text(self.pullColumnFrame, bd=2, height=1, width=20)
        self.colMinPull.config(state=tk.NORMAL)
        self.colMinPull.grid(row=0, column=1, padx=10, pady=10)

        self.colMaxPull = tk.Text(self.pullColumnFrame, bd=2, height=1, width=20)
        self.colMaxPull.config(state=tk.NORMAL)
        self.colMaxPull.grid(row=0, column=2, padx=10, pady=10)

        self.pullColButton = tk.Button(self.pullColumnFrame,command=self.pullColumnFunction, text="Get Column", height=1, width=20)
        self.pullColButton.grid(row=1, columnspan=3, padx=3,pady=3)
        
        #frame 4(display graph)
        self.displayGraphFrame = tk.Frame(self.optionsFrame, width=500, borderwidth=0)
        self.displayGraphFrame.pack(side=tk.TOP)

        self.graphYInput = tk.Text(self.displayGraphFrame, bd=2, height=1, width=20)
        self.graphYInput.config(state=tk.NORMAL)
        self.graphYInput.grid(row=0, column=0, padx=10, pady=10)

        self.graphXInput = tk.Text(self.displayGraphFrame, bd=2, height=1, width=20)
        self.graphXInput.config(state=tk.NORMAL)
        self.graphXInput.grid(row=0, column=1, padx=10, pady=10)

        self.displayGraphButton = tk.Button(self.displayGraphFrame, command=self.displayGraph, text="Graph", height=1, width=20)
        self.displayGraphButton.grid(row=1, column=0, padx=3, pady=3)

        self.graphTypeDropdown = ttk.Combobox(self.displayGraphFrame, state="readonly", values=self.graphTypeOptions)
        self.graphTypeDropdown.grid(row=1, column=1, padx=3, pady=3)

        #frame 5 (dropdown for list splicing)
        self.dropdownFrame = tk.Frame(self.optionsFrame, width=500, borderwidth=0)
        self.dropdownFrame.pack(side=tk.TOP)

        self.dropdown = ttk.Combobox(self.dropdownFrame, state="readonly", values=self.dropdownOptions)
        self.dropdown.current(0)
        self.dropdown.grid(row=0, column=0, padx=10, pady=10)

        self.clearOutputButton = tk.Button(self.dropdownFrame, command=self.clearOutputFunc, text='Clear Output', height=1, width=20)
        self.clearOutputButton.grid(row=0, column=1, padx=10, pady=10)


    def clearOutputFunc(self):
        self.textWidget.config(state=tk.NORMAL)
        self.textWidget.delete("1.0", "end")
        self.textWidget.config(state=tk.DISABLED)
        self.variableToRun = ''
        self.variableToRun = "                   DATA OUTPUT\n-------------------------------------------------------"
        self.updateText()
        self.variableToRun = "OPERATIONS MENU GUIDE \n\nPULL VALUES A COLUMN WITH CONDITIONS:\n(Reference Column) (Condition in Reference Column) (Output Column)\nPress 'PULL' when ready.\n\nAVERAGE:\nEnter column to be averaged and press the 'Calculate Average' button.\n\nGET COLUMN:\n(Column Name) (Min Value) (Max Value)\nLeave the min and max empty if you want to pull all values in the column\n\nGRAPH:\n(X-Axis) (Y-Axis)\n\nDROPDOWN MENU:\nPick the starting index in the column(intervals of 100)\n\n-------------------------------------------------------\n"
        self.updateText()
        self.variableToRun = ""


    #GRAPH FRAME FUNCTIONS
    def displayGraph(self):
        #initialize graph
        try:
            if self.bar1:
                self.bar1.get_tk_widget().pack_forget()

            self.graphTypeChosen = self.graphTypeDropdown.get()
            self.figure1 = plt.Figure(figsize=(5, 3.5), dpi=100)
            self.ax1 = self.figure1.add_subplot(111)
            self.bar1 = FigureCanvasTkAgg(self.figure1, self.graphFrame)
            self.bar1.get_tk_widget().grid(row=0, column=0, padx=(300, 10))
            print('pressed')
            graphY = str(self.graphYInput.get("1.0", "end-1c"))
            graphX = str(self.graphXInput.get("1.0", "end-1c"))
            #initialization for the matplotlib for plotting graph
            df1 = self.dataset[[graphX, graphY]].groupby(graphX).sum()
            df1.plot(kind=self.graphTypeChosen, legend=True, ax=self.ax1)
            self.ax1.set_title(f'{graphX} x {graphY}')
        except Exception as e:
            self.variableToRun = ''
            self.variableToRun += "An error occured: " + str(type(e).__name__) + "\n" + str(e)
            self.updateText()
            #print("An error occured: ", type(e).__name__, "\n", e)

    #OPTIONS FRAME FUNCTIONS
    def pullColumnFunction(self):
        try:
            #for splicing
            userIndex = self.dropdown.get()
            #Reset variable to run
            self.variableToRun=""
            #variables for func
            colNameToGet = str(self.colNamePull.get("1.0", "end-1c"))
            colMinVal = self.colMinPull.get("1.0", "end-1c")
            colMaxVal = self.colMaxPull.get("1.0", "end-1c")

            #setting the default values if entry is empty
            if isinstance(self.dataset[colNameToGet].values[1], (int, float)):
                if len(colMinVal) == 0:
                    colMinVal = min(self.dataset[colNameToGet].values)
                if len(colMaxVal) == 0:
                    colMaxVal = max(self.dataset[colNameToGet].values)

            #print out rows in that column respective to the min and max
            self.variableToRun += "Showing results for " + colNameToGet + " (" + str(userIndex) + " - " + str(int(userIndex) + 100) + ")\n"
            for row in self.dataset[colNameToGet].values[int(userIndex):int(userIndex) + 100]:
                if isinstance(row, (int, float)): 
                    if float(row) >= float(colMinVal) and float(row) <= float(colMaxVal): 
                        self.variableToRun += " - " + str(row) + "\n"
                else:
                        self.variableToRun += " - " + str(row) + "\n"
            self.updateText()
            print(self.variableToRun)
        except Exception as e:
            self.variableToRun = ''
            self.variableToRun += "An error occured: " + str(type(e).__name__) + "\n" + str(e)
            self.updateText()
            #print("An error occured: ", type(e).__name__, "\n", e)


    def runPullRowFromCol(self):
        try:
            optionChoice = self.pullingDropdown.get()
            if optionChoice == "Pull Column":
                #for splicing
                userIndex = self.dropdown.get()

                pullFrom = str(self.pullFromThisCol.get("1.0", 'end-1c'))
                dataFromRow = str(self.nameOfPull.get("1.0", 'end-1c'))
                colResult = str(self.colGrabFrom.get("1.0", 'end-1c'))
                self.variableToRun = dataFromRow +" (first 100 results from {" + pullFrom + "})" + ":\n"

                for i in list(self.dataset.loc[self.dataset[pullFrom] == dataFromRow, colResult].values[int(userIndex):int(userIndex) + 100]):
                    self.variableToRun += " - " + str(i) + "\n"
                #self.variableToRun = dataFromRow + ":\n" + str(self.dataset.loc[self.dataset[pullFrom] == dataFromRow, colResult].values[:100])
                self.updateText()
                print(self.variableToRun)
            if optionChoice == "Pull Row":
                pullFromCol = str(self.pullFromThisCol.get("1.0", 'end-1c'))
                dataFromCol = str(self.nameOfPull.get("1.0", 'end-1c'))
                self.variableToRun = ''
                separatorList = []
                for label in self.datasetLabels:
                    output = list(self.dataset.loc[self.dataset[pullFromCol] == dataFromCol, label])
                    separatorList.append(output)
                    
                for i in range(len(separatorList[0])):
                    self.variableToRun += "Row " + str(i) + "\n"
                    for j in range(len(separatorList)):
                        self.variableToRun += str(self.datasetLabels[j]) + ": \n" + str(separatorList[j][i]) + "\n\n"
                    self.updateText()
                    self.variableToRun = ''
                    
        except Exception as e:
            self.variableToRun = ''
            self.variableToRun += "An error occured: " + str(type(e).__name__) + "\n" + str(e)
            self.updateText()
            #print("An error occured: ", type(e).__name__, "\n", e)

    def getMedianOfColFunc(self):
        try:
            colName = str(self.colNameAve.get("1.0", 'end-1c'))
            lenOfCol = len(list(self.dataset[colName]))
            median = list(self.dataset[colName])[lenOfCol//2]
            self.variableToRun = "Median of " + colName + ": " + str(median) + "\nColumn length: " + str(lenOfCol) + " rows."
            self.updateText()
        except Exception as e:
            self.variableToRun = ''
            self.variableToRun += "An error occured: " + str(type(e).__name__) + "\n" + str(e)
            self.updateText()
            #print("An error occured: ", type(e).__name__, "\n", e)

    def getAveOfColFunc(self):
        try:
            #Does this for all rows, not just the first 100 rows
            colName = str(self.colNameAve.get("1.0", 'end-1c'))
            total = 0
            lenOfCol = len(list(self.dataset[colName]))
            datas = self.dataset[colName].dropna()
            values = list(datas.values)
            for i in values:
                total += int(i) 
            self.variableToRun = "Average of " + colName + ": " + str("%.3f" % (total / lenOfCol)) + "\nColumn length: " + str(lenOfCol) + " rows."
            self.updateText()
            print("total", total, "\n")
            print("len of col", lenOfCol, "\n")
        except Exception as e:
            self.variableToRun = ''
            self.variableToRun += "An error occured: " + str(type(e).__name__) + "\n" + str(e)
            self.updateText()
            #print("An error occured: ", type(e).__name__, "\n", e)
    
    def getMaxOfColFunc(self):
        try:
            colNameToGet = str(self.colNameAve.get("1.0", "end-1c"))
            lenOfCol = len(list(self.dataset[colNameToGet]))
            theMax = max(self.dataset[colNameToGet].values)
            self.variableToRun = ''
            self.variableToRun += "Max of " + colNameToGet + ": " + str(theMax) + "\nColumn length: " + str(lenOfCol) + " rows."
            self.updateText()
        except Exception as e:
            self.variableToRun = ''
            self.variableToRun += "An error occured: " + str(type(e).__name__) + "\n" + str(e)
            self.updateText()

    def getMinOfColFunc(self):
        try:
            colNameToGet = str(self.colNameAve.get("1.0", "end-1c"))
            lenOfCol = len(list(self.dataset[colNameToGet]))
            theMin = min(self.dataset[colNameToGet].values)
            self.variableToRun = ''
            self.variableToRun += "Min of " + colNameToGet + ": " + str(theMin) + "\nColumn length: " + str(lenOfCol) + " rows."
            self.updateText()
        except Exception as e:
            self.variableToRun = ''
            self.variableToRun += "An error occured: " + str(type(e).__name__) + "\n" + str(e)
            self.updateText()

    #function for rounding up size to nearest hundreds
    def roundup(self, x):
        return int(math.ceil(x / 100.0)) * 100

    #organize the dropdown options using roundup and the len of the dataset (will run this in init)
    def wrangleDropdownOptions(self):
        roundedNum = self.roundup(self.datasetLength)
        for i in range(0, roundedNum, 100):
            self.dropdownOptions.append(i)





#DRIVER CODE:
if __name__ == "__main__":
    runMain = Main()
