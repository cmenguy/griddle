# griddle &mdash; Complex optimization on 2-dimensional grids

griddle makes use of the [Simulated Annealing](http://en.wikipedia.org/wiki/Simulated_annealing) algorithm to optimize and arange grid connections from a state of complete chaos to an optimal state.

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

griddle is written in Python, tested against 2.7 and uses the following modules:

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

The perturbation coefficient is very important as it controls the accept probability for a new random state. In other terms, it helps avoiding local minima by adding more diversity in the neighboring states, and so should be chosen wisely.
In physics term for the analogy to the simulated annealing process, it can be seen as the agitation : if the agitation is too low, we will end up with a local minima, if the agitation is too high, the algorithm will take a very long time to converge.

The following curves show the influence of tau on the energy of the system:

![tau energy](/data/tau-energy.png "Influence of Tau on the energy")

We can see that a higher tau leads to a better exploration of the solution space and is able to converge towards the global minima, while lower values of tau cause it to get trapped in a local minima.

### Influence of cooling factor

The cooling factor beta is also important because it determines how aggressively the system will cool down after each iteration. It is important not to cool down too quickly otherwise the solution space will not be explored fully, but also cooling down too slowly will be very slow to converge.

![beta energy](/data/beta-energy.png "Influence of Beta on the energy")
