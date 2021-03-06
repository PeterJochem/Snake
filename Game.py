# This class implements a single game 
import graphics
import numpy as np
from snake import Snake
from graphics import *
from random import random
from Neural_Network import Neural_Network

class Game: 
    
    # length_grid is the number of rows in the grid 
    # width grid is the width of each grid 
    # legth_window is the number of pixels in the window
    # width_window is the number of pixels in the window
    # display is the graphics window we will write to  
    def __init__(self, length_grid, width_grid, length_window, width_window, display):
        
        self.score = 0
        
        self.isOver = False
        
        self.moveNumber = 0

        self.message = None

        self.length_grid = length_grid
        self.width_grid = width_grid
        self.board = np.zeros( (length_grid, width_grid) )
    
        self.length_window = length_window
        self.width_window = width_window
        
        if ( display == True ):
            self.window = GraphWin("Snake", self.length_window, self.width_window)
        else:
            self.window = None

        self.snake = Snake("Peter", "Blue")
        
        # This also sets the methods board object
        self.drawBoard()
            
        self.id = 0

        # A tuple of the current food's location
        self.current_food = [0, 0]
        self.current_food = self.placeFood()
        
        # This describes the hidden layer's architecture
        hiddenArch = [10, 6]
        self.neural_network = Neural_Network( 8, hiddenArch, 4  )
        
        ######## GRAPHICS FIELDS #############
        # Store fields here to make copying the NN easier later 
        # Store ratio to describe how much space the NN gets 
        self.allPoints = self.draw_NN()
        ######################################
    
    # This method will draw the neural network to the given
    # graphics window. If the window is None, then do nothing
    def draw_NN(self):

        if ( self.window == None):
            return None

        allCircles = []
        currentLayer = []

        center_x = (self.width_window * 0.75) + (0.5 * self.width_window * 0.24)

        start_y = self.length_window * 0.03

        neuronColor = "blue"
        neuronRadius = 6

        # We want the widest layer to just fill up the width
        widest = 8
        for i in range(len(self.neural_network.allWeights) ):
            if ( ( len(self.neural_network.allWeights[i]) > widest) ):
                    widest = len(self.neural_network.allWeights[i] )

        increment_x = (self.width_window * 0.25) / (float( widest + 1 ) )

        nextRow = start_y
        lastColumn = center_x

        # Create input and hidden neurons 
        for i in range(len(self.neural_network.allWeights) ):

            currentLayer = []
            # Draw the center(s) neurons
            length = -1
            priorOffset = -1
            numNeurons = len(self.neural_network.allWeights[i] )
            if ( ( (numNeurons % 2) == 0) ):
                # Draw two in the center
                priorOffset = (increment_x / 2.0)
                length = int( ( numNeurons - 2) / 2 )
                nextPoint = None

                nextPoint1 = Point( center_x + (increment_x / 2.0) , nextRow  )

                nextPoint2 = Point( center_x - (increment_x / 2.0) , nextRow  )

                # Draw the first
                nextCircle = Circle(nextPoint1, neuronRadius)
                nextCircle.setFill(neuronColor)
                currentLayer.append(nextCircle)
                nextCircle.draw(self.window)
    
                # Draw the second
                nextCircle = Circle(nextPoint2, neuronRadius)
                nextCircle.setFill(neuronColor)
                currentLayer.append(nextCircle)
                nextCircle.draw(self.window)
            
            elif( (numNeurons % 2) != 0):
                length = int( ( len(self.neural_network.allWeights[i] - 1) ) / 2)
                priorOffest = 0.0
                # Draw just one in the center
                nextPoint = Point( center_x, nextRow)
                nextCircle = Circle(nextPoint, neuronRadius)
                nextCircle.setFill(neuronColor)
                currentLayer.append(nextCircle)
                nextCircle.draw(self.window)


            # Draw the rest of the neurons
            for j in range( length ):

                # Draw the first
                nextPoint = Point( center_x + increment_x + priorOffset, nextRow  )
                nextCircle = Circle(nextPoint, neuronRadius)
                nextCircle.setFill(neuronColor)
                currentLayer.append(nextCircle)
                nextCircle.draw(self.window)
                # Draw the second
                nextPoint = Point( center_x - (increment_x + priorOffset ) , nextRow  )
                nextCircle = Circle(nextPoint, neuronRadius)
                nextCircle.setFill(neuronColor)
                currentLayer.append(nextCircle)
                nextCircle.draw(self.window)
                priorOffset = increment_x + priorOffset

            nextRow = nextRow + 100

            # Put the currentLayer into the overall list
            allCircles.append(currentLayer)


        # Create the output neurons
        currentLayer = []
        # Draw the center(s) neurons
        length = -1
        priorOffset = -1
        numNeurons = 4
        # Draw two in the center
        priorOffset = (increment_x / 2.0)
        length = int( ( numNeurons - 2) / 2 )
        nextPoint = None

        nextPoint1 = Point( center_x + (increment_x / 2.0) , nextRow  )

        nextPoint2 = Point( center_x - (increment_x / 2.0) , nextRow  )

        # Draw the first
        nextCircle = Circle(nextPoint1, neuronRadius)
        nextCircle.setFill(neuronColor)
        currentLayer.append(nextCircle)
        nextCircle.draw(self.window)
        
        # Draw the second
        nextPoint = Point( center_x - (increment_x + priorOffset ) , nextRow  )
        nextCircle = Circle(nextPoint, neuronRadius)
        nextCircle.setFill(neuronColor)
        currentLayer.append(nextCircle)
        nextCircle.draw(self.window)
        
        priorOffset =  increment_x / 2.0 # increment_x + priorOffset

        # Draw the rest of the neurons
        for j in range( length ):

            # Draw the first
            nextPoint = Point( center_x + increment_x + priorOffset, nextRow  )
            nextCircle = Circle(nextPoint, neuronRadius)
            nextCircle.setFill(neuronColor)
            currentLayer.append(nextCircle)
            nextCircle.draw(self.window)
            # Draw the second
            nextPoint = Point( center_x - (increment_x - priorOffset ) , nextRow  )
            nextCircle = Circle(nextPoint, neuronRadius)
            nextCircle.setFill(neuronColor)
            currentLayer.append(nextCircle)
            nextCircle.draw(self.window)
            priorOffset = increment_x + priorOffset

        allCircles.append(currentLayer)
        nextRow = nextRow + 50

        # Draw the weights
        allLines = []
        for i in range(len( allCircles ) - 1 ):
            for j in range(len( allCircles[i]  ) ):

                for k in range( len( allCircles[i + 1] ) ):

                    nextLine = Line( allCircles[i][j].getCenter(), allCircles[i + 1][k].getCenter()  )
                    nextLine.setFill( color_rgb( int( 150 - abs( self.neural_network.allWeights[i][j][k] * 149 ) ), 0, 0)  )
                    nextLine.setWidth(1)
                    nextLine.draw(self.window)
                    allLines.append(nextLine)

        # Return the list of points
        return allCircles

    # This method returns the normalized distance to the wall in the direction we are moving
    # (x,y) is the proposed, new location in the grid
    # (priorX, priorY) is the location we moved from 
    def distance_wall(self, x, y, priorX, priorY):

        maxLength = maxLength = np.sqrt( ( (self.width_grid)**2) + ( (self.length_grid)**2) )

        # Check if we are on the diagonal
        deltaX = int(x - priorX)
        deltaY = int(y - priorY)
        distance = 0.0
        if ( (deltaX == 1) and (deltaY == 1) ):
            # Distance to the bottom right corner   
            distance = np.sqrt( ( (self.width_grid - x)**2) + ( (self.length_grid - y)**2) )  
            return distance / maxLength

        if ( (deltaX == -1) and (deltaY == 1) ):
            # Distance to the bottom left corner
            distance = np.sqrt( ( x**2) + ( (self.length_grid - y)**2) )
            return distance / maxLength

        if ( (deltaX == 1) and (deltaY == -1) ):
            # Distance to the right top corner
            distance = np.sqrt( ( (self.width_grid)**2) + ( (self.length_grid)**2) )
            return distance / maxLength

        if ( (deltaX == -1) and (deltaY == -1) ):
            # Distance to the left top corner
            distance = np.sqrt( ( x**2) + ( y**2) )
            return distance / maxLength

        # Check the single dimension movements
        if ( (x - priorX == 1) ):
            maxLength = float(self.width_grid) 
        elif( y - priorY == 1  ):
             maxLength = float(1 * self.length_grid)

        # Check that the (x, y) pair is legal
        if ( (x < 0) or (y < 0) ):
             return 0.0   
        elif ( (x >= self.width_grid) or (y >= self.length_grid) ):
            # EXPLAIN THIS
            return 0.0
         
        # Normal 4-neighbor cases 
        if ( ( int(x - priorX) != 0) ):
            # Moving to the right/left
            return (maxLength - x) / maxLength
        else:
            return (maxLength - y) / maxLength 

         
    # This method computes the distance from the head of the body to the tail
    # in the direction we are moving in
    # Return 0 if (x, y) goes out of bounds or collides with oneself
    # Return 1 if (x,y) stays in bound and does not collide with onself
    # (x,y) is the new loaction we are moving to 
    # Return 0 for bad
    # Return 1 for good
    def distance_body(self, x, y):
        
        maxLength = np.sqrt( ( (self.width_grid)**2) + ( (self.length_grid)**2) )
        # Check that the (x, y) pair is legal    
        if ( (x < 0) or (y < 0) ):
            return 0.0    
        
        elif ( (x >= self.width_grid) or (y >= self.length_grid) ):
            return 0.0
         
        # Traverse the x-dimension forwards    
        if ( self.snake.isBody(x, y) == True ):
            return 0.0
        else:
            return 1.0

    # This method returns the normalized distance to the food
    # in the direction we are moving
    # (x,y) is the proposed, new location in the grid
    # (priorX, priorY) is the location we moved from
    # Return 1 if moving in that direction will hit the wall
    # Return 0 if moving in that direction will not hit the wall
    def distance_food(self, x, y, priorX, priorY):
           
        # Check the 8 neighbor diagonal cases first
        deltaX = int(x - priorX)
        deltaY = int(y - priorY)
        distance = 0.0
        
        # distance = 1 if the food is in that direction
        # distance = 0 if the food is not in that direction

        if ( (deltaX == 1) and (deltaY == 1) ):
            
            if ( ( abs(x - self.current_food[0] ) == abs( y - self.current_food[1]  )  ) ):
                return 1.0
            else:
                return 0.0

        elif ( (deltaX == 1) and (deltaY == -1) ):
            if ( ( abs(x - self.current_food[0] ) == abs( y - self.current_food[1]  )  ) ):
                return  1.0
            else:
                return 0.0

        elif ( (deltaX == -1) and (deltaY == 1) ):
            if ( ( abs(x - self.current_food[0] ) == abs( y - self.current_food[1]  )  ) ):
                return 1.0
            else:
                return 0.0

        elif ( (deltaX == -1) and (deltaY == -1) ):
            if ( abs( (x - self.current_food[0] ) == abs( y - self.current_food[1]  )  ) ):
                return 1.0
            else:
                return 0.0

        maxLength = self.width_grid
        # Check that the (x,y) pair is legal
        if ( (x < 0) or (y < 0) or (x >= self.length_grid) or (y >= self.width_grid) ):
            return 0.0
        
        if ( (deltaX != 0) and ( abs(x - self.current_food[0]) < abs(priorX - self.current_food[0])  )  ):
            return 1.0  #abs(x - self.current_food[0])
        
        elif ( (deltaY != 0) and (  abs(y - self.current_food[1]) < abs(priorY - self.current_food[1])  )  ):
            return 1.0  # abs(y - self.current_food[1])
        else:
            return 0.0
        

    # This method generates the (x,y) pair of the given location's 8 neighbors
    # (x, y) is the current location's coordinates in the game's grid
    def generate_8_Neighbors(self, x, y):

        return [ [x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1], [x + 1, y + 1], [x - 1, y - 1], [x - 1, y + 1], [x + 1, y - 1] ]

    # This method generates the (x,y) pair of the given location's 4 neighbors
    # (x, y) is the current location's coordinates in the game's grid
    def generate_4_Neighbors(self, x, y):

        return [ [x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1] ]

 
    # This method takes the game state and computes the in vector
    # that will go to the neural network
    # Input: (x,y) is the current location of the head in the game's grid 
    # Output: N x ? np.array
    def compute_In_Vector(self, x, y):
        
        numNeighbors = 8
        numStats = 1
        length = numNeighbors * numStats
        returnVector = np.zeros( (length, 1) )
        
        neighbors_list = self.generate_8_Neighbors(x, y) 
        # neighbors_list = self.generate_4_Neighbors(x, y)

        vectorIndex = 0
        [ [x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1], [x + 1, y + 1], [x - 1, y - 1], [x - 1, y + 1], [x + 1, y - 1] ]
        #forward_x = [True, False, False, False, True, False, False, True]
        #forward_y = [False, False, True, False, True, False, True, False]
        for i in range( len(neighbors_list) ):
            
            prior_x = self.snake.body_x[-1] 
            prior_y =  self.snake.body_y[-1]
            x = neighbors_list[i][0] 
            y = neighbors_list[i][1]
            
            returnVector[vectorIndex] =  self.distance_food( x, y, prior_x, prior_y ) 

            vectorIndex = vectorIndex + numStats
        
        return returnVector
        
    
    # This method randomnly places the food in the grid
    def placeFood(self):
        
        priorX = self.current_food[0]
        priorY = self.current_food[1]

        # Place the food randomnly
        # Check that the spot is not occupied by the current snake
        
        while (True):
            new_x = int( random() * len(self.board[0] ) ) 
            new_y = int( random() * len(self.board ) )
        
            # Check that 
            for i in range(len( self.snake.body_x ) ):
                
                if ( (new_x == self.snake.body_x[i] ) and (new_y == self.snake.body_y[i] )  ):
                    continue
                if ( (priorX == new_x) or ( priorY == new_y) ):
                    continue

            # Always place the food in the same spot to start
            if( self.id == 0):
                 new_x = 4 
                 new_y = 9 
                 self.id = 1
                 return [new_x, new_y]
            
            return [new_x, new_y]

    
    # Draw the board to the screen
    def drawBoard(self):
        
        if (self.window != None ):
            self.window.setBackground("black") 
        
        self.rectangles = []
        
        # Store the list of points needed to draw the board
        points = [] 
        
        for i in range( self.length_grid ):
            
            current_row_rectangles = []
                
            Point_1 = Point( 0 , 0 ) 
            for j in range( self.width_grid ):
                
                current_row = (0.75) * float(self.length_window) / float(self.length_grid)
                current_column = (0.75) * float(self.width_window) / float(self.width_grid ) 
                
                Point_1 = Point( current_row * j , current_column * i )  
                Point_2 = Point( current_row * (j + 1) , current_column * (i + 1) )
                
                current_row_rectangles.append( Rectangle(Point_1, Point_2 ) )


            # Append the next row to the array
            self.rectangles.append(current_row_rectangles)

        
        # Traverse the list of the rectangles to change their fill colors
        if ( self.window != None ):
            for i in  range( len( self.rectangles  ) ):
                for j in range( len( self.rectangles[i] ) ):
                    
                    self.rectangles[i][j].draw(self.window)
                    self.rectangles[i][j].setFill("black")
        

        self.board = self.rectangles

        # Draw the snake's body
        x = self.snake.body_x[0]
        y = self.snake.body_y[0]
        if ( self.window != None ):
            self.rectangles[y][x].setFill(self.snake.color)
            # Draw the name and the score
            self.message = Text( Point(50, 50), "Score: " + str(self.score) )
            self.message.setSize(18)
            self.message.setTextColor("white")
            self.message.draw(self.window)
            
            # Draw the food
            try:
                self.rectangles[ self.current_food[1] ][ self.current_food[0]  ].setFill("purple")
            except:
                pass

    
    # This moves the game from one state to the next
    # Command is either "left", "right", "up", "down"
    def nextState(self, command):
        
        self.moveNumber = self.moveNumber + 1
        if ( self.moveNumber > 1000):
            self.isOver = True

        # Re-draw the food
        if ( self.window != None ):
            self.rectangles[ self.current_food[1] ][ self.current_food[0]  ].setFill("purple")

        # Update the internal data structures 
        newState_x = self.snake.body_x.copy() 
        newState_y = self.snake.body_y.copy()
        

        if ( command == "left" ):
            newState_x = np.append( newState_x,  newState_x[ -1] - 1 )
            newState_y = np.append( newState_y,  newState_y[ -1]   )
        
        elif ( command == "right" ):
            newState_x = np.append( newState_x,  newState_x[ -1] + 1 )
            newState_y = np.append( newState_y,  newState_y[ -1]   )    
        
        elif ( command == "up" ):
            newState_x = np.append( newState_x,  newState_x[ -1]    )
            newState_y = np.append( newState_y,  newState_y[ -1] + 1)

        elif ( command == "down" ):
            newState_x = np.append( newState_x,  newState_x[-1]  )
            newState_y = np.append( newState_y,  newState_y[-1] - 1 )
        

        # Check if the food and the head collided
        head_x = newState_x[-1]
        head_y = newState_y[-1]
        if ( (self.current_food[0] == head_x ) and (self.current_food[1] == head_y )   ):
             
            self.score = self.score + 1.0

            # Draw the name and the score
            if ( self.window != None ):
                self.message.undraw()
                self.message = Text( Point(60, 30), "Score: " + str(self.score) )
                self.message.setSize(18)
                self.message.setTextColor("white")
                self.message.draw(self.window)
            

            # Add an item to the snake's body 
            # FIX ME - am I appending in the wrong order?
            # The head is at the end of the list
            self.snake.body_x = np.append(self.snake.body_x, self.current_food[0]  )  
            self.snake.body_y = np.append(self.snake.body_y, self.current_food[1]  )
             
            # Draw the new square
            x = self.snake.body_x[-1]
            y = self.snake.body_y[-1]
            
            if ( self.window != None ):
                self.rectangles[y][x].setFill("white") 

            # Place new food
            self.current_food = self.placeFood()

            return


        # This is the caboose of the snake and will be deleted
        # We delete by changing the fill to the background color
        delete_x = newState_x[0]
        delete_y = newState_y[0]
        if ( self.window != None ):
            self.rectangles[delete_y][delete_x].setFill("black")

        newState_x = np.delete(newState_x, 0)
        newState_y = np.delete(newState_y, 0)
        
        # Change the snake's data structures 
        self.snake.body_x = newState_x.copy()
        self.snake.body_y = newState_y.copy()

        # Traverse the list of the rectangles to change their fill colors
        if ( self.window != None ):
            for i in range( len( newState_x  ) ):
             
                x = newState_x[i]
                y = newState_y[i]
                self.rectangles[y][x].setFill("white")

    # Let the neural net generate a move
    # Return "left" or "right" or "up" or "down"
    def generate_NN_Move(self):

        x = self.snake.body_x[ -1 ]
        y = self.snake.body_y[ -1 ]
        
        inputVector = self.compute_In_Vector(x, y)
              
        outputVector = self.neural_network.forwardProp(inputVector)

        for i in range(4):
            move = np.argmax(outputVector.copy() )
            # Check that the move is legal
            if ( self.snake.isLegal( move, x, y, self.length_grid, self.width_grid ) == False ):
                
                # The game is over
                self.isOver = True
            else:
                break
        
        if ( np.sum(outputVector[0] ) == -4):
            print("NO MOVE FOUND")
            print("(x, y) is ")
            print( str(x) + str(", ") + str(y) )
            self.isOver = True

        if ( move == 0 ):
            self.neural_network.left = True
            move = "left"

        elif ( move == 1 ):
            self.neural_network.right = True
            move = "right"

        elif ( move == 2):
            self.neural_network.down = True
            move = "down"

        elif ( move == 3 ):
            self.neural_network.up = True
            move = "up"

        return move
        


