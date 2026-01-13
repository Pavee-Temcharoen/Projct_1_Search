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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # DFS / BFS

    # state       => tuple of position        => (x,y)
    # action      => list of direction        => ['North', 'South', 'East', 'West']
    # visited     => set of state             => {(5,5), (5,6)}
    # step_cost   => cost to walk mostly 1    => 1
    # stack/queue => (stact,action)           => [((5,6), ['North']), ((6,5), ['East'])]
    # succuessors => (stact,action,step_cost) => ((5,6), 'North', 1)

    stack = util.Stack() # create stack

    start_state = problem.getStartState() # start state

    if problem.isGoalState(start_state): # dont walk if goal instantly
        return []

    visited = set() # popped state

    stack.push((start_state, [])) # store (state, list of all action until this state)

    while not stack.isEmpty():
        state, actions = stack.pop()

        if state in visited: # ignore visited state
            continue
        visited.add(state)

        if problem.isGoalState(state): # check goal
            return actions

        # next successor: list of (next_state, action, stepCost)
        for next_state, action, step_cost in problem.getSuccessors(state):
            if next_state not in visited: # push to stack if not visited
                stack.push((next_state, actions + [action]))

    return [] # no answer
    
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue() # create queue

    start_state = problem.getStartState()

    if problem.isGoalState(start_state):
        return []
    
    visited = set()

    queue.push((start_state, []))

    while not queue.isEmpty():
        state, actions = queue.pop()

        if state in visited:
            continue
        visited.add(state)

        if problem.isGoalState(state):
            return actions

        # successor
        for next_state, action, step_cost in problem.getSuccessors(state):
            if next_state not in visited:
                queue.push((next_state, actions + [action]))

    return []
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):

    # UCS (DIJ)

    # state       => tuple of position        => (x,y)
    # actions     => list of direction        => ['North', 'South', 'East', 'West']
    # node        => (stact,action,g)         => [((5,6), ['North'],0), ((6,5), ['East'],1)]

    # step_cost   => cost to walk             => 1
    # g           => cost from start to state =>
    # best_g      => dict-state of best cost  => {'(5,5)':0,'(5,6)':2,'(6,5)':3}
    # prio-queue  => prio=g -node-            => prio1-item = ((6,5), ['East'], 1) / prio2-item = ((5,6), ['North'], 2)
    # succuessors => (state,action,step_cost) => ((5,6), 'North', 1)

    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pq = util.PriorityQueue() # prior-q (pop low)

    start_state = problem.getStartState()

    start_node = (start_state, [], 0) # node (state, actions_so_far, g_cost)

    best_g = {start_state: 0} # best cost { state1:g1,  state2:g2 }

    pq.push(start_node, 0) # start prio-q g = 0

    while not pq.isEmpty():
        state, actions, g = pq.pop()

        if g > best_g.get(state, float('inf')): # check cost -> skip if not best-cost
            continue

        if problem.isGoalState(state): # return if reach goal
            return actions

        # successors: (next_state, action, step_cost)
        for next_state, action, step_cost in problem.getSuccessors(state):
            new_g = g + step_cost
            old_best = best_g.get(next_state, float('inf'))

            # if find better cost in next_state
            if new_g < old_best:
                best_g[next_state] = new_g
                pq.push((next_state, actions + [action], new_g), new_g)

    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):

    # A* (UCS + heuristic)

    # state       => tuple of position                 => (x,y)
    # actions     => list of directions => ['North', 'East', ...]
    # node        => (state, actions, g)               => ((6,5), ['East'], 1)

    # step_cost   => cost of ONE move                  => usually 1
    # g           => total cost from start to state    => sum(step_cost)
    # h           => heuristic estimate (state->goal)  => heuristic(state, problem)
    # f           => priority value                    => f = g + h

    # best_g      => dict: best known g per state      => {(5,5):0, (6,5):1, (5,6):2, ...}
    # (acts like "visited" but cost-aware)

    # priority-q  => stores nodes ordered by f         =>
    #   prio=f - item=(state, actions, g)
    #   e.g.
    #     f=4  item=((6,5), ['East'], 1)    because g=1, h=3
    #     f=6  item=((5,6), ['North'], 2)   because g=2, h=4

    # successors  => list of triples returned by problem:
    #   (next_state, action, step_cost)
    #   e.g. ((5,6), 'North', 1)

    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pq = util.PriorityQueue()
    start_state = problem.getStartState()

    best_g = {start_state: 0}

    start_node = (start_state, [], 0)

    # priority => f = g + h
    start_f = 0 + heuristic(start_state, problem)
    pq.push(start_node, start_f)

    while not pq.isEmpty():
        state, actions, g = pq.pop()

        if g > best_g.get(state, float('inf')): # Skip outdated entries
            continue

        if problem.isGoalState(state):
            return actions

        for next_state, action, step_cost in problem.getSuccessors(state): # Expand
            new_g = g + step_cost

            # consider path if better than any previous one
            if new_g < best_g.get(next_state, float('inf')):
                best_g[next_state] = new_g
                new_actions = actions + [action]
                new_f = new_g + heuristic(next_state, problem)
                pq.push((next_state, new_actions, new_g), new_f)

    return []

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
