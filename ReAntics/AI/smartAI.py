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

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "Ai")
        self.depth_limit = 2
        self.anthillCoords = None
        self.tunnelCoords = None
        self.food1Coords = None
        self.food2Coords = None
        self.maxTunnelDist = 0
        self.maxFood1Dist = 0
        self.maxFood2Dist = 0

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
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on your side of the board
                    y = random.randint(0, 3)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
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
        root = {"move":None, "state":currentState, "value":0, "parent":None, "depth":0}
        # tree = {"0":[root,]}
        move = self.bfs(root, 0)

        # moves = listAllLegalMoves(currentState)
        # selectedMove = moves[random.randint(0,len(moves) - 1)];
        #
        # #don't do a build move if there are already 3+ ants
        # numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        # while (selectedMove.moveType == BUILD and numAnts >= 3):
        #     selectedMove = moves[random.randint(0,len(moves) - 1)]

        return move

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

    ##
    #evaluateState
    #
    # This agent evaluates the state and returns a double between -1.0 and 1.0
    #
    def evaluateState(self, gs):
        myInv = getCurrPlayerInventory(gs)
        theirInv = getEnemyInv(self, gs)
        me = gs.whoseTurn

        #do this once
        if self.maxTunnelDist == 0:
            self.tunnelCoords = getConstrList(gs, me, (TUNNEL,))[0].coords
            print(self.tunnelCoords)
            foods = getConstrList(gs, None, (FOOD,))
            self.myFood = foods[0]
            #find the food closest to the tunnel
            bestDistSoFar = 1000 #i.e., infinity
            for food in foods:
                dist = stepsToReach(gs, self.tunnelCoords, food.coords)
                if (dist < bestDistSoFar):
                    self.myFoodCoords = food.coords
                    bestDistSoFar = dist

            print(self.myFoodCoords)

            for i in range(0,10):
                for j in range(0,10):
                    tunnelDist = approxDist((i,j), self.tunnelCoords)
                    if (tunnelDist > self.maxTunnelDist):
                        self.maxTunnelDist = tunnelDist


        #if we have more than three workers, throw out this option
        myWorkers = getAntList(gs, me, (WORKER,))
        if len(myWorkers) > 2:
            return -1.0
        else:
            myWorkerScore = len(myWorkers) / 2

        #if our queen is on our anthill or our tunnel, we're in a bad state
        myQueen = getAntList(gs, me, (QUEEN,))[0]
        #if myQueen.coords == 0:

        #give positive weight to soldiers that are closer to the enemy queen
        mySoldiers = getAntList(gs, me, (SOLDIER,))
        enemyQueen = getAntList(gs, 1-me, (QUEEN,))[0]
        soldierScore = 0.0
        #starts at one so soldierScore avoids division by zero
        maxSoldierScore = 1.0
        for soldier in mySoldiers:
            #give priority to moves that make more soldiers
            soldierScore += 40
            maxSoldierScore += 40
            #then give priority to moves that move soldiers close to the enemy queen
            soldierScore += 20 - approxDist(soldier.coords, enemyQueen.coords)
            maxSoldierScore += 19
        soldierScore = soldierScore / maxSoldierScore

        #calculate ant score
        myAnts = myInv.ants
        myAntScore = 0
        myAntHealthScore = 0
        for ant in myAnts:
            myAntHealthScore += ant.health
            if ant.type == WORKER:
                myAntScore += 1
            elif ant.type == SOLDIER:
                myAntScore += 4
            elif ant.type == DRONE:
                myAntScore += 2
            elif ant.type == R_SOLDIER:
                myAntScore += 3
        #theirAnts = getAntList(gs, 1-me, (QUEEN, WORKER, DRONE, SOLDIER, R_SOLDIER))
        theirAnts = theirInv.ants
        theirAntScore = 0
        theirAntHealthScore = 0
        for ant in myAnts:
            theirAntHealthScore += ant.health
            if ant.type == WORKER:
                theirAntScore += 1
            elif ant.type == QUEEN:
                theirAntScore += 4
            elif ant.type == SOLDIER:
                theirAntScore += 4
            elif ant.type == DRONE:
                theirAntScore += 2
            elif ant.type == R_SOLDIER:
                theirAntScore += 3
        antDiff = (myAntScore - theirAntScore) / max(myAntScore, theirAntScore)

        antHealthDiff = (myAntHealthScore - theirAntHealthScore) / (myAntScore + theirAntScore)

        #queen health
        myQueen = getAntList(gs, me, (QUEEN,))
        theirQueen = getAntList(gs, 1-me, (QUEEN,))
        if len(theirQueen) != 0 and len(myQueen) != 0:
            queenDiff = (myQueen[0].health - theirQueen[0].health) / 10

        #calculating food and give positive weight to worker ant nearer the tunnel that are carrying food
        theirWorkers = getAntList(gs, 1-me, (WORKER,))

        myCarryScore = 0.0
        nearTunnelScore = 0
        nearFoodScore = 0
        numWorkersCarrying = 0
        for worker in myWorkers:
            if worker.carrying:
                numWorkersCarrying += 1
                myCarryScore += 1
                nearTunnelScore += approxDist(worker.coords, self.tunnelCoords) / self.maxTunnelDist
            else:
                nearFoodScore +=  approxDist(worker.coords, self.myFoodCoords) / 10

        if numWorkersCarrying != 0:
            nearTunnelScore /= numWorkersCarrying
        if (len(myWorkers)-numWorkersCarrying) != 0:
            nearFoodScore /= (len(myWorkers)-numWorkersCarrying)


        theirCarryScore = 0.0
        for worker in theirWorkers:
            if worker.carrying:
                theirCarryScore += 1

        myPotentialFood = myInv.foodCount + (myCarryScore / 2)
        theirPotentialFood = theirInv.foodCount + (theirCarryScore / 2)
        foodDiff = (myPotentialFood - theirPotentialFood) / 11

        return (nearTunnelScore + nearFoodScore + soldierScore) / 3


    def expandNode(self, node):
        moves = listAllLegalMoves(node["state"])
        if len(moves) != 1:
            for move in moves:
                if move.moveType == END:
                    moves.remove(move)
        moveList = []
        for move in moves:
            newNode = {"move":move}
            newNode["state"] = getNextState(node["state"], newNode["move"])
            getEnemyInv(self, newNode["state"])
            newNode["value"] = self.evaluateState(newNode["state"])
            newNode["parent"] = node
            newNode["depth"] = node["depth"]+1
            moveList.append (newNode)
        return moveList


    def evalListNodes(self, nodes):
        sum = 0
        for node in nodes:
            sum += node["value"]
        return sum / len(nodes)


    def bfs(self, node, depth):
        newNodes = self.expandNode(node)
        if depth < self.depth_limit:
            for n in newNodes:
                # print(str(newNodes.index(n)) + " , " + str(depth))
                n["value"] = self.bfs(n, depth+1)
        evaluation = self.evalListNodes(newNodes)
        if depth > 0:
            return evaluation
        else:
            max = -10
            move = None
            for n in newNodes:
                if n["value"] > max:
                    max = n["value"]
                    move = n["move"]
            return move
