from pylab import *
import sys
from inspyred import ec, benchmarks
import plot_utils

import es
from inspyred_utils import NumpyRandomWrapper

sys.path.append('..')
from benchmark import run_benchmark

display = False # Plot initial and final populations

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
#args["mixing_number"] = 5 #rho

strategy_modes = [None, es.GLOBAL, es.INDIVIDUAL]

args["mixing_number"] = 1 #rho

#args["problem_class"] = benchmarks.Sphere
args["problem_class"] = benchmarks.Rosenbrock
#args["problem_class"] = benchmarks.Rastrigin

num_runs = 10 # Number of runs to be done for each condition

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
    
    # Run the ES *num_runs* times for each strategy mode and record results     
    results = []
    for strategy_mode in strategy_modes :
        if show:
            print("Trying strategy ", str(strategy_mode))
        args["strategy_mode"] = strategy_mode
        results.append([es.run_es(rng,num_vars=num_vars, display=display,**args)
                        for _ in range(num_runs)]) 
        
    best_fitnesses = [[run_result[1] for run_result in runs] 
                      for runs in results]

    # Boxplot comparing the best fitnesses
    fig = figure('ES (best fitness)')
    ax = fig.add_subplot(1,1,1)
    ax.boxplot(best_fitnesses)  
    ax.set_yscale('log')
    ax.set_xticklabels(strategy_modes)
    #ax.set_xticklabels( map(lambda s: str(s), strategy_modes ) )
    ax.set_xlabel('Strategy')
    ax.set_ylabel('Fitness')
    ioff()
    if show: 
        show()

    return { f'best_fitness_{mode}': max(best_fitnesses[i]) for i, mode in enumerate(strategy_modes)}

results = run_benchmark(run, 'results/es2', args, {
        'mixing_number': [1, 5, 10],
        'num_offspring': [20, 100, 160],
    }, 
    problems=[benchmarks.Rosenbrock, benchmarks.Sphere, benchmarks.Rastrigin],
    combine=True)