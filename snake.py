import numpy as np

# This class implements the snake object
class Snake:

    # Constructor 
    # Describe the input args here
    def __init__(self, name, color):

        self.color = color
        self.name = name 

        self.body_x = np.array( [10] ) 
        self.body_y = np.array( [10] )
    
    # This method checks if a given (x,y) location on the board
    # is pat of the snake's body
    # Return True if the (x,y) is part of the body 
    def isBody(self, x, y):
        
        # Traverse the snake's body to check for collisions
        for i in range(len( self.body_x ) ):
            
            if ( ( self.body_x[i] == x) and ( self.body_y[i] == y) ):
                return True
         
        return False

    # This method checks to see if a move is legal
    # Move is a string {left, right, up, down}
    # (x,y) is the curret x,y of the snake's body
    # Return Value: True if the move is legal frmo 
    def isLegal(self, move, x, y, maxX, maxY):
        
        # Check for error conditions
        if ( (move < 0) or (move > 4) ):
            print("Error: The input is out of range")

        newX = x
        newY = y
        if ( move == 0 ):
            move = "left"
            newX = x - 1

        elif ( move == 1 ):
            move = "right"
            newX = x + 1

        elif ( move == 2):
            move = "down"
            newY = y - 1

        elif ( move == 3 ):
            move = "up"
            newY = y + 1
        
        if ( (newX >= maxX) or (newY >= maxY) or (newX < 0) or (newY < 0) ):
            return False

        if ( (self.isBody(newX, newY) == True) ):
            return False
        else:
            return True
        
        

