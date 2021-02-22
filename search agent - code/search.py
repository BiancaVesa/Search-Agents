# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import random


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


class Node:

    def __init__(self, state, action, parent, path_cost=0):
        self.state = state
        self.action = action
        self.parent = parent
        self.path_cost = path_cost


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    """

    "*** YOUR CODE HERE ***"

    adj = util.Stack()
    explored = []
    solution = []

    start_node = Node(problem.getStartState(), None, None, 0)

    adj.push(start_node)

    while not adj.isEmpty():
        current_node = adj.pop()

        if current_node.state in explored: continue

        if problem.isGoalState(current_node.state):
            path_node = current_node

            while path_node.state != start_node.state:
                solution.append(path_node.action)
                path_node = path_node.parent

            solution.reverse()
            return solution

        explored.append(current_node.state)
        successors = problem.getSuccessors(current_node.state)

        for successor in successors:
            if (not explored.__contains__(successor[0])) and (not adj.list.__contains__(successor)):
                new_node = Node(successor[0], successor[1], current_node, current_node.path_cost + successor[2])
                adj.push(new_node)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    adj = util.Queue()
    explored = []
    solution = []

    start_node = Node(problem.getStartState(), None, None, 0)

    adj.push(start_node)

    while not adj.isEmpty():
        current_node = adj.pop()

        if current_node.state in explored: continue

        if problem.isGoalState(current_node.state):
            path_node = current_node

            while path_node.state != start_node.state:
                solution.append(path_node.action)
                path_node = path_node.parent

            solution.reverse()
            return solution

        explored.append(current_node.state)
        successors = problem.getSuccessors(current_node.state)

        for successor in successors:
            if (not explored.__contains__(successor[0])) and (not adj.list.__contains__(successor)):
                new_node = Node(successor[0], successor[1], current_node, current_node.path_cost + successor[2])
                adj.push(new_node)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    adj = util.PriorityQueue()
    explored = []
    solution = []

    start_node = Node(problem.getStartState(), None, None, 0)

    adj.push(start_node, start_node.path_cost)

    while not adj.isEmpty():
        current_node = adj.pop()

        if current_node.state in explored: continue

        if problem.isGoalState(current_node.state):
            path_node = current_node

            while path_node.state != start_node.state:
                solution.append(path_node.action)
                path_node = path_node.parent

            solution.reverse()
            return solution

        explored.append(current_node.state)
        successors = problem.getSuccessors(current_node.state)

        for successor in successors:
            if (not explored.__contains__(successor[0])) and (not adj.heap.__contains__(successor)):
                new_node = Node(successor[0], successor[1], current_node, current_node.path_cost + successor[2])
                adj.push(new_node, new_node.path_cost)



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    adj = util.PriorityQueue()
    explored = []
    solution = []

    start_node = Node(problem.getStartState(), None, None, 0)

    adj.push(start_node, start_node.path_cost + heuristic(start_node.state, problem))

    while not adj.isEmpty():
        current_node = adj.pop()

        if current_node.state in explored: continue

        if problem.isGoalState(current_node.state):
            path_node = current_node

            while path_node.state != start_node.state:
                solution.append(path_node.action)
                path_node = path_node.parent

            solution.reverse()
            return solution

        explored.append(current_node.state)
        successors = problem.getSuccessors(current_node.state)

        for successor in successors:
            if (not explored.__contains__(successor[0])) and (not adj.heap.__contains__(successor)):
                new_node = Node(successor[0], successor[1], current_node, current_node.path_cost + successor[2])
                adj.update(new_node, new_node.path_cost + heuristic(new_node.state, problem))


def randomSearch(problem):

    current_state = problem.getStartState()

    actions = []

    while problem.isGoalState(current_state) == False:
        successors = problem.getSuccessors(current_state)
        successor = random.choice(successors)
        current_state = successor[0]
        actions.append(successor[1])

    return actions


    # Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
rs = randomSearch
