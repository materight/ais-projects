# -*- coding: utf-8 -*-

from random import Random
from time import time
import math
import inspyred

import plot_utils

from matplotlib import *
from pylab import *

from matplotlib import collections  as mc

def readFileAsMatrix(file):
    with open(file) as f:
        lines = f.read().splitlines()
        matrix = []
        for line in lines:
            row = []
            for value in line.split():
                row.append(float(value))
            matrix.append(row)
        return matrix

def plotSolution(points, distances, solution, title):
    fig = figure(title)
    ax = fig.add_subplot(111)
    ax.scatter(*zip(*points))
    
    for i,p in enumerate(points):
        ax.annotate(str(i), p)
    
    # draw all possible path segments
    lines = []
    for i, p in enumerate(points):
        for j, q in enumerate(points):
            if distances[i][j] > 0 and i > j:
                lines.append((points[i], points[j]))
    lc = mc.LineCollection(lines, linewidths=.1)
    ax.add_collection(lc)

    # draw the solution
    lines = []
    for i in arange(len(solution)-1):
        lines.append((points[solution[i]], points[solution[i+1]]))
    lines.append((points[solution[0]], points[solution[-1]]))
    lc = mc.LineCollection(lines, linewidths=1, color="r")
    ax.add_collection(lc)

    #ax.set_title(title)
    ax.autoscale()
    ax.margins(0.1)

def main(prng=None, display=False):    
    if prng is None:
        prng = Random()
        #prng.seed(time())

    """
    points = [(110.0, 225.0), (161.0, 280.0), (325.0, 554.0), (490.0, 285.0),
              (157.0, 443.0), (283.0, 379.0), (397.0, 566.0), (306.0, 360.0), 
              (343.0, 110.0), (552.0, 199.0)]
    distances = [[0 for _ in range(len(points))] for _ in range(len(points))]
    for i, p in enumerate(points):
        for j, q in enumerate(points):
            distances[i][j] = math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)
    """
    
    """
    datasets taken from:
        https://people.sc.fsu.edu/~jburkardt/datasets/tsp/tsp.html
        http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/index.html
    """
    #instance = "p01"
    instance = "bays29"
    #instance = "att48"
    points = readFileAsMatrix("datasets/tsp/" + instance + "_xy.txt")
    distances = readFileAsMatrix("datasets/tsp/" + instance + "_d.txt")
    
    print("Points:\n", points)
    print("Distances:\n", distances)
    
    # common parameters
    pop_size = 50
    max_generations = 20
    # ACS specific parameters
    evaporation_rate = 0.1
    learning_rate = 0.1
    # EA specific parameters
    tournament_size = 5
    num_elites = 1
    
    args = {}
    args["fig_title"] = "ACS"
    
    # run ACS
    problem = inspyred.benchmarks.TSP(distances)
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
    problem = inspyred.benchmarks.TSP(distances)
    ea = inspyred.ec.EvolutionaryComputation(prng)
    ea.observer = [plot_utils.plot_observer]
    ea.selector = inspyred.ec.selectors.tournament_selection
    ea.variator = [inspyred.ec.variators.partially_matched_crossover,
                   inspyred.ec.variators.inversion_mutation]
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
        for link in best_ACS.candidate:
            # each point is ((i, j), 1/distance_ij)
            indices.append(link.element[0])
        indices.append(best_ACS.candidate[-1].element[1])
        solution_ACS = indices
        
        solution_EA = best_EA.candidate

        print("Best Solution ACS: {0} - Distance: {1}".format(str(solution_ACS), 1/best_ACS.fitness))
        print("Best Solution EA : {0} - Distance: {1}".format(str(solution_EA), 1/best_EA.fitness))
        
        plotSolution(points, distances, solution_ACS, "ACS (best solution)")
        plotSolution(points, distances, solution_EA, "EA (best solution)")
        
        ioff()
        show()
            
if __name__ == "__main__":
    main(display=True)
