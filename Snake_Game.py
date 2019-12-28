from snake import Snake
from Game import Game
import numpy as np
import graphics
import time
import random

############ Main ##################


# Records how many children each NN has  
rate_update = 4 

# Simply counts what generation we are on
current_gen = 0

# Records the highest score seen so far in training 
# So we can save the weights of that neural network
highestScore = 7

# This creates the inital cohort of neural networks
# numGames is the number of games/nn's to have in the cohort
# Returns the cohort of neural networks
def generation_0( numGames ):

    allGames = [  ]

    for i in range(numGames):
        myGame = Game(20, 20, 600, 500, False)
        allGames.append(myGame)
        myGame.drawBoard()

        while ( True ):    
            move = myGame.generate_NN_Move() 
            if ( myGame.isOver == True):
                break
            else:
                myGame.nextState( move )

    # Find the best nets in the set - take the ones with the most moves
    allDirections = []
    maxIndex = 0
    secondIndex = 1 
    for i in range(1, len(allGames) ):
        if ( allGames[i].neural_network.checkMoves() > 3.0  ):
            if ( allGames[i].moveNumber < 900 ):
                allDirections.append( allGames[i].neural_network )

    # Return the NN's that have moved in all the directions
    return allDirections

# This takes a group of NN's and the number of children each can have 
# and generates the next generation of NN's
# 
def nextGeneration(currentCohort, rate): 
    
    global rate_update
    global current_gen
    double = False
    
    children = []
    for i in range(len(currentCohort) - 1 ):
            
        # Change how pairs are made
        children_new = currentCohort[i].crossOver(currentCohort[i + 1], rate)
        children.extend(children_new)

    
    allGames = []
    # Run a game for each child
    for i in range( len(children)  ):
        myGame = Game(20, 20, 600, 500, False)
            
        myGame.neural_network = children[i]

        allGames.append(myGame)

        myGame.drawBoard()

        while ( True ):
            move = myGame.generate_NN_Move()
            if ( myGame.isOver == True):
                if ( myGame.score > 2.0 ):
                    double = True
                    # rate_update = 10
                break
            else:
                myGame.nextState( move )
            
    currentCohort = []
    for i in range(1, len(allGames) ):
        if ( allGames[i].neural_network.checkMoves() > 1.0):
            if ( allGames[i].moveNumber < 900 ):                
                
                if ( current_gen >= 1):
                    if ( (allGames[i].score > 2) ):  # and (double == False)  ):
                        currentCohort.append( allGames[i].neural_network )
                    
                elif ( (allGames[i].score > 0) ):  # and (double == False)  ):
                    currentCohort.append( allGames[i].neural_network )
                

        # If we have a new high score, save the weights 
        global highestScore
        if ( allGames[i].score > highestScore ):
            highestScore = allGames[i].score
            print("Saved weights on a game with a score >= " + str(highestScore) )
            allGames[i].neural_network.saveWeights()
    
    return currentCohort


# Create the inital conditions and begin training
numGenerations = 0
# gen_now = generation_0(2000)

rate_level = [5, 120, 10, 10, 10, 10, 10, 10, 10, 10, 10]
for i in range( numGenerations ):
    current_gen = i
    print("Generation: " + str(i) )
    
    gen_now = nextGeneration( gen_now, rate_level[i] )

# random.shuffle(gen_now)

g = input("Press Enter to see the trained snake")

numGames = 5
for i in range(numGames):
    myGame = Game(20, 20, 900, 900, True)
    
    #myGame.neural_network.saveWeights()
    # Load trained weights
    myGame.neural_network.loadWeights()
    
    # myGame.neural_network = gen_now[0]
    
    myGame.drawBoard()

    while ( True ):
        time.sleep(0.2)
        move = myGame.generate_NN_Move()
        if(myGame.neural_network.checkMoves() == True):
            pass 

        if ( myGame.isOver == True):
            break
        else:
            myGame.nextState( move )


####################################
