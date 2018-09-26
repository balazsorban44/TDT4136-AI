from enum import Enum
from os import system
from sys import argv
import numpy as np
from math import sqrt


def heuristic(a, b):
    x_diff = abs(a.x - b.x)
    y_diff = abs(a.y - b.y)
    return x_diff + y_diff

def dist(a, b):
    return sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

start, goal = {"x": 0, "y":0}, {"x": 0, "y":0}

board_matrix = []
if argv[1] == "--source" or argv[1] == "-s":
    file = open(argv[2])
    for line in file:
        row = []
        for x in line:
            
            if x != "\n":
                row.append(x)
        board_matrix.append(row)
    file.close()
else:
    print("Please define the source file with the --source or -s flag")

board_matrix = np.transpose(board_matrix)

class Type(Enum):
    water = 100
    mountain = 50
    forest = 10
    grassland = 5
    road = 1
    obstacle = -1
    free = 0
    start = -2
    goal = -3
    error = -10


class Node:
    def __init__(self, x, y, Type):
        self.x = x
        self.y = y
        self.neighbors = {
            "north": None,
            "south": None,
            "west": None,
            "east": None
        }
        self.f = 99999
        self.g = 99999
        self.h = 99999
        self.Type = Type
        self.prev = None
        self.isPath = False

    def __str__(self):
        return "{:<4}".format(str(self.Type.value))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def findType(element):
    if element == ".":
        return Type.free
    elif element == "w":
        return Type.water
    elif element == "r":
        return Type.road
    elif element == "m":
        return Type.mountain
    elif element == "forest":
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
            if 1 < node.y:
                node.neighbors["north"] = node_matrix[node.x][node.y-1]
            if len(node_matrix[node.x]) > node.y+1:
                node.neighbors["south"] = node_matrix[node.x][node.y+1]
            if 1 < node.x:
                node.neighbors["west"] = node_matrix[node.x-1][node.y]
            if len(node_matrix) > node.x+1:
                node.neighbors["east"] = node_matrix[node.x+1][node.y]

    return node_matrix




def printBoard(board):
    for x in range(0, len(board)):
        print("{:<4}".format(x), end="")
    print("\n")
    for line in np.transpose(board):
        for node in line:
            if node.isPath:
                print("{:<4}".format("🛣"), end="")
            elif node.Type.value == -2:
                print("{:<4}".format("🚩"), end="")
            elif node.Type.value == -3:
                print("{:<4}".format("🏁"), end="")
            elif node.Type.value == -1:
                print("{:<4}".format("🚧"), end="")
            elif node.Type.value == 0:
                print("{:<4}".format("o"), end="")
            else:
                print(node, end="")
        print("")
    return ""

board = createBoard(board_matrix)

start_node = board[start["x"]][start["y"]]
goal_node = board[goal["x"]][goal["y"]]
start_node.f = heuristic(start_node, goal_node)



def A_star(start_node, goal_node):
    openSet = [start_node]
    closeSet = []
    while len(openSet) is not 0:
        openSet.sort(key=lambda node : node.f, reverse=True)
        current = openSet.pop()
        closeSet.append(current)

        # Done!
        if current == goal_node:
            path = "end"
            node = goal_node.prev
            while node.prev is not None:
                node.isPath=True
                node = node.prev

            return "DONE!" + "\n" + printBoard(board)
            
        
        for neighbor in current.neighbors:
            neighbor = current.neighbors[neighbor]
            tempG = current.g + dist(current, neighbor)
            if neighbor in closeSet:
                continue
            if neighbor not in openSet and neighbor.Type.value != -1:
                openSet.append(neighbor)
            elif tempG >= neighbor.g:
                continue
                
            neighbor.prev = current
            neighbor.h = heuristic(neighbor, goal_node)
            neighbor.g = tempG
            neighbor.f = neighbor.g + neighbor.h
    return printBoard(board)

print(A_star(start_node, goal_node))