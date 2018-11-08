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
    SIZE = 100
    TESTS = 100
    PERCENTAGE = .2

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "Jordan")
        self.genes = []
        self.fitnessValues = [ None ] * self.TESTS
        self.index = 0
        self.counter = 0
        self.moveCounter = 0
        self.initializePopulation(self.SIZE)

    
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
        self.state = currentState
        self.moveCounter += 1
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
    # This agent learns better ways to arrange the structures (Anthill, Tunnel, Grass, Food)
    #
    def registerWin(self, hasWon):
        self.fitnessValues[self.counter] = self.evaluateFitness(self.state)
        self.moveCounter = 0
        self.counter += 1
        if self.counter == self.TESTS:
            self.genes[self.index].setFitness(sum(self.fitnessValues)/float(self.SIZE))
            self.index += 1
            self.counter = 0
            if self.index >= len(self.genes):
                #make new generation
                self.genes = self.newGeneration()
                self.index = 0
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
            for i in range(0, 11):
                x = random.randint(0, 9)
                y = random.randint(0, 3)
                while (x,y) in randomGene:
                    x = random.randint(0, 9)
                    y = random.randint(0, 3)
                randomGene.append((x, y))
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
                randomGene.append((x, y))
            self.genes.append(self.Gene(randomGene))

    def haveChildren(self, a, b):
        randomIndex = random.randint(1, 24)
        #Child 1
        parent1 = a[:randomIndex]
        parent2 = b[randomIndex:]
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
            rand = random.randint(0, 99)
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
                    while (x, y) in child1:
                        y = random.randint(6, 9)
                        x = random.randint(0, 14 - y)
                        if (x, y) == (4, 8):
                            x += 1
                child1[i] = (x, y)
        for i in range(0,len(child2)):
            rand = random.randint(0,99)
            if rand > 90:
                if i < 11:
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
        return self.Gene(child1), self.Gene(child2)

    def evaluateFitness(self, state):
        # queen health
        # enemy queen health
        # anthill health
        # enemy anthill health
        # food count
        # number of moves
        # who won

        me = state.whoseTurn

        ourQueen = state.inventories[me].getQueen()
        theirQueen = state.inventories[1-me].getQueen()
        ourAnthill = state.inventories[me].getAnthill()
        theirAnthill = state.inventories[1-me].getAnthill()


        if ourQueen == None:
            queenHealthDifference = -1*theirQueen.health
        elif theirQueen == None:
            queenHealthDifference = ourQueen.health
        else:
            queenHealthDifference = ourQueen.health - theirQueen.health

        anthillHealthDifference = ourAnthill.captureHealth - theirAnthill.captureHealth
        foodCount = state.inventories[me].foodCount

        fitnessValue = 2*queenHealthDifference + 10*anthillHealthDifference + 2*foodCount + \
                       .1*self.moveCounter
        # print("didWin: %d    queenHealth: %d    anthillHealth: %d    foodCount: %d    total: %d" %
        #      (100*didWin, 2*queenHealthDifference, 10*anthillHealthDifference, 2*foodCount, fitnessValue))
        return fitnessValue

    def newGeneration(self):
        sortedList = sorted(self.genes, key=lambda x: x.fitnessScore)
        totalBest = len(self.genes)*self.PERCENTAGE
        newGenes = []
        for i in range(0, int(len(self.genes)/2)):
            a = random.randint(0, int(totalBest))
            b = random.randint(0, int(totalBest))
            while b == a:
                b = random.randint(0, int(totalBest))
            children = self.haveChildren(sortedList[a].attributes, sortedList[b].attributes)
            newGenes.append(children[0])
            newGenes.append(children[1])

        self.printState(sortedList[0])
        return newGenes

    def printState(self, gene):
        outputState = GameState.getBlankState()
        coords = gene.attributes
        p1Queen = Ant(coords[0], QUEEN, 0)
        p1Hill = Building(coords[0], ANTHILL, 0)
        p1Tunnel = Building(coords[1], TUNNEL, 0)
        for i in range(0,9):
            p1Grass = Building(coords[i+2], GRASS, 0)
            outputState.board[coords[i+2][0]][coords[i+2][1]].constr = p1Grass
            outputState.inventories[0].constrs.append(p1Grass)
        for i in range(0,2):
            p1Food = Building(coords[i + 11], FOOD, 0)
            outputState.inventories[2].constrs.append(p1Food)
        outputState.inventories[0].ants.append(p1Queen)
        outputState.inventories[0].constrs.append(p1Hill)
        outputState.inventories[0].constrs.append(p1Tunnel)
        asciiPrintState(outputState)