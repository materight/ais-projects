from pylab import *
from random import Random
from ga import run_ga
import sys

"""    
-------------------------------------------------------------------------
Edit this part to do the exercises
"""

num_vars = 10 # Number of dimensions of the search space
std_dev = 0.1 # Standard deviation of the Gaussian mutations
max_generations = 200 # Number of generations of the GA

# parameters for the GA
args = {}
args["crossover_rate"] = 0 # Crossover fraction
args["tournament_size"] = 2
args["mutation_rate"] = 1.0 # fraction of loci to perform mutation on
args["num_elites"] = 1 # number of elite individuals to maintain in each gen
args["pop_size"] = 20
args["pop_init_range"] = [-10, 10] # Range for the initial population
display = True # Plot initial and final populations

"""
-------------------------------------------------------------------------
"""

args["fig_title"] = 'GA'

if __name__ == "__main__":
    if len(sys.argv) > 1 :
        rng = Random(int(sys.argv[1]))
    else :
        rng = Random()
        
    # Run the GA
    best_individual, best_fitness, final_pop = run_ga(rng, num_vars=num_vars,
                                                      max_generations=max_generations,
                                                      display=display,
                                                      gaussian_stdev=std_dev,**args)
    
    # Display the results
    print("Best Individual:", best_individual)
    print("Best Fitness:", best_fitness)
    # The distance from the optimum in the N-dimensional space
    print("Distance from Global Optimum", sqrt(sum(array(best_individual) ** 2)))
    if display :
        ioff()
        show()
