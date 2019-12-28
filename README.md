# How To Run My Code
Clone my repo and run ```python3 Snake_Game.py```. No other software should need to be installed

# Description
I used a neural network and a genetic algorithm to learn how to play snake. First I programmed a simple snake game, then I implemnted the algorithms to have the agent learn how to play the game.

The program supports aribtrary graph structures. One could make the network as deep as one wanted to. One can also choose how wide to make each hidden layer. As of now, one can simply edit the Game.py file and change the arguments used to construct the neural network. This will change the network's structure. 

The input vector is an 8 vector. There is one value for each of the 8 neighbors of the current location of the head. If moving to the given location reduces the distance to the food then the entry is 1. If it increases the distance or stays the same, then the entry is a 0. Ideally, I would add, for each 8 neighbors, another piece of information describing where the body is. I experimented heavily with this and could not seem to learn a set of weights that explicity avoided its own body. It may be that I simply need to train longer or use a diffrent graph structure.

# Results
I found good results when I used two hidden layers. One of width 10 and the next of width 6. So the network is 8 x 10 x 6 x 4. I used the rectified linear unit on the input and hidden units and the softmax function on the output neurons.

There are four output neurons. Each one represents one of the 4 legal moves for the snake. Whichever neuron is maximally fired, its corresponding direction will be the direction we move in.  

The Genetic Algorithm 
The crossover function simply averages each matrix of weights from two of the chosen neural networks. Then, a small bit of noise is added to this average. 

A good weight set is learned in 3-4 generations.

The video of the trained neural network playing snake can be found at


[![](http://img.youtube.com/vi/6AC9wYStHTM/0.jpg)](http://www.youtube.com/watch?v=6AC9wYStHTM "Neural Network Learns to Play Snake")

