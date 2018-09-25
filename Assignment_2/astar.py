from enum import Enum
from sys import argv
import numpy as np


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
        self.Type = Type
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
            
            node.neighbors = {
                "north": node_matrix[node.x][node.y-1] if 1 < node.y else None,
                "south": node_matrix[node.x][node.y+1] if len(node_matrix[node.x]) > node.y+1 else None,
                "west":  node_matrix[node.x-1][node.y] if 1 < node.x else None,
                "east": node_matrix[node.x+1][node.y] if len(node_matrix) > node.x+1 else None
            }

    return node_matrix




def printBoard(board):
    for line in np.transpose(board):
        for node in line:
            print(node, end="")
        print("")
    return ""

board = createBoard(board_matrix)

start_node = board[start["x"]][start["y"]]
goal_node = board[goal["x"]][goal["y"]]


def A_star(start_node, goal_node, board):
    openSet = [start_node]
    closeSet = []
    while len(openSet) is not 0:
        current = openSet.pop()
        if current == goal_node:
            return "DONE!" # return path


A_star(start_node, goal_node, board)