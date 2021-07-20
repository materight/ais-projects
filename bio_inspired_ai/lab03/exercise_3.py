from pylab import *
import sys
from inspyred import benchmarks

import cma_es
import es
from inspyred_utils import NumpyRandomWrapper

sys.path.append('..')
from benchmark import run_benchmark

display = True # Plot initial and final populations

"""
-------------------------------------------------------------------------
Edit this part to do the exercises

"""

# parameters for CMA-ES
args = {}
args["num_vars"] = 10
args["max_generations"] = 100
args["sigma"] = 1.0 # default standard deviation

args["pop_size"] = 20 #mu
args["num_offspring"] = 20 #lambda

#args["problem_class"] = benchmarks.Sphere
args["problem_class"] = benchmarks.Rosenbrock
#args["problem_class"] = benchmarks.Rastrigin

"""
-------------------------------------------------------------------------
"""

args["fig_title"] = 'CMA-ES'

def run(args, show=True):
    
    args["max_generations"] = 10000 // args["num_offspring"] 

    if len(sys.argv) > 1 :
        rng = NumpyRandomWrapper(int(sys.argv[1]))
    else :
        rng = NumpyRandomWrapper()
        
    # Run CMA-ES
    best_individual, best_fitness = cma_es.run(rng,
                                           display=display,use_log_scale=True,
                                           **args)
    
    # Display the results
    if show:
        print("Best Individual:", best_individual)
        print("Best Fitness:", best_fitness)
    
    if display :
        ioff()
        if show: show()

    return {'best_fitness': best_fitness}

#run(args)

results = run_benchmark(run, 'results/es3', args, {
        'pop_size': [20],
        'num_offspring': [20],
        'num_vars': [10, 20, 30]
    }, 
    problems=[benchmarks.Rosenbrock, benchmarks.Sphere, benchmarks.Rastrigin],
    combine=True)