from snake import Snake
from Game import Game
import numpy as np
import graphics
import time
import random

############ Main ##################

# Create game 
# Run the game's logic

rate_update = 4 

current_gen = 0

def generation_0( numGames ):

    allGames = [  ]

    for i in range(numGames):
        # print("Game: " + str(i) )
        myGame = Game(20, 20, 600, 500, False)
        allGames.append(myGame)
        myGame.drawBoard()

        while ( True ):    
            # time.sleep(0.4)
            move = myGame.generate_NN_Move() 
            if ( myGame.isOver == True):
                #if(myGame.neural_network.checkDirections() == True):
                #    print("ALL 4 directions found!!")
                break
            else:
                myGame.nextState( move )

    # Find the best nets in the set - take the ones with the most moves
    doubles = []
    maxIndex = 0
    secondIndex = 1 
    for i in range(1, len(allGames) ):
        if ( allGames[i].neural_network.checkMoves() > 3.0  ):
            if ( allGames[i].moveNumber < 900 ):
                doubles.append( allGames[i].neural_network )

    print("")
    print("The percentage of doubles is " + str( float( len(doubles) ) / float( len( allGames)  )   ) )
    print("")
    # Take the two best NN and mutate them

    return doubles



def nextGeneration(doubles, rate): 
    
    global rate_update
    global current_gen
    double = False
    
    children = []
    for i in range(len(doubles) - 1 ):
            
        # Change how pairs are made
        children_new = doubles[i].crossOver(doubles[i + 1], rate)
        children.extend(children_new)

    
    allGames = []
    # Run a game for each child
    for i in range( len(children)  ):
        # print("Game: " + str(i) )
        myGame = Game(20, 20, 600, 500, False)
            
        myGame.neural_network = children[i]

        allGames.append(myGame)

        myGame.drawBoard()


        while ( True ):
            # time.sleep(0.4)
            move = myGame.generate_NN_Move()
            if ( myGame.isOver == True):
                if ( myGame.score > 2.0 ):
                    double = True
                    # rate_update = 10
                #if(myGame.neural_network.checkDirections() == True):       
                #    print("ALL 4 directions found!!")
                break
            else:
                myGame.nextState( move )
            

    doubles = []
    for i in range(1, len(allGames) ):
        if ( allGames[i].neural_network.checkMoves() > 1.0  ):
            if ( allGames[i].moveNumber < 900 ):                
                
                if ( current_gen == 1):
                    if ( (allGames[i].score > 5) ):  # and (double == False)  ):
                        doubles.append( allGames[i].neural_network )
                    
                elif ( (allGames[i].score > 0) ):  # and (double == False)  ):
                    doubles.append( allGames[i].neural_network )
                
                #if ( (allGames[i].score > 2) ):  #  and (double == True)  ):
                #    doubles.append( allGames[i].neural_network )


        if (allGames[i].score > 2.0   ):
            print("NN scored! " + str( allGames[i].score  ) )


    print("")
    print("The percentage of doubles is " + str( float( len(doubles) ) / float( len( allGames)  )   ) )
    print("")

    return doubles


numGenerations = 0
#gen_now = generation_0(2000)

rate_level = [100, 50, 10]
for i in range( numGenerations ):
    current_gen = i
    print("Generation: " + str(i) )
    
    gen_now = nextGeneration( gen_now, rate_level[i] )

#random.shuffle(gen_now)

#gen_now[0].saveWeights()
#gen_now[0].loadWeights()


g = input("Press Enter to see the trained snake")

numGames = 5
for i in range(numGames):
    # print("Game: " + str(i) )
    myGame = Game(20, 20, 900, 900, True)
    
    #myGame.neural_network.saveWeights()
    # Load trained weights
    myGame.neural_network.loadWeights()
    
    #myGame.neural_network = gen_now[0]
    
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
