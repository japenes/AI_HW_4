import random
import sys
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *
#from Gene import *


##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    genes = []
    index = 0

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "Jordan")
    
    ##
    #getPlacement
    #
    #Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        numToPlace = 0
        #implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
            return self.genes[self.index].attributes[0:11]
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            return self.genes[self.index].attributes[11:]
        else:
            return [(0, 0)]
    
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        moves = listAllLegalMoves(currentState)
        selectedMove = moves[random.randint(0,len(moves) - 1)];

        #don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0,len(moves) - 1)];
            
        return selectedMove
    
    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        #Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

    ##
    #registerWin
    #
    # This agent doens't learn
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        pass

    class Gene:
        attributes = []
        fitnessScore = 0

        def __init__(self, array):
            self.attributes = array
            fitnessScore = 0

        def setFitness(self, score):
            fitnessScore = score

    def initializePopulation(self, size):
        for i in range(0, size):
            randomGene = []
            for i in range(0,11):
                x = random.randint(0,9)
                y = random.randint(0,3)
                while (x,y) in randomGene:
                    x = random.randint(0, 9)
                    y = random.randint(0, 3)
            for i in range(0,2):
                y = random.randint(6, 9)
                x = random.randint(0, 14-y)
                if (x, y) == (4, 8):
                    x += 1
                while (x, y) in randomGene:
                    y = random.randint(6, 9)
                    x = random.randint(0, 14 - y)
                    if (x, y) == (4, 8):
                        x += 1
                randomGene.append((x,y))
            self.genes[i] = self.Gene(randomGene)

    def haveChildren(self, a, b):
        randomIndex = random.randint(1,24)
        #Child 1
        parent1 = a[:randomIndex]
        parent2 = b[randomIndex:]
        for i in range(0, len(parent2)):
            while parent2[i] in parent1:
                if (randomIndex+i < 11):
                    x = random.randint(0, 9)
                    y = random.randint(0, 3)
                else:
                    y = random.randint(6, 9)
                    x = random.randint(0, 14 - y)
                    if (x, y) == (4, 8):
                        x += 1
            parent2[i] = (x, y)
        child1 = parent1+parent2
        parent1 = b[:randomIndex]
        parent2 = a[randomIndex:]
        for i in range(0, len(parent2)):
            while parent2[i] in parent1:
                if randomIndex+i < 11:
                    x = random.randint(0, 9)
                    y = random.randint(0, 3)
                else:
                    y = random.randint(6, 9)
                    x = random.randint(0, 14 - y)
                    if (x, y) == (4, 8):
                        x += 1
            parent2[i] = (x, y)
        child2 = parent1+parent2
        for i in range(0,len(child1)):
            rand = random.randint(0,99)
            if rand > 90:
                if i < 11:
                    x = random.randint(0, 9)
                    y = random.randint(0, 3)
                    while (x, y) in child1:
                        x = random.randint(0, 9)
                        y = random.randint(0, 3)
                else:
                    y = random.randint(6, 9)
                    x = random.randint(0, 14 - y)
                    if (x, y) == (4, 8):
                        x += 1
                    while (x, y) in child2:
                        y = random.randint(6, 9)
                        x = random.randint(0, 14 - y)
                        if (x, y) == (4, 8):
                            x += 1
                child1[i] = (x, y)
        for i in range(0,len(child2)):
            rand = random.randint(0,99)
            if rand > 90:
                if (i < 11):
                    x = random.randint(0, 9)
                    y = random.randint(0, 3)
                    while (x, y) in child2:
                        x = random.randint(0, 9)
                        y = random.randint(0, 3)
                else:
                    y = random.randint(6, 9)
                    x = random.randint(0, 14 - y)
                    if (x, y) == (4, 8):
                        x += 1
                    while (x, y) in child2:
                        y = random.randint(6, 9)
                        x = random.randint(0, 14 - y)
                        if (x, y) == (4, 8):
                            x += 1
                child2[i] = (x, y)
        return child1, child2

    def evaluateFitness(self, state):
        # queen health
        # enemy queen health
        # anthill health
        # enemy anthill health
        # food count
        # ant count
        # who won
        ourAnts = getAntList(state, 0, (QUEEN, WORKER, DRONE, SOLDIER, R_SOLDIER))
        theirAnts = getAntList(state, 1, (QUEEN, WORKER, DRONE, SOLDIER, R_SOLDIER))
        ourQueen = getAntList(state, 0, (QUEEN, ))
        theirQueen = getAntList(state, 1, (QUEEN, ))
        ourAnthill = getConstrList(state, 0, (ANTHILL, ))
        theirAnthill = getConstrList(state, 1, (ANTHILL, ))
        winner = getWinner(state)


        if len(ourQueen) == 0:
            queenHealthDifference = -1*theirQueen.health
        elif len(theirQueen) == 0:
            queenHealthDifference = ourQueen.health
        else:
            queenHealthDifference = ourQueen.health - theirQueen.health

        anthillHealthDifference = ourAnthill.health - theirAnthill.health
        foodCount = state.inventories[0].foodCount

        fitnessValue = 100*(1-winner) + 2*queenHealthDifference + 10*anthillHealthDifference + 2*foodCount
        return fitnessValue


