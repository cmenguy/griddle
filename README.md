# grid-optimizer &mdash; Complex optimization on 2-dimensional grids

grid-optimizer makes use of the [Simulated Annealing](http://en.wikipedia.org/wiki/Simulated_annealing) algorithm to optimize and arange grid connections from a state of complete chaos to an optimal state.

## Quicklinks
  - [Installation](#installation)
  - [Example](#example)
    - [Initial state](#initial-state)
    - [Final state](#final-state)
    - [Large grids](#large-grids)
  - [Analysis](#analysis)
    - [Influence of perturbation coefficient](#influence-of-perturbation-coefficient)
    - [Influence of cooling factor](#influence-of-cooling-factor)

## Installation

grid-optimizer is written in Python, tested against 2.7 and uses the following modules:
	- [pygame](http://www.pygame.org/) for graphics to represent grid connections
	- [pyplot](http://matplotlib.org/api/pyplot_api.html) for analysis of parameters

This is an iterative algorithm, and each cycle will transition the grid to a new state which can be viewed using the `pygame` interface.

The verbosity can be specified and has the following levels:
	- 0 will only print lines on `stdout` for each iteration.
	- 1 will display the state of the grid at the beginning and end of the algorithm.
	- 2 will display the state of the grid for every iteration - not recommended.

There are 2 important parameters that can be specified:
	- Tau is the initial perturbation coefficient - representing in the analogy to simulated annealing how high the temperature us. It's a probability so has to be between 0 and 1, and the bigger the value, the hotter the temperature.
	- Beta is the cooling factor, meaning after every iteration this will determine how much we decrease the temperature. A higher number will decrease the temperature more slowly.

For a complete list of all parameters available, you can use the help menu:

    $ ./simulated_annealing -h
    Usage: simulated_annealing [options]

	Options:
	  -h, --help            show this help message and exit
	  -s SIZE, --size=SIZE  size of the grid in format WxH
	  -t TAU, --tau=TAU     initial perturbation coefficient
	  -b BETA, --beta=BETA  cooling factor
	  -v VERBOSE, --verbose=VERBOSE
	                        verbose level
	  -n, --nograph         


## Example

### Initial State

With a verbose level of 1 or more, the initial state will be represented with `pygame`.
This shows the grid as a set of tiles, and various connections between each of the tiles created at random.

![chaotic grid](/data/chaos.png "Grid in initial state")

The goal is to minimize the total distance between each tile using the simulated annealing algorithm.

### Final State

Once the algorithm has converged, the grid will be in a state where the entropy in the system has been minimized with successive temperature decreases.
Here is an example of what a grid can look like after the algorithm is done:

![optimized grid](/data/order.png "Grid in final state")

Note that it is not guaranteed that the simulated annealing algorithm will find the global optima, as it could also be stuck in a local optima depending on the values of tau and beta chosen - more on that in the [analysis](#analysis) section.

### Large grids

You can also specify grids larger than 5x5 with the command line, and the algorithm should work the same way.
It is worth noting that as the grid size grows, the tree of probabilities grows as well, and so the algorithm is more likely to get stuck in a local minima, so it is important to decrease the temperature more slowly as you increase the size.

![big grid](/data/big-grid.png "Large grid in final state")

## Analysis

### Influence of perturbation coefficient

The perturbation coefficient is very important