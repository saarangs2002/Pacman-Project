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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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
        #print(legalMoves[chosenIndex])
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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

        """
        -> score stores a very low value(-100) when there is ghost near(<=2 blocks) the agent
        -> also score will give some low(-25) value when the action is 'Stop', 
            we don't want the agent to wait till the ghost near to move to a nearby location
        -> We are trying not to die at any cost
        -> This still won't prevent the agent from dying in some cases, but mostly the agent will survive

        -> foodMinDis stores the lowest manhattan distance to any food (when there is atlest 1 food)
        -> foodMinDis will store value 1 if there is no food remianing
        -> we want to reduce foodMinDis, so we add reciprocal of foodMinDis to the return value
            foodMinDis : increases -> reciprocal of foodMinDis: increases -> return value increases
        """
        score = 0.0; 
        for x in successorGameState.getGhostStates():
            if manhattanDistance(newPos,x.getPosition()) <= 2:
                if(x.scaredTimer <=2 ):
                    #giving high penalty if the ghost is near
                    score -= 100
                else:
                    #if the ghost is near but afraid try to apporach it
                    score += 5
        
        
        if(len(newFood.asList())!=0):
            foodDistance = [manhattanDistance(newPos,x) for x in newFood.asList()]
            #finding the minimum manhattan distance to any food
            foodMinDis = min(foodDistance)
        else:
            foodMinDis = 1;

        #giving penalty for 'Stop'
        if(action == 'Stop'):
            score = score - 25

        return successorGameState.getScore() + score + 1/foodMinDis

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        #util.raiseNotDefined()
        
        score,action = self.MIN_MAX(gameState,0,0)
        return action


    def MIN_MAX(self,gameState,agent,depth):
        #calling MAX_VALUE assuming the max player will take the first move
        return self.MAX_VALUE(gameState,agent,depth)


    def MAX_VALUE(self,gameState,agent,depth):

        maxScore = float("-inf")
        legalActions = gameState.getLegalActions(agent)

        #checking if there is any more child nodes
        if((self.depth == depth) or len(legalActions)==0):
            return self.evaluationFunction(gameState),""
        else:
            for action in legalActions:
                "We need find the action that guarantees best result"
                
                successor = gameState.generateSuccessor(agent,action)
                successorAgent = agent +1
                successorDepth = depth

                #finalizing successorDepth and successorAgent
                if successorAgent == gameState.getNumAgents():
                    successorAgent = 0
                    successorDepth += 1
            
                #calling MIN_VALUE function or MAX_VALUE function according the succerssorAgent
                if(successorAgent == 0):
                    score = self.MAX_VALUE (successor,successorAgent,successorDepth)[0]
                else:
                    score = self.MIN_VALUE (successor,successorAgent,successorDepth)[0]

                #finding the best score for the agent
                if score > maxScore:
                    maxScore = score
                    maxAction = action
    
        return maxScore,maxAction

    def MIN_VALUE(self,gameState,agent,depth):

        minScore = float("inf")
        legalActions = gameState.getLegalActions(agent)
        
        #checking if there is any more child nodes
        if((self.depth == depth) or len(legalActions) == 0):
            return self.evaluationFunction(gameState),""
        else:
            for action in legalActions:
                "We need find the action that guarantees best result"
                
                successor = gameState.generateSuccessor(agent,action)
                successorAgent = agent +1
                successorDepth = depth

                #finalizing successorDepth and successorAgent
                if successorAgent == gameState.getNumAgents():
                    successorAgent = 0
                    successorDepth += 1
            
                #calling MIN_VALUE function or MAX_VALUE function according the succerssorAgent
                if(successorAgent == 0):
                    score = self.MAX_VALUE (successor,successorAgent,successorDepth)[0]
                else:
                    score = self.MIN_VALUE (successor,successorAgent,successorDepth)[0]

                #finding the best score for the agent
                if score < minScore:
                    minScore = score
                    minAction = action

        return minScore,minAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        score,action = self.MIN_MAX(gameState,0,0,float("-inf"),float("inf"))
        return action

    def MIN_MAX(self,gameState,agent,depth,alpha,beta):
        #calling MAX_VALUE assuming the max player will take the first move
        return self.MAX_VALUE(gameState,agent,depth,alpha,beta)


    def MAX_VALUE(self,gameState,agent,depth,alpha,beta):

        maxScore = float("-inf")
        legalActions = gameState.getLegalActions(agent)

        #checking if there is any more child nodes    
        if((self.depth == depth) or len(legalActions)==0):
            return self.evaluationFunction(gameState),""
        else:
            for action in legalActions:
                """We need find the action that guarantees best result, 
                but certain nodes need not be explore, so we want to avoid that"""
                
                successor = gameState.generateSuccessor(agent,action)
                successorAgent = agent +1
                successorDepth = depth

                #finalizing successorDepth and successorAgent
                if successorAgent == gameState.getNumAgents():
                    successorAgent = 0
                    successorDepth += 1
            
                #calling MIN_VALUE function or MAX_VALUE function according the succerssorAgent
                if(successorAgent == 0):
                    score = self.MAX_VALUE (successor,successorAgent,successorDepth,alpha,beta)[0]
                else:
                    score = self.MIN_VALUE (successor,successorAgent,successorDepth,alpha,beta)[0]

                #finding the best score for the agent
                if score > maxScore:
                    maxScore = score
                    maxAction = action
                
                #updating the value of alpha
                alpha = max(maxScore,alpha)

                #checking if the rest of the branches can be pruned
                if maxScore > beta:
                    return maxScore,maxAction
    
        return maxScore,maxAction

    def MIN_VALUE(self,gameState,agent,depth,alpha,beta):

        minScore = float("inf")
        legalActions = gameState.getLegalActions(agent)

        if((self.depth == depth) or len(legalActions) == 0):
            return self.evaluationFunction(gameState),""
        else:
            for action in legalActions:
                """We need find the action that guarantees best result, 
                but certain nodes need not be explore, so we want to avoid that"""
                
                successor = gameState.generateSuccessor(agent,action)
                successorAgent = agent +1
                successorDepth = depth

                #finalizing successorDepth and successorAgent
                if successorAgent == gameState.getNumAgents():
                    successorAgent = 0
                    successorDepth += 1
            
                #calling MIN_VALUE function or MAX_VALUE function according the succerssorAgent
                if(successorAgent == 0):
                    score = self.MAX_VALUE (successor,successorAgent,successorDepth,alpha,beta)[0]
                else:
                    score = self.MIN_VALUE (successor,successorAgent,successorDepth,alpha,beta)[0]

                #finding the best score for the agent
                if score < minScore:
                    minScore = score
                    minAction = action
                
                #updating the value of beta
                beta = min(beta,minScore)
                
                #checking if the rest of the branches can be pruned
                if minScore < alpha:
                    return minScore,minAction

        return minScore,minAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        score,action = self.MIN_MAX(gameState,0,0)
        return action

    def MIN_MAX(self,gameState,agent,depth):
        #calling MAX_VALUE assuming the max player will take the first move
        return self.MAX_VALUE(gameState,agent,depth)


    def MAX_VALUE(self,gameState,agent,depth):

        maxScore = float("-inf")
        legalActions = gameState.getLegalActions(agent)

        #checking if there is any more child nodes
        if((self.depth == depth) or len(legalActions) == 0):
            return self.evaluationFunction(gameState),""
        else:
            for action in legalActions:
                "We need find the action that guarantees best result"
                successor = gameState.generateSuccessor(agent,action)
                successorAgent = agent +1
                successorDepth = depth

                #finalizing successorDepth and successorAgent
                if successorAgent == gameState.getNumAgents():
                    successorAgent = 0
                    successorDepth += 1
            
                #calling MIN_VALUE function or MAX_VALUE function according the succerssorAgent
                if(successorAgent == 0):
                    score = self.MAX_VALUE (successor,successorAgent,successorDepth)[0]
                else:
                    score = self.MIN_VALUE (successor,successorAgent,successorDepth)[0]

                #finding the best score for the agent
                if score > maxScore:
                    maxScore = score
                    maxAction = action
    
        return maxScore,maxAction

    def MIN_VALUE(self,gameState,agent,depth):

        meanScore = 0.0
        minAction = ""
        legalActions = gameState.getLegalActions(agent)

        if((self.depth == depth) or len(legalActions) == 0):
            return self.evaluationFunction(gameState),""
        else:
            for action in legalActions:
                "We need find the the mean value of all the actions"
                
                successor = gameState.generateSuccessor(agent,action)
                successorAgent = agent +1
                successorDepth = depth

                #finalizing successorDepth and successorAgent
                if successorAgent == gameState.getNumAgents():
                    successorAgent = 0
                    successorDepth += 1
            
                #calling MIN_VALUE function or MAX_VALUE function according the succerssorAgent
                if(successorAgent == 0):
                    score = self.MAX_VALUE (successor,successorAgent,successorDepth)[0]
                else:
                    score = self.MIN_VALUE (successor,successorAgent,successorDepth)[0]

                meanScore += score
        #finding the mean score for the agent's all possible moves
        meanScore /= len(legalActions)

        return meanScore,minAction

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    """
    -> score stores a very low value(-100) when there is ghost near(<=2 blocks away) the agent
    -> We are trying not to die at any cost
    -> This still won't prevent the agent from dying in some cases, but mostly the agent will survive

    -> foodMinDis stores the lowest manhattan distance to any food (when there is atlest 1 food)
    -> foodMinDis will store value 1 if there is no food remianing
    -> we want to reduce foodMinDis, so we add reciprocal of foodMinDis to the return value
        foodMinDis : increases -> reciprocal of foodMinDis: increases -> return value increases
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    score = 0.0; 
    for x in currentGameState.getGhostStates():
        if manhattanDistance(newPos,x.getPosition()) <= 2:
            #giving high penalty if the ghost is near
            if(x.scaredTimer <=0 ):
                score -= 100
        
    if(len(newFood.asList())!=0):
        foodDistance = [manhattanDistance(newPos,x) for x in newFood.asList()]
        #finding the minimum manhattan distance to any food
        foodMinDis = min(foodDistance)
    else:
        foodMinDis = 1;

    return currentGameState.getScore() + score + 1/foodMinDis 

    
# Abbreviation
better = betterEvaluationFunction
