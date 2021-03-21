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

for num_vars in [10, 100]:
    for pop_size in [20, 100]:
        # parameters for CMA-ES
        args = {}
        args["max_generations"] = 100
        args["sigma"] = 1.0 # default standard deviation

        args["pop_size"] = pop_size #mu
        args["num_offspring"] = 100 #lambda

        #args["problem_class"] = benchmarks.Sphere
        args["problem_class"] = benchmarks.Rosenbrock
        #args["problem_class"] = benchmarks.Rastrigin

        """
        -------------------------------------------------------------------------
        """

        args["fig_title"] = f'CMA-ES vars={num_vars}, pop_size={pop_size}'

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
            print(f"vars={num_vars}, pop_size={pop_size}")
            #print("Best Individual:", best_individual)
            print(f"Best Fitness: {best_fitness}\n")
            
if display :
    ioff()
    show()
