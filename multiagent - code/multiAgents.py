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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        minFoodDist = 100000
        minGhostDist = 100000

        for food in newFood.asList():
            minFoodDist = min(minFoodDist, manhattanDistance(newPos, food))

        for ghost in successorGameState.getGhostPositions():
            minGhostDist = min(minGhostDist, manhattanDistance(newPos, ghost))

        if len(newFood.asList()) == 0:
            minFoodDist = 1

        stop_pen = 0
        if action == Directions.STOP and minGhostDist > 5:
            stop_pen = -100

        return successorGameState.getScore() + minGhostDist / minFoodDist + stop_pen


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

            gameState.isWin():
            Returns whether or not the game state is a winning state

            gameState.isLose():
            Returns whether or not the game state is a losing state
            """
            "*** YOUR CODE HERE ***"

            value, action = self.minimaxDecision(gameState, 0, 0)
            return action


    def minimaxDecision(self, gameState, player, depth):

        legalActions = gameState.getLegalActions(player)

        #cutoff-test
        if len(legalActions) == 0 or depth == self.depth:
            return self.evaluationFunction(gameState), None

        if player == 0:
            return self.agentValue(gameState, player, depth)
        else:
            return self.ghostValue(gameState, player, depth)


    def agentValue(self, gameState, player, depth):
        legalActions = gameState.getLegalActions(player)

        max_values = []

        for legalAction in legalActions:
            successor = gameState.generateSuccessor(player, legalAction)

            max_values.append((self.minimaxDecision(successor, player + 1, depth)[0], legalAction))

        return max(max_values)

    def ghostValue(self, gameState, player, depth):
        legalActions = gameState.getLegalActions(player)
        last_ghost = gameState.getNumAgents()
        min_values = []

        for legalAction in legalActions:
            successor = gameState.generateSuccessor(player, legalAction)
            next_player = player + 1

            if next_player == last_ghost:
                next_player = 0
                min_values.append((self.minimaxDecision(successor, next_player, depth + 1)[0], legalAction))
            else:
                min_values.append((self.minimaxDecision(successor, next_player, depth)[0], legalAction))

        return min(min_values)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -1000000
        beta = 1000000
        return self.alphaBetaPrunning(gameState, 0, 0, alpha, beta)[1]

    def alphaBetaPrunning(self, gameState, player, depth, alpha, beta):
        legalActions = gameState.getLegalActions(player)

        if len(legalActions) == 0 or depth == self.depth:
            return self.evaluationFunction(gameState), None

        if player == 0:
            return self.agentValue(gameState, player, depth, alpha, beta)
        else:
            return self.ghostValue(gameState, player, depth, alpha, beta)


    def agentValue(self, game_state, player, depth, alpha, beta):

        legalActions = game_state.getLegalActions(player)
        max_value = -1000000
        max_values = []
        action = None

        for legalAction in legalActions:
            successor = game_state.generateSuccessor(player, legalAction)

            max_values.append((self.alphaBetaPrunning(successor, player + 1, depth, alpha, beta)[0], legalAction))

            max_value, action = max(max_values)
            alpha = max(alpha, max_value)

            if max_value > beta:
                return max_value, action

        return max_value, action


    def ghostValue(self, gameState, player, depth, alpha, beta):
        legalActions = gameState.getLegalActions(player)

        last_ghost = gameState.getNumAgents()
        min_value = 1000000
        min_values = []
        action = None

        for legalAction in legalActions:
            successor = gameState.generateSuccessor(player, legalAction)
            next_player = player + 1

            if next_player == last_ghost:
                next_player = 0
                min_values.append((self.alphaBetaPrunning(successor, next_player, depth + 1, alpha, beta)[0], legalAction))
            else:
                min_values.append((self.alphaBetaPrunning(successor, next_player, depth, alpha, beta)[0], legalAction))

            min_value, action = min(min_values)
            beta = min(beta, min_value)

            if min_value < alpha:
                return min_value, action

        return min_value, action


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


class  RandomAgent(Agent):

    def  getAction(self , gameState):
        legalMoves = gameState.getLegalActions () # Pick  randomly  among  the  legal
        chosenIndex = random.choice(range(0, len(legalMoves)))
        return  legalMoves[chosenIndex]


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
