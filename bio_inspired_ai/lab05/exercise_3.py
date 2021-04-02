# -*- coding: utf-8 -*-

from pylab import *
import sys
from inspyred import ec
import plot_utils

import constrained_benchmarks

import es
from inspyred_utils import NumpyRandomWrapper

"""
-------------------------------------------------------------------------
Edit this part to do the exercises
"""

# parameters for the ES
args = {}
args["max_generations"] = 100 # Number of generations of the ES
args["pop_size"] = 20 # mu
args["num_offspring"] = 100 #lambda
args["sigma"] = 1.0 # default standard deviation
args["strategy_mode"] = None # es.GLOBAL, es.INDIVIDUAL
args["mixing_number"] = 1 #rho

args["problem_class"] = constrained_benchmarks.RosenbrockCubicLine
#args["problem_class"] = constrained_benchmarks.RosenbrockDisk
#args["problem_class"] = constrained_benchmarks.MishraBirdConstrained
#args["problem_class"] = constrained_benchmarks.Townsend
#args["problem_class"] = constrained_benchmarks.Simionescu
#args["problem_class"] = constrained_benchmarks.SphereCircle
#args["problem_class"] = constrained_benchmarks.SphereConstrained

"""
-------------------------------------------------------------------------
"""

display = True # Plot initial and final populations

args["fig_title"] = 'ES'

if __name__ == "__main__":
    
    if len(sys.argv) > 1 :
        rng = NumpyRandomWrapper(int(sys.argv[1]))
    else :
        rng = NumpyRandomWrapper()
        
    # Run the ES
    best_individual, best_fitness, final_pop = es.run_es(rng,num_vars=2,
                                           display=display,use_log_scale=True,
                                           **args)
    
    # Display the results
    print("Best Individual:", best_individual)
    print("Best Fitness:", best_fitness)
    
    function = args["problem_class"](2).printSolution(best_individual)
    
    if display :
        
        if args["problem_class"] == constrained_benchmarks.SphereCircle:
            x = []
            y = []
            c = []
            final_pop.sort()
            num_feasible = len([p for p in final_pop if p.fitness >= 0])
            feasible_count = 0
            for i, p in enumerate(final_pop):
                x.append(p.candidate[0])
                y.append(p.candidate[1])
                if i == len(final_pop) - 1:
                    c.append('r')
                elif p.fitness < 0:
                    c.append('0.98')
                else:
                    c.append(str(1 - feasible_count / float(num_feasible)))
                    feasible_count += 1
            angles = linspace(0, 2*pi, 100)
            figure(str(args["problem_class"]))
            lower_bound_1 = constrained_benchmarks.SphereCircle(2).bounder.lower_bound[0]
            lower_bound_2 = constrained_benchmarks.SphereCircle(2).bounder.lower_bound[0]
            upper_bound_1 = constrained_benchmarks.SphereCircle(2).bounder.upper_bound[0]
            upper_bound_2 = constrained_benchmarks.SphereCircle(2).bounder.upper_bound[0]
            plot(cos(angles), sin(angles), color='b')
            xlim(lower_bound_1, upper_bound_1)
            ylim(lower_bound_2, upper_bound_2)
            axes().set_aspect('equal')
            scatter(x, y, color=c)
        
        ioff()
        show()
