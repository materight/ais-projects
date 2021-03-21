from pylab import *
import sys
from inspyred import benchmarks

import cma_es
import es
from inspyred_utils import NumpyRandomWrapper

display = True # Plot initial and final populations

"""
-------------------------------------------------------------------------
Edit this part to do the exercises

"""

num_vars = 10

# parameters for CMA-ES
args = {}
args["max_generations"] = 100
args["sigma"] = 1.0 # default standard deviation

args["pop_size"] = 20 #mu
args["num_offspring"] = 100 #lambda

#args["problem_class"] = benchmarks.Sphere
args["problem_class"] = benchmarks.Rosenbrock
#args["problem_class"] = benchmarks.Rastrigin

"""
-------------------------------------------------------------------------
"""

args["fig_title"] = 'CMA-ES'

if __name__ == "__main__":
    
    if len(sys.argv) > 1 :
        rng = NumpyRandomWrapper(int(sys.argv[1]))
    else :
        rng = NumpyRandomWrapper()
        
    # Run CMA-ES
    best_individual, best_fitness = cma_es.run(rng,num_vars=num_vars,
                                           display=display,use_log_scale=True,
                                           **args)
    
    # Display the results
    print("Best Individual:", best_individual)
    print("Best Fitness:", best_fitness)
    
    if display :
        ioff()
        show()
