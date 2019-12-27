# This file implements the neural network

import numpy as np
import random
import copy

class Neural_Network:

    # Describe the inputs 
    # NumInputs is 
    # HiddenArch is a list of the number of neurons at each HIDDEN layer of the NN
    # numOutput is 
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
         
        for i in range(len( self.allWeights ) ):
            #print("")
            #print(self.allWeights[i])
            #print("")
            pass
        
        # Pass in the size of the input
        # self.w1 = self.init_Weights(numInputs, numHidden)
        # self.bias_1 = np.ones(numHidden) * 0.1
        # Pass in the size of the intermediate vector
        # self.w2 = self.init_Weights(numHidden, numOutput)
        # self.bias_2 = np.ones(numOutput) * 0.1
        # For testing
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        ###########
    
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
       
        #if ( self.up and self.right ):
        #    print("up and right")
        
        #if ( self.down and self.right  ):
        #    print("down and right ")
        
        # Observed
        #if( self.up and self.left ):
        #    print("up and left")
        
        # Observed
        #if ( self.down and self.left ):
        #    print("down and left")
        
        #if ( self.down and self.up ):
        #    print("up and down")
        
        # Observed
        #if ( self.right and self.left  ):
        #    print("left and right")
    

       #if (count == 2):
        #    print("Double")
        #if (count == 1):
        #    print("SINGLE")
        return count
        

    def checkDirections(self):

        if (self.up and self.down and self.left and self.right):
            return True
        return False
    
    def createVector(self, start, stop, numCol, numRow):

        returnVector = np.zeros( (numCol, numRow) )

        for i in range(len( returnVector ) ):
            for j in range(len( returnVector[0] ) ):
                returnVector[i][j] =random.uniform(start, stop)
        
        return returnVector
    
    # This method takes the current neural net and crosses it over
    # to make the offspring
    # Input:
    # Output:
    def crossOver(self, partner, numChildren):

        offSpring = []
        
        # Re-set the state's fields
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.id = 0

        # Try averaging all the entries +/ random noise

        for i in range(numChildren):

            nextChild_solo =  copy.deepcopy(self)
            nextChild_couple = copy.deepcopy(self)
            
            for i in range(len(self.allWeights) ):
                
                nextChild_solo.allWeights[i] = ( ((self.allWeights[i] + partner.allWeights[i]) ) / 2.0) #+ ( self.createVector( -100.0, 100.0, len(self.w1), len(self.w1[0])  )  )
                nextChild_solo.allWeights[i] = ( ((self.allWeights[i] + partner.allWeights[i]) ) / 2.0) #+ ( self.createVector( -100.0, 100.0, len(self.w2), len(self.w2[0] ) )  )

                nextChild_couple.allWeights[i] = ( ((self.allWeights[i]) ) ) + ( self.createVector( -1.0, 1.0, len(self.allWeights[i]), len(self.allWeights[i][0] )  )  )
                nextChild_couple.allWeights[i] = ( ((self.allWeights[i]) ) ) + ( self.createVector( -1.0, 1.0, len(self.allWeights[i]), len(self.allWeights[i][0] )  )  )

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
        
        # print( returnVector )
        return returnVector


    # This method takes an input vector
    # Input: an input vector to forward propogate 
    # Output: The maximum index of the output vector
    def forwardProp(self, inputVector):
        
        #print("")   
        #print( np.matmul( inputVector.copy().T, self.w1.copy() ) )
        # print("")   
        
        # WHY DOES RELU PREVENT TRIPLES??????
        #layer_1 = self.relu( np.matmul( inputVector.copy().T, self.w1.copy() ) )  # + self.bias_1 )   
        
        layer_next = inputVector.copy().T
         
        for i in range(len(self.allWeights) ):
            # layer_next =  np.matmul( layer_next.copy(), self.allWeights[i].copy() )
            layer_next = self.relu( np.matmul( layer_next.copy(), self.allWeights[i].copy() ) )


        # layer_1 =  np.matmul( inputVector.copy().T, self.w1.copy() )

        # Use the softmax function at the output layer
        #outputVector = # np.array( [ self.softmax( (np.matmul( layer_1.copy(), self.w2.copy() ) )[0] ) ] ) # + self.bias_2 )
        
        # outputVector = np.array( [ np.matmul( layer_1.copy(), self.w2.copy() )[0]  ] ) 
        #outputVector = np.matmul( layer_1.copy(), self.w2.copy() )
    

        #print("") 
        #print(outputVector)
        #print("")
        
        #while(True):
        #    pass
        
        
        return layer_next

    
    def saveWeights(self):

        myFile = open("best_weights.txt", "w+")

        # Record the meta-data
        myFile.write( "input:" + str( self.numInputs ) )
        myFile.write("\n")

        myFile.write( "numLayers:" + str( len(self.allWeights) + 1) )
        myFile.write("\n")

        # Write the hidden layers - FIX to make more general!
        # change the name of this to hidden width
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

    # Load the weights from the file
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
                #print(numLayers)
                #print(len(self.allWeights) )
                # Record all the number of weights
            elif( (lineNumber >= 2) and ( lineNumber < numLayers + 2) ):
                
                allWidths.append( int( (x.split(":") )[1] ) )
                    
                # print( "Next width is " + str(allWidths[lineNumber - 2] ) )

                lineNumber = lineNumber + 1
                continue

            # Get the next value from the file 
            value_now = x
        
            # Write the weights
            newWeights[currentLayer][currentRow, currentColumn] = value_now

            # Check for change to next weight set 
            # Update the weight sets  
            # Increment the current row and column
            # currentRow = currentRow + 1
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




    # This method takes itself and a mate's weights
    # and mutate them to return a child 
    # Input:
    # Output: child neural net
    def mutate(self, mate):
         
        # Return a new, child neural network
        pass 


####### Main for testing ###########

#myNN = Neural_Network(16, 5, 4)
#inputVector = np.zeros(16)
#print( myNN.forwardProp( inputVector  ) )




