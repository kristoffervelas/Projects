#implement A*
import tkinter as tk
import os
import math
import numpy as np
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import Label
from tkinter import Entry
from tkinter import filedialog
from tkinter import Canvas
import pandas as pd
import lxml
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#should probably display grid first and do matrix logic last to visualize


class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 #dist between curr node and start node
        self.h = 0 #estimated distance from curr node to end node (pythagorean)
        self.f = 0 #total cost of node

    def __eq__(self, other):
        return self.position == other.position


class Main():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("A*")

        windowX = 1400
        windowY = 1000

        self.obstaclePts = [] #list of obstacle coords

        self.window.geometry("%sx%s" % (str(windowX), str(windowY)))
        self.window.resizable(False, False)
        self.createMatrix()
        self.displayGrid()
        self.displayOptions()


        self.window.mainloop()

    def astar(self,maze,start,end):
        #returns the path as tuples

        #create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        open_list = []
        closed_list = []

        open_list.append(start_node)

        #loop until find end
        while len(open_list) > 0:

            #get current node (the one w the lowest f)
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path


            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

    def createMatrix(self):
        self.mainMatrix = [[0 for i in range(30)] for i in range(20)]
        self.matrixLenY = len(self.mainMatrix)
        self.matrixLenX = len(self.mainMatrix[0])

        #print(self.mainMatrix)
        #print(self.matrixLenX)
        #print(self.matrixLenY)

    def displayOptions(self):

        self.optionsFrame = tk.Frame(self.window, height=100, width=1200)
        self.optionsFrame.grid(row=1, column=0)

        self.findPathButton = tk.Button(self.optionsFrame, command=self.updateGrid, text="A Star", height=1, width=20)
        self.findPathButton.grid(row=0, column=1, padx=20, pady=20)

        self.clearMatrixButton = tk.Button(self.optionsFrame, command=self.clearMatrix, text="Clear Matrix", height=1, width=20)
        self.clearMatrixButton.grid(row=0, column=2, padx=20, pady=20)

        self.obstacleDropdown = ttk.Combobox(self.optionsFrame, state='readonly', values=["Ready", "Place Obstacles"])
        self.obstacleDropdown.current(0)
        self.obstacleDropdown.grid(row=0, column=0, padx=20, pady=20)    

        self.startPull = tk.Text(self.optionsFrame, bd=2, height=1, width=20)
        self.startPull.config(state=tk.NORMAL)
        self.startPull.grid(row=0, column=3, padx=20, pady=20)

        self.endPull = tk.Text(self.optionsFrame, bd=2, height=1, width=20)
        self.endPull.config(state=tk.NORMAL)
        self.endPull.grid(row=0, column=4, padx=20, pady=20)

    def clearMatrix(self):
        self.obstaclePts = []
        self.mainMatrix = [[0 for i in range(30)] for i in range(20)]
        self.cells = {}
        self.cellX = 40
        self.cellY = 40
        for row in range(20):
            for col in range(30):
                x1=col*self.cellX
                y1=row*self.cellY 
                x2=x1+self.cellX
                y2=y1+self.cellY

                self.cells[row, col] = self.gridFrame.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
        #for a button

    def clearGrid(self):
        for i in range(20):
            for j in range(30):
                if self.mainMatrix[i][j] != 2:
                    self.mainMatrix[i][j] = 0

        self.cells = {}
        self.cellX = 40
        self.cellY = 40
        for row in range(20):
            for col in range(30):
                x1=col*self.cellX
                y1=row*self.cellY 
                x2=x1+self.cellX
                y2=y1+self.cellY

                self.cells[row, col] = self.gridFrame.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')

        for row, col in self.obstaclePts:
            self.gridFrame.itemconfig(self.cells[row, col], fill='brown')


    def displayGrid(self):
        self.gridFrame = tk.Canvas(self.window, width=1200, height=800, bg='white')
        self.gridFrame.grid(row=0, column=0, pady=50, padx=100)
        #40x40 for each cell
        #self.dict for colors, can change them using function that manipulates the dict
        #dict before creating buttons to initialize colors first
        self.gridColors = {}
        for row in range(len(self.mainMatrix)):
            for col in range(len(self.mainMatrix[row])):
                self.gridColors[row, col] = "white"
                #all initialize to white
        #print(self.gridColors)

        #
        self.clearGrid()
        
        self.gridFrame.bind('<Button-1>', self.gridClick)

        #use dictionary to connect each cell into its matrix index
        #be able to hide numbers (be u friendly)
        #can add obstacles and change user pos
        #can change target direction, if new pos alrdy visited, recalculate path, else start path again from last state?

    def gridClick(self, event):
        #for obstacles
        #bind to canvas when done
        #canvas is 1200x800 (WxH)
        #cells are 30x20 (WxH)
        #each cell is 40x40 dimensions

        widths = []
        heights = []

        for i in range(0, 1240, 40):
            widths.append(i)

        for i in range(0, 840, 40):
            heights.append(i)

        chosenX = -10
        chosenY = -10

        for ind, width in enumerate(widths):
            if event.x > width - 40 and event.x < width:
                chosenX = ind-1

        for ind, height in enumerate(heights):
            if event.y > height - 40 and event.y < height:
                chosenY = ind-1

        self.gridFrame.itemconfig(self.cells[chosenY, chosenX], fill='brown')

        self.obstaclePts.append([chosenY, chosenX])

        self.mainMatrix[chosenY][chosenX] = 2

        #get the coordinates in terms of the cell numbers
        #change matrix values accordingly
        #print(event.x, event.y)

    def updateGrid(self):
        #this is where you update graph with matrix state
        #only play with the matrix
        self.clearGrid()
        self.optimal_path=[]

        if self.startPull.get("1.0", "end-1c") == "":
            start = (1, 4)
        else:
            start = self.startPull.get("1.0", "end-1c").split(",")
            start = (int(start[0]), int(start[1]))

        if self.endPull.get("1.0", "end-1c") == "":
            end = (15, 15)
        else:
            end = self.endPull.get("1.0", "end-1c").split(",")
            end = (int(end[0]), int(end[1]))

        self.optimal_path = self.astar(self.mainMatrix, start, end)

        #set color of optimal path (red)
        for row, col in self.optimal_path:
            self.gridFrame.itemconfig(self.cells[row, col], fill='red')

        #set start green
        self.gridFrame.itemconfig(self.cells[int(start[0]), int(start[1])], fill='green')
        #set end blue
        self.gridFrame.itemconfig(self.cells[int(end[0]), int(end[1])], fill='blue')



        
            
        



if __name__ == '__main__':
    runMain = Main()

#AFTER STEP BASED, IMPLEMENT COST BASED WHERE SOME STEPS COST MORE THAN OTHERS

