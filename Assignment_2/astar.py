from enum import Enum
from os import system
from sys import argv
import numpy as np
from math import sqrt
import time


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Intalize the Matrix!
board_matrix = []

cost = False
dijkstra = False
bfs = False
showChecked = False
showHelp = False
showBoard = False

if "--help" in argv or "-h" in argv or len(argv) <= 1:
    print(bcolors.OKBLUE + "TDT4136 AI Assignment 2 © by Petter Rein & Balázs Orbán @ NTNU - 2018" + bcolors.ENDC)
    print("""
Available flags are:
    --help, -h - Show help (Hint: you are here 😉 )
    --source, -s - Specify the source file for the input
    --show-checked, -C - Show the checked blocks
    --show-board, -B - show the original board
    --mode, -m - Specify the algorithm to run. Possible values are:
        Default: If mode is omitted, A* without cost is run.
        bfs - Run Best-First Search
        dijkstra - Run Dijkstra's algorithm
        cost - Run A* with cost

Block types:
    representation - name - cost to pass
    🏁  - goal - Ø
    🚩  - start - Ø
    👠  - found path - Ø
    🛤  - road - 1
    🌱  - grassland - 5 
    🌳  - forest - 10
    ⛰  - mountain - 50
    🌊  - water - 100
    ❔  - checked - Ø
    🚧  - obstacle - not passable

    Ø - There is no point in measuring the cost to pass
    """)
    showHelp = True

if not showHelp:

    # Add source file with -s or --source flags and transform it into a 2D array
    if  "--source" in argv or "-s" in argv:
        file = open(argv[2])
        for line in file:
            row = []
            for x in line:

                if x != "\n":
                    row.append(x)
            board_matrix.append(row)
        file.close()
    else:
        print(bcolors.FAIL+"Please define the source file with the --source or -s flag"+bcolors.ENDC)

    if "--show-board" in argv or "-B" in argv:
        showBoard = True
    if "--mode" in argv or "-m" in argv:
        if "cost" in argv:
            cost = True
            print("Running A* with cost")
        if "bfs" in argv:
            bfs = True
            print("Running Best-First Search")
        elif "dijkstra" in argv:
            print("Running Dijkstra's alogirthm")
            dijkstra = True
    else:
        print("""
Running A* without cost
To try different modes, use the --mode or -m flags.:
    bfs - Run Best-First Search
    dijkstra - Run Dijkstra's algorithm
    cost - Run A* with cost
""")

    if "--show-checked" in argv or "-C" in argv:
        print("showing checked blocks")
        showChecked = True


# Petter make the matrix with the red pill, Balazs want it with the blue so we flip it. First column board[x] is horizontal and board[1][x] is not vertical now.
board_matrix = np.transpose(board_matrix)

# Defined Type and their weights
class Type(Enum):
    water = 100
    mountain = 50
    forest = 10
    grassland = 5
    road = 1
    obstacle = -1
    start = -2
    goal = -3
    error = -10


# Node class containing the coordinates, its type,
# if the Node was visited, or if it is part of the final path.
# Also fScore, gScore, hScore
class Node:
    def __init__(self, x, y, Type):
        self.x = x
        self.y = y
        self.neighbors = {}
        # 2**10000 represents Infinity
        self.f = 2**10000
        self.g = 2**10000
        self.h = 2**10000
        self.type = Type
        self.prev = None
        self.isPath = False
        self.isChecked = False

    # Make it so that you can print a node
    def __str__(self):
        return printBlock(str(self.type.value))

    # Make it so that you can compare two nodes
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# Maps every character from txt to their Type
def findType(element):
    if element == "w":
        return Type.water
    elif element == "r" or element == ".":
        return Type.road
    elif element == "m":
        return Type.mountain
    elif element == "f":
        return Type.forest
    elif element == "g":
        return Type.grassland
    elif element == "#":
        return Type.obstacle
    elif element == "A":
        return Type.start
    elif element == "B":
        return Type.goal
    else:
        return Type.error

start, goal = {"x": 0, "y":0}, {"x": 0, "y":0}

# Reads everyting in the first Matrix, and convert it into nodes for easy calls
def createBoard(board_matrix):
    x = -1
    y = -1
    node_matrix = []
    for lines in board_matrix:
        x = x + 1
        row = []
        for element in lines:
            y = y + 1
            if element == "A":
                start["x"] = x
                start["y"] = y
            if element == "B":
                goal["x"] = x
                goal["y"] = y
            node = Node(x,y, findType(element))
            row.append(node)
        y = -1
        node_matrix.append(row)

    for lines in node_matrix:
        for node in lines:
            node.neighbors = {}
            if 1 <= node.y:
                node.neighbors["north"] = node_matrix[node.x][node.y-1]
            if len(node_matrix[node.x]) > node.y+1:
                node.neighbors["south"] = node_matrix[node.x][node.y+1]
            if 1 <= node.x:
                node.neighbors["west"] = node_matrix[node.x-1][node.y]
            if len(node_matrix) > node.x+1:
                node.neighbors["east"] = node_matrix[node.x+1][node.y]

    return node_matrix

# Prettify block
def printBlock(emoji):
    print("{:<4}".format(emoji), end="")


# Custom print for the board so we can make pretty rapport + emojies
def printBoard(board):
    printBlock("")
    for x in range(0, len(board)):
        printBlock(x)
    print("\n")
    y = 0
    for line in np.transpose(board):
        printBlock(str(y))
        for node in line:
            if node.isPath:
                printBlock("👠")
            elif node.isChecked:
                printBlock("❔")
            elif node.type.name == "goal":
                printBlock("🏁")
            elif node.type.name == "start":
                printBlock("🚩")
            elif node.type.name == "obstacle":
                printBlock("🚧")
            elif node.type.name == "water":
                printBlock("🌊")
            elif node.type.name == "mountain":
                printBlock("⛰")
            elif node.type.name == "forest":
                printBlock("🌳")
            elif node.type.name == "grassland":
                printBlock("🌱")
            elif node.type.name == "road":
                printBlock("🛤")
            elif node.type.name == "free":
                printBlock("o")
            else:
                printBlock(node)
        print("")
        y+=1
    return ""

# Saves the node_Matrix_Board as a global function
board = createBoard(board_matrix)


# Heurisitc calulator Manhattan
def heuristic(a, b):
    x_diff = abs(a.x - b.x)
    y_diff = abs(a.y - b.y)
    return x_diff + y_diff



if not showHelp:
    # Saves the start_node as a global node
    start_node = board[start["x"]][start["y"]]


    # Saves the goal_node as a global node
    goal_node = board[goal["x"]][goal["y"]]

# A* per se
def A_star(start_node, goal_node):



    # Must intialize the first heuristics between the start and end node
    start_node.f = heuristic(start_node, goal_node)

    # Start with the start node in the openSet
    openSet = [start_node]
    # Intialize the closeSet
    closeSet = []

    # Run as long we have something in the openSet to check
    while len(openSet) is not 0:

        # Sorts the openSet so we always have the node with lowest fscore first so pop works
        if cost:
            openSet.sort(key=lambda node : node.f, reverse=True)
            current = openSet.pop()
        elif dijkstra:
            openSet.sort(key=lambda node : node.g, reverse=True)
            current = openSet.pop()
        elif bfs:
            current = openSet.pop()
        else:
            openSet.sort(key=lambda node : node.f, reverse=True)
            current = openSet.pop()
        closeSet.append(current)

        # The A* algorithm reached the 🏁
        if current == goal_node:
            path = "end"
            node = goal_node.prev
            # use --checked or -c flag

            if showChecked:
                for node in closeSet:
                    node.isChecked = True

            pathCost = 0
            while node.prev is not None:
                node.isPath = True
                pathCost += node.type.value
                node = node.prev

            print("\n" + bcolors.OKGREEN + "DONE!"+ bcolors.ENDC + " Cost was: "+ str(pathCost) + " and the path is:")
            return  printBoard(board)


        # Find every friendly neighbor for this node
        for neighbor in current.neighbors:
            neighbor = current.neighbors[neighbor]

            # If we care about node cost or not
            if cost or dijkstra:
                tempG = current.g + neighbor.type.value
            else:
                tempG = current.g
                neighbor.f = neighbor.g

            # If the neighbor is already considered don't do it again
            if neighbor in closeSet:
                continue

            # If not, do it and only if this is not a wall!
            if neighbor not in openSet and neighbor.type.value != -1:
                if bfs:
                    openSet.insert(0, neighbor)
                else:
                    openSet.append(neighbor)
            # If the old g is better dont change now!
            elif tempG >= neighbor.g:
                continue
            # Save the path we go so we can go back sometime
            neighbor.prev = current
            # Update heurisitc, not needed to save it, but nice to have
            neighbor.h = heuristic(neighbor, goal_node)
            # Save the temp gScore as the new
            neighbor.g = tempG
            # Calculate the fScore and save it.
            if cost:
                neighbor.f = current.g + neighbor.h + neighbor.type.value
            else:
                neighbor.f = current.g + neighbor.h

    # The A* algorithm did not find a solution from 🚩 to 🏁
    else:
        for node in closeSet:
            node.isChecked = True
        print("No solution on this board! '❔' means the area was checked")
        return printBoard(board)


#A_star(start_node, goal_node)

if showBoard:
    printBoard(board)

if not showHelp:
    start_time = time.time()
    A_star(start_node, goal_node)
    print("It took %s seconds" % (time.time() - start_time))
