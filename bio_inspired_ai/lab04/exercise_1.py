# -*- coding: utf-8 -*-

from pylab import *

from inspyred import benchmarks
from inspyred.ec import Bounder
from inspyred.ec.emo import Pareto
from inspyred_utils import NumpyRandomWrapper

import sys
import inspyred_utils 
import multi_objective

"""
-------------------------------------------------------------------------
Edit this part to do the exercises

Try different methods of combining multiple objectives into a single objective
    (1) additive
    (2) multiplicative

Try using different weights for combining the objectives in both cases, and try
this on different fitness functions.

"""

display = True# Plot initial and final populations
num_vars = 19 + 2 # set 3 for Kursawe, set to 19+num_objs for DTLZ7
num_objs = 2 # used only for DTLZ7

# parameters for the GA
args = {}
args["pop_size"] = 50
args["max_generations"] = 100

# make sure that this array has the same size as num_objs
#args["fitness_weights"] = [0.5, 0.5]
args["fitness_weights"] = [1, 1]

#problem = benchmarks.Kursawe(num_vars) # set num_vars = 3
problem = benchmarks.DTLZ7(num_vars, num_objs) # set num_objs = 3 and num_vars = 19+num_objs

"""
-------------------------------------------------------------------------
"""

args["fig_title"] = 'GA'

if __name__ == "__main__" :
    if len(sys.argv) > 1 :
        rng = NumpyRandomWrapper(int(sys.argv[1]))
    else :
        rng = NumpyRandomWrapper()
    
    best_individual, best_fitness = multi_objective.run_ga(rng, problem, 
                                        display=display, num_vars=num_vars, 
                                        **args)
    
    print("Best Individual", best_individual)
    print("Objectives Fitness", problem(*best_individual))
    print("Tot Fitness", best_fitness)
    
    if display :    
        ioff()
        show()
