# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


# define pacman        
PACMAN = 0
class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        # Get pacman's legal moves of the current state 
        moves = gameState.getLegalActions(PACMAN)
        # Calculates all the possible next states for the possible moves
        next_states = [gameState.generateSuccessor(PACMAN, move) for move in moves]
        # Calculates the scores for every next state so we can choose the best
        scores = [self.min(0, next_state, 1) for next_state in next_states]
        # Find the index of the best score and find its corresponding move        
        return moves[(scores.index(max(scores)))]
    
    def min(self, depth, state, ghost):
      # Base check
      if self.depth == depth or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      # Get all the legal moves that the ghost can do
      moves = state.getLegalActions(ghost)
      # Calculates all the possible next states 
      # for the possible moves
      next_states = [state.generateSuccessor(ghost, move) for move in moves]
      
      # If we still have some ghost to calculate moves and scores
      # for do it otherwise switch to Pacman
      if ghost >= state.getNumAgents() - 1:
    	  scores = [self.max(depth + 1, next_state) for next_state in next_states]
      else:
    		scores = [self.min(depth, next_state, ghost + 1) for next_state in next_states]

      # Return the lowest score. Observe! This 'min' is not a
      # recursive call, but simply choosing the lowest
      # possible number from scores.
      return min(scores)      

    def max(self, depth, state):
      # Base check
      if self.depth == depth or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
        
      # Get all the legal moves that Pacman can do
      moves = state.getLegalActions(PACMAN)
      # Calculates all the possible next states 
      # for the possible moves
      next_states = [state.generateSuccessor(PACMAN, move) for move in moves]
      # Calculates the scores for every next state so we can choose the best
      scores = [self.min(depth, next_state, 1) for next_state in next_states]

      # Return the highest score. Observe! This 'max' is not a
      # recursive call, but simply choosing the highest
      # possible number from scores.
      return max(scores)
      

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
      """
        Returns the minimax action using self.depth and self.evaluationFunction
      """

      # The main difference between this and the Minimax agent is that
      # we don't generate all the next states, only those that actually
      # have a chance to return a better score. The rest of the states
      # are 'pruned'.

      # Get pacman's legal moves of the current state
      moves = gameState.getLegalActions(PACMAN)

      # initialize values
      alpha = float("-inf")
      beta = float("inf")
      current_score = float("-inf")
      current_move = moves[0]

      # For every move check if the score is better than the previous best
      for move in moves:
        next_state = gameState.generateSuccessor(PACMAN, move)
        next_score = self.min(0, next_state, alpha, beta, 1)
        # If better update
        if next_score > current_score:
          current_score = next_score
          current_move = move
        # If score better than beta return the move
        if next_score > beta:
          return current_move
        # Update alpha
        alpha = max(next_score, alpha)
          
      return current_move


    def max(self, depth, state, alpha, beta):
      # Base check
      if self.depth == depth or state.isWin() or state.isLose():
        return self.evaluationFunction(state)

      # Get legal moves
      moves = state.getLegalActions(PACMAN)
      # initialize value
      value = float("-inf")
      
      # For every move check if the score is better than the previous best
      for move in moves:
        next_state = state.generateSuccessor(PACMAN, move)
        value = max(value, self.min(depth, next_state, alpha, beta, 1))
        if value > beta:
          return value

        # Update alpha
        alpha = max(value, alpha)


      return value


    def min(self, depth, state, alpha, beta, ghost):
      # Base check
      if self.depth == depth or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      # Get legal moves
      moves = state.getLegalActions(ghost)
      # initialize value
      value = float("inf")

      # For every move check if the score is better than the previous best
      for move in moves:
        next_state = state.generateSuccessor(ghost, move)
        # For every move check if the score is better than the previous best
        # for all ghosts. If you are done with the ghosts, change to Pacman
        if ghost >= state.getNumAgents() - 1:
          value = min(value, self.max(depth + 1, next_state, alpha, beta))
        else:
          value = min(value, self.min(depth, next_state, alpha, beta, ghost + 1))
    
        if value < alpha:
          return value
        # Update beta
        beta = min(beta, value)

      return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

