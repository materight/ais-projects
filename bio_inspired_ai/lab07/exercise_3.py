# -*- coding: utf-8 -*-

from random import Random
from time import time
import math
import inspyred

import plot_utils

from matplotlib import *
from pylab import *

def readFileAsList(file):
    with open(file) as f:
        lines = f.read().splitlines()
        n = len(lines)
        array = np.empty(n,dtype=np.uint32)
        for i in range(n):
            array[i] = int(lines[i])
        return array

def main(prng=None, display=False):    
    if prng is None:
        prng = Random()
        #prng.seed(time()) 

    """
    items = [(7,369), (10,346), (11,322), (10,347), (12,348), (13,383),
             (8,347), (11,364), (8,340), (8,324), (13,365), (12,314), 
             (13,306), (13,394), (7,326), (11,310), (9,400), (13,339), 
             (5,381), (14,353), (6,383), (9,317), (6,349), (11,396), 
             (14,353), (9,322), (5,329), (5,386), (5,382), (4,369), 
             (6,304), (10,392), (8,390), (8,307), (10,318), (13,359), 
             (9,378), (8,376), (11,330), (9,331)]
    capacity = 15
    """

    # datasets taken from https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html
    #instance = "01"
    #instance = "02"
    #instance = "03"
    #nstance = "04"
    #instance = "05"
    #instance = "06"
    #instance = "07"
    instance = "08"
    capacity = readFileAsList("datasets/knapsack_01/p" + instance + "_c.txt")[0]
    weights =  readFileAsList("datasets/knapsack_01/p" + instance + "_w.txt")
    values =  readFileAsList("datasets/knapsack_01/p" + instance + "_p.txt")
    items = [(w,v) for w, v in zip(weights, values)]

    print("Items:\n", items)
    print("Capacity:\n", capacity)

    # common parameters
    pop_size = 50
    max_generations = 20
    duplicates = True
    # ACS specific parameters
    evaporation_rate = 0.1
    learning_rate = 0.1
    # EA specific parameters
    tournament_size = 5
    num_elites = 1
    
    args = {}
    args["fig_title"] = "ACS"
    
    # run ACS
    problem = inspyred.benchmarks.Knapsack(capacity, items, duplicates=duplicates)
    ac = inspyred.swarm.ACS(prng, problem.components)
    ac.observer = [plot_utils.plot_observer]
    ac.terminator = inspyred.ec.terminators.generation_termination
    final_pop = ac.evolve(generator=problem.constructor,
                          evaluator=problem.evaluator,
                          bounder=problem.bounder,
                          maximize=problem.maximize,
                          pop_size=pop_size,
                          max_generations=max_generations,
                          evaporation_rate=evaporation_rate,
                          learning_rate=learning_rate,**args)
    best_ACS = max(ac.archive)
    
    args["fig_title"] = "EA"
    
    # run EA
    problem = inspyred.benchmarks.Knapsack(capacity, items, duplicates=duplicates)
    ea = inspyred.ec.EvolutionaryComputation(prng)
    ea.observer = [plot_utils.plot_observer]
    ea.selector = inspyred.ec.selectors.tournament_selection
    ea.variator = [inspyred.ec.variators.uniform_crossover,
                   inspyred.ec.variators.gaussian_mutation]
    ea.replacer = inspyred.ec.replacers.generational_replacement
    ea.terminator = inspyred.ec.terminators.generation_termination
    final_pop = ea.evolve(generator=problem.generator,
                          evaluator=problem.evaluator,
                          bounder=problem.bounder,
                          maximize=problem.maximize,
                          pop_size=pop_size,
                          max_generations=max_generations,
                          num_selected=pop_size,
                          tournament_size=tournament_size,
                          num_elites=num_elites,**args)
    best_EA = max(ea.population)
    
    if display:
        
        indices = []
        for item in best_ACS.candidate:
            # each item is (element, value)
            index = items.index((item.element, item.value))
            indices.append(index)
        solution_ACS = np.zeros(len(items),dtype=np.uint16)
        for i in indices:
            solution_ACS[i] += 1
        solution_ACS = solution_ACS.tolist()
        
        solution_EA = best_EA.candidate
        
        print("Best Solution ACS: {0} - Value: {1}".format(str(solution_ACS), best_ACS.fitness))
        print("Best Solution EA : {0} - Value: {1}".format(str(solution_EA), best_EA.fitness))

        ioff()
        show()
            
if __name__ == "__main__":
    main(display=True)
