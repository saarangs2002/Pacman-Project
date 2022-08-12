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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    cur_state = problem.getStartState() 
    visitLog = {cur_state:[0]}              
    """
    visitLog[state] == [0] {when unvisited but in frontier list}
    visitLog[state] == [1,direction,predecessor] {when visited} 
    """ 
    actionList=[]                           #finally stores the list of action to reach goal from starting position   
    DFStack = util.Stack()
    DFStack.push([cur_state,-1,-1])         #[state,direction,predecessor]

    while (DFStack.isEmpty()==0):
        cur_stateData = DFStack.pop()
        cur_state = cur_stateData[0]
        if (visitLog[cur_state][0]==0):
            visitLog[cur_state]=[1,cur_stateData[1],cur_stateData[2]]
            if(problem.isGoalState(cur_state)==1):
                break
            for x in problem.getSuccessors(cur_state):
                if (x[0] not in visitLog):
                    visitLog[x[0]] = [0]
                    DFStack.push([x[0],x[1],cur_state])
                elif((visitLog[x[0]][0]==0) ):
                    visitLog[x[0]] = [0]
                    DFStack.push([x[0],x[1],cur_state])
    
    while (problem.getStartState() != cur_state):
        actionList.insert(0,visitLog[cur_state][1])
        cur_state = visitLog[cur_state][2]

    return(actionList)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    cur_state = problem.getStartState()    
    visitLog = {cur_state:[0,0,0]}          #the log that keep status of expanded nodes [visit_status,direction,predecessor]
    actionList=[]                           #stores the list of action to reach goal from starting position    
    BFSQueue = util.Queue()
    BFSQueue.push(cur_state)

    while (BFSQueue.isEmpty()==0):
        cur_state = BFSQueue.pop()
        if (visitLog[cur_state][0]==0):
            visitLog[cur_state][0]=1
            if(problem.isGoalState(cur_state)==1):
                break
        for x in problem.getSuccessors(cur_state):
            if (x[0] not in visitLog):
                visitLog[x[0]] = [0,x[1],cur_state]
                BFSQueue.push(x[0])
                if(problem.isGoalState(x[0])==1):
                    break       

    while (problem.getStartState() != cur_state):
        actionList.insert(0,visitLog[cur_state][1])
        cur_state = visitLog[cur_state][2]
    return(actionList)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    cur_state = problem.getStartState()     
    visitLog = {cur_state:[0]}             
    """
    visitLog[state] == [0] {when unvisited but in frontier list}
    visitLog[state] == [1,direction,predecessor] {when visited} 
    """ 
    actionList=[]                           #stores the list of action to reach goal from starting position   
    PQueue = util.PriorityQueue()
    PQueue.push([cur_state,-1,-1,0],0)      #[state,direction,predecessor,g(n)],g(n)

    while (PQueue.isEmpty()==0):
        cur_stateData = PQueue.pop()
        print (cur_stateData)
        cur_state = cur_stateData[0]
        if (visitLog[cur_state][0]==0):
            visitLog[cur_state]=[1,cur_stateData[1],cur_stateData[2]]
            if(problem.isGoalState(cur_state)==1):
                break
            for x in problem.getSuccessors(cur_state):
                if (x[0] not in visitLog):
                    visitLog[x[0]] = [0]
                    gn = x[2]+cur_stateData[3]
                    PQueue.push([x[0],x[1],cur_state,gn],gn)
                elif((visitLog[x[0]][0]==0) ):
                    visitLog[x[0]] = [0]
                    gn = x[2]+cur_stateData[3]
                    PQueue.push([x[0],x[1],cur_state,gn],gn)
    
    while (problem.getStartState() != cur_state):
        actionList.insert(0,visitLog[cur_state][1])
        cur_state = visitLog[cur_state][2]

    return(actionList)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    cur_state = problem.getStartState()     
    visitLog = {cur_state:[0]} 
    """
    visitLog[state] == [0] {when unvisited but in frontier list}
    visitLog[state] == [1,direction,predecessor] {when visited} 
    """ 
    actionList=[]                           #the list that has action to reach there from predecessor node    
    PQueue = util.PriorityQueue()
    PQueue.push([cur_state,-1,-1,0],0)      #[state,direction,predecessor,g(n)],g(n)

    while (PQueue.isEmpty()==0):
        cur_stateData = PQueue.pop()
        cur_state = cur_stateData[0]
        if (visitLog[cur_state][0]==0):
            visitLog[cur_state]=[1,cur_stateData[1],cur_stateData[2]]
            if(problem.isGoalState(cur_state)==1):
                break
            for x in problem.getSuccessors(cur_state):
                if (x[0] not in visitLog):
                    visitLog[x[0]] = [0]
                    gn = x[2]+cur_stateData[3]
                    PQueue.push([x[0],x[1],cur_state,gn],gn+heuristic(x[0],problem))
                elif((visitLog[x[0]][0]==0) ):
                    visitLog[x[0]] = [0]
                    gn = x[2]+cur_stateData[3]
                    PQueue.push([x[0],x[1],cur_state,gn],gn+heuristic(x[0],problem))
    
    while (problem.getStartState() != cur_state):
        actionList.insert(0,visitLog[cur_state][1])
        cur_state = visitLog[cur_state][2]

    return(actionList)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
