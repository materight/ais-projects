from pylab import *
import sys
from inspyred import ec, benchmarks
import plot_utils

import es
from inspyred_utils import NumpyRandomWrapper

sys.path.append('..')
from benchmark import run_benchmark

display = True # Plot initial and final populations

"""
-------------------------------------------------------------------------
Edit this part to do the exercises

"""

num_vars = 10

# parameters for the ES
args = {}
args["max_generations"] = 100
args["sigma"] = 1.0 # default standard deviation

args["pop_size"] = 20 # mu
args["num_offspring"] = 100 #lambda

args["strategy_mode"] = None
#args["strategy_mode"] = es.GLOBAL
#args["strategy_mode"] = es.INDIVIDUAL

args["mixing_number"] = 1 #rho
#args["mixing_number"] = 5

#args["problem_class"] = benchmarks.Sphere
args["problem_class"] = benchmarks.Rosenbrock
#args["problem_class"] = benchmarks.Rastrigin

"""
-------------------------------------------------------------------------
"""

args["fig_title"] = 'ES'

def run(args, show=True):
    
    args["max_generations"] = 10000 // args["num_offspring"] 

    if len(sys.argv) > 1 :
        rng = NumpyRandomWrapper(int(sys.argv[1]))
    else :
        rng = NumpyRandomWrapper()

    # Run the ES
    best_individual, best_fitness, final_pop = es.run_es(rng,num_vars=num_vars,
                                           display=display,use_log_scale=True,
                                           **args)
    
    # Display the results
    if show:
        print("Best Individual:", best_individual)
        print("Best Fitness:", best_fitness)
    
    if display:
        ioff()
        if show: show()

    return {'best_fitness': best_fitness}

results = run_benchmark(run, 'results/es1', args, {
        'num_offspring': [100],
        'mixing_number': [1, 2, 5],
        'strategy_mode': [None, es.GLOBAL, es.INDIVIDUAL]
    }, 
    problems=[benchmarks.Rosenbrock], # benchmarks.Sphere, benchmarks.Rastrigin 
    combine=True)