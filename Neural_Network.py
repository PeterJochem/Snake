# This file implements the neural network

import numpy as np
import random
import copy

class Neural_Network:
 
    # NumInputs is the number of input neurons to the NN
    # HiddenArch is a list of the number of neurons at each HIDDEN layer of the NN
    # numOutput is the number of output neurons
    def __init__(self, numInputs, hiddenArch, numOutput):
        
        self.numInputs = numInputs
        self.numOutput = numOutput

        # Create the hidden weight sets with the right sizes 
        self.allWeights = []

        for i in range( -1, len(hiddenArch)  ):
            # Check the edge cases
            # print(i)
            if (i == -1):
                self.allWeights.append( self.init_Weights(numInputs, hiddenArch[0] ) )
        
            elif ( i == len(hiddenArch) - 1):
                self.allWeights.append( self.init_Weights( hiddenArch[i], self.numOutput ) )
            else:
                # Normal case
                self.allWeights.append( self.init_Weights( hiddenArch[i], hiddenArch[i + 1] ) )
         
        
        # These fields record if the NN has moved in the given direction yet
        self.up = False
        self.down = False
        self.left = False
        self.right = False
    
    # This method checks how many directions the snake has moved so far
    # It returns the number of unique directions
    def checkMoves(self):
        count = 0
        if (self.up):
            count = count + 1

        if ( self.down ):
            # Occurs
            count = count + 1

        if(self.left):
            count = count + 1

        if(self.right):
            # Occurs
            count = count + 1

        #if ( count == 3):
        #    print("TRIPLE")
        #if (count == 2):
        #    print("Double")
        #if (count == 1):
        #    print("SINGLE")
        return count
        
    # This method checks if the snake/NN has moved in all 4 directions
    # Return True if it has moved in all 4 directions
    # Return False otherwise
    def checkDirections(self):

        if (self.up and self.down and self.left and self.right):
            return True
        return False
    
    # This method creates a matrix of the size (numRow, numCol)
    # with random values in the interval of [start, stop]
    # It returns the given matrix
    def createVector(self, start, stop, numRow, numCol):

        returnVector = np.zeros( (numRow, numCol) )

        for i in range(len( returnVector ) ):
            for j in range(len( returnVector[0] ) ):
                returnVector[i][j] = random.uniform(start, stop)
        
        return returnVector
    
    # This method takes the current neural net and crosses it over
    # to make the offspring
    # Input: partner is another NN
    # Output: a set of NN's called offspring
    def crossOver(self, partner, numChildren):

        offSpring = []
        
        # Re-set the state's fields so we can reuse
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.id = 0

        # Try averaging all the entries +/ random noise
        for i in range(numChildren):

            nextChild_solo =  copy.deepcopy(self)
            nextChild_couple = copy.deepcopy(self)
            
            for j in range(len(self.allWeights) ):
                
                nextChild_solo.allWeights[j] = ( ((self.allWeights[j] + partner.allWeights[j]) ) / 2.0) #+ ( self.createVector( -100.0, 100.0, len(self.w1), len(self.w1[0])  )  )
                nextChild_solo.allWeights[j] = ( ((self.allWeights[j] + partner.allWeights[j]) ) / 2.0) #+ ( self.createVector( -100.0, 100.0, len(self.w2), len(self.w2[0] ) )  )

                nextChild_couple.allWeights[j] = ( ((self.allWeights[j]) ) ) + ( self.createVector( -1.0, 1.0, len(self.allWeights[j]), len(self.allWeights[j][0] )  )  )
                nextChild_couple.allWeights[j] = ( ((self.allWeights[j]) ) ) + ( self.createVector( -1.0, 1.0, len(self.allWeights[j]), len(self.allWeights[j][0] )  )  )

            offSpring.append(nextChild_solo)
            offSpring.append(nextChild_couple)

        return offSpring



    # This randomnly a single layer's of the NN's weights
    # Input: The length of the desired vector 
    # Output: The randomnly initalized weight vector
    def init_Weights(self, numColumns, numRows):
        
        # Must make the weights smaller or else softmax returns infinite
        returnVector = self.createVector(-1.0, 1.0, numColumns, numRows)

        return returnVector
        
         
    # This function implements the rectified linear unit
    def relu( self, myInput ):
        
        myCopy = copy.deepcopy(myInput)

        for i in range( len(myInput) ):
            for j in range( len(myInput[i] ) ):
                myCopy[i, j] = max(0.0, myInput[i,j] )
    
        return myCopy
    
    # This function implements the softmax function
    # Input is a 1 x N vector where N is the number of categorical output variables 
    # Return is a 1 x N vector of the softmax for each of the N entries 
    def softmax(self, inVector):
        
        returnVector = np.zeros(len(inVector) )
        
        # Traverse the array once to compute the integral term
        integral = float( np.sum( np.exp( inVector ) ) )
        
        for i in range(len(inVector) ):

           returnVector[i] = (np.e ** inVector[i] ) / integral   
        
        return returnVector


    # This method takes an input vector
    # Input: an input vector to forward propogate 
    # Output: The maximum index of the output vector
    def forwardProp(self, inputVector):
        
        # WHY DOES RELU PREVENT TRIPLES??????
        
        layer_next = inputVector.copy().T
         
        for i in range(len(self.allWeights) ):
            layer_next =  np.matmul( layer_next.copy(), self.allWeights[i].copy() )
            # layer_next = self.relu( np.matmul( layer_next.copy(), self.allWeights[i].copy() ) )

        # layer_next = self.softmax(layer_next)

        # Use the softmax function at the output layer
        #outputVector = # np.array( [ self.softmax( (np.matmul( layer_1.copy(), self.w2.copy() ) )[0] ) ] ) # + self.bias_2 )
        
        return layer_next

    # This method saves the given weights to the filed called best_weights.txt
    def saveWeights(self):

        myFile = open("best_weights.txt", "w+")

        # Record the meta-data
        myFile.write( "input:" + str( self.numInputs ) )
        myFile.write("\n")

        myFile.write( "numLayers:" + str( len(self.allWeights) + 1) )
        myFile.write("\n")

        for i in range(len(self.allWeights) ):
            myFile.write( "layer:" + str( len(self.allWeights[i] ) ) )
            myFile.write("\n")

        
        myFile.write( "output:" + str( self.numOutput ) )
        myFile.write("\n")

        # Save the all weights
        for i in range(len( self.allWeights) ):
            for j in range (len (self.allWeights[i]) ):
                for k in range(len( self.allWeights[i][j] ) ):
                    myFile.write( str(self.allWeights[i][j][k] ) )
                    myFile.write( "\n" )

        myFile.close()

    # This method loads the weights from best_weights.txt into the current NN 
    def loadWeights(self):
        myFile = open("best_weights.txt", "r")

        allLines = myFile.readlines()
        lineNumber = 0

        # Create the empty weight sets - we will fill them below 
        newWeights = copy.deepcopy(self.allWeights)
        allWidths = []

        # Records where in the matrix to write the next value
        currentLayer = 0
        currentRow = 0
        currentColumn = 0
        currentSet = 1
        for x in allLines:
            if ( lineNumber == 0):
                self.numInputs = int( (x.split(":") )[1] )
                lineNumber = lineNumber + 1
                continue
            elif ( lineNumber == 1):
                numLayers = int( (x.split(":") )[1] )
                lineNumber = lineNumber + 1
                
                continue
            elif( (lineNumber >= 2) and ( lineNumber < numLayers + 2) ):
                
                allWidths.append( int( (x.split(":") )[1] ) )

                lineNumber = lineNumber + 1
                continue

            # Get the next value from the file 
            value_now = x
        
            # Write the weights
            newWeights[currentLayer][currentRow, currentColumn] = value_now

            currentColumn = currentColumn + 1
            if ( currentColumn >= len(newWeights[currentLayer][0] ) ):
                currentColumn = 0
                currentRow = currentRow + 1

            if ( currentRow >=  len(newWeights[currentLayer] ) ):
                currentRow = 0
                currentColumn = 0
                currentLayer = currentLayer + 1
            
            if ( currentLayer >= len(newWeights) ):
                break
                
        self.allWeights = newWeights

        myFile.close()







