#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import itertools
from sys import argv


error = False
difficulty = ""
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(bcolors.UNDERLINE + "\nTDT4136 AI Assignment 4 © by Petter Rein & Balázs Orbán @ NTNU - 2018" + bcolors.ENDC+"\n")

if "--difficulty" not in argv and "-d" not in argv:
    print(bcolors.FAIL + "Please define the difficulty by --difficulty {value} or -d {value} flags.\npossible values: easy, medium, hard, veryhard" + bcolors.ENDC)
    error = True
else:
    if "-d" in argv:
        difficulty = argv[argv.index("-d")+1]
    else:
        difficulty = argv[argv.index("--difficulty")+1]

class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        self.calls = 0
        self.failures = 0

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [ (i, j) for i in self.constraints for j in self.constraints[i] ]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [ (i, var) for i in self.constraints[var] ]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """

        self.calls += 1
        complete = True
        for key in assignment.keys():
            if len(assignment[key]) != 1:
                complete = False
        if complete:
            return assignment

        unassigned = self.select_unassigned_variable(assignment)
        for value in assignment[unassigned]:
            assignment_copy = copy.deepcopy(assignment)
            assignment_copy[unassigned] = [value]
            queue = self.get_all_neighboring_arcs(unassigned)
            if self.inference(assignment_copy, queue):
                result = self.backtrack(assignment_copy)
                if result:
                    return result
        self.failures += 1
        return False

    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """
        for var in assignment.keys():
            if len(assignment[var]) > 1:
               return var

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        while(queue):
            i, j = queue.pop(0)
            if self.revise(assignment, i, j):
                if not assignment[i]:
                    return False
                for neighbor in self.get_all_neighboring_arcs(i):
                    if j not in neighbor[0]:
                        queue.append((neighbor[0], i))
        return True
        
    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
        revised = False
        for x in assignment[i]:
            satisfied = False
            for y in assignment[j]:
                if (x, y) in self.constraints[i][j]:
                    satisfied = True
                    break
            if not satisfied:
                assignment[i].remove(x)
                revised = True
        return revised


def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = [ 'WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T' ]
    edges = { 'SA': [ 'WA', 'NT', 'Q', 'NSW', 'V' ], 'NT': [ 'WA', 'Q' ], 'NSW': [ 'Q', 'V' ] }
    colors = [ 'red', 'green', 'blue' ]
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp

def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    board = map(lambda x: x.strip(), open(filename, 'r'))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), map(str, range(1, 10)))
            else:
                csp.add_variable('%d-%d' % (row, col), [ board[row][col] ])

    for row in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for col in range(9) ])
    for col in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for row in range(9) ])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp

def print_sudoku_solution(csp):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    solution = csp.backtracking_search()
    for row in range(9):
        for col in range(9):
            print print_emoji(solution['%d-%d' % (row, col)][0]),
            if col == 2 or col == 5:
                print('|'),
        print
        if row == 2 or row == 5:
            print '------+-------+------'

    print(bcolors.OKBLUE+"The number of times the backtrack function was called: " + str(csp.calls) + bcolors.ENDC)
    print(bcolors.FAIL+"The number of times the backtrack function failed: " + str(csp.failures)+bcolors.ENDC)

def print_emoji(digit):
    if digit == "1":
        return "1️⃣"
    if digit == "2":
        return "2⃣"
    if digit == "3":
        return "3⃣"
    if digit == "4":
        return "4⃣"
    if digit == "5":
        return "5⃣"
    if digit == "6":
        return "6️⃣"
    if digit == "7":
        return "7️⃣"
    if digit == "8":
        return "8️⃣"
    if digit == "9":
        return "9️⃣"
    else:
        return digit
    


if not error:
    csp = create_sudoku_csp("./" + difficulty + ".txt")
    print_sudoku_solution(csp)