# -*- coding: utf-8 -*-

from pylab import *

from inspyred import benchmarks
from inspyred.ec import Bounder
from inspyred.ec.emo import Pareto
from inspyred_utils import NumpyRandomWrapper

import sys
import inspyred_utils
import multi_objective

class MyBenchmark(benchmarks.Benchmark):
    
    def __init__(self, dimensions=2, objectives=[benchmarks.Sphere]):
        benchmarks.Benchmark.__init__(self, dimensions, len(objectives))
        self.bounder = Bounder([-5.0] * self.dimensions, [5.0] * self.dimensions)
        self.maximize = False
        self.evaluators = [cls(dimensions).evaluator for cls in objectives]
    
    def generator(self, random, args):
        return [random.uniform(-5.0, 5.0) for _ in range(self.dimensions)]
        
    def evaluator(self, candidates, args):
        fitness = [evaluator(candidates, args) for evaluator in self.evaluators]
        return map(Pareto, zip(*fitness))
    
""" 
-------------------------------------------------------------------------
Edit this part to do the exercises

"""

display = True# Plot initial and final populations
num_vars = 2+19 # set 3 for Kursawe, set to 19+num_objs for DTLZ7
num_objs = 2 # used only for DTLZ7

# parameters for NSGA-2
args = {}
args["pop_size"] = 50
args["max_generations"] = 100

#problem = benchmarks.Kursawe(num_vars) # set num_vars = 3
problem = benchmarks.DTLZ7(num_vars,num_objs) # set num_objs = 3 and num_vars = 19+num_objs

#problem = MyBenchmark(num_vars, [benchmarks.Rastrigin, benchmarks.Schwefel] )
#problem = MyBenchmark(num_vars, [benchmarks.Sphere, benchmarks.Rastrigin, benchmarks.Schwefel] )

"""
-------------------------------------------------------------------------
"""

args["fig_title"] = 'NSGA-2'
    
if __name__ == "__main__" :
    if len(sys.argv) > 1 :
        rng = NumpyRandomWrapper(int(sys.argv[1]))
    else :
        rng = NumpyRandomWrapper()
    
    final_pop, final_pop_fitnesses = multi_objective.run_nsga2(rng, problem,
                                        display=display, num_vars=num_vars,
                                        **args)
    
    print("Final Population\n", final_pop)
    print()
    print("Final Population Fitnesses\n", final_pop_fitnesses)
    
    ioff()
    show()
