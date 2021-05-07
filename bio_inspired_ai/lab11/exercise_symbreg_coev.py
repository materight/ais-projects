# -*- coding: utf-8 -*-

#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import sys
import time
import random

import numpy

from deap import base
from deap import creator
from deap import tools
from deap import gp

import exercise_symbreg as symbreg

"""
-------------------------------------------------------------------------
Edit this part to do the exercises
"""

GA_POP_SIZE = 200               # population size for GA
GP_POP_SIZE = 200               # population size for GP
NGEN = 50                       # number of generations (for both GA and GP)
GA_TRNMT_SIZE = 3               # tournament size for GA
GA_REP_IND = 10                 # number of arrays for each GA individual
GA_CXPB, GA_MUTPB = 0.5, 0.2    # crossover and mutation probability for GA
GP_CXPB, GP_MUTPB = 0.5, 0.2    # crossover and mutation probability for GP

"""
-------------------------------------------------------------------------
"""

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("IndGA", list, fitness=creator.FitnessMax)

toolbox_ga = base.Toolbox()

toolbox_ga.register("float", random.uniform, -1, 1)
toolbox_ga.register("individual", tools.initRepeat, creator.IndGA, toolbox_ga.float, GA_REP_IND)
toolbox_ga.register("population", tools.initRepeat, list, toolbox_ga.individual)

toolbox_ga.register("select", tools.selTournament, tournsize=GA_TRNMT_SIZE)
toolbox_ga.register("mate", tools.cxTwoPoint)
# we leave the internal parameters of mutation (mu, sigma and indpb) as they are
toolbox_ga.register("mutate", tools.mutGaussian, mu=0, sigma=0.01, indpb=0.05)

toolbox_gp = symbreg.toolbox

#--------------------------------------------------------------------

def main(seed):
    random.seed(seed)
    
    pop_ga = toolbox_ga.population(n=GA_POP_SIZE)
    pop_gp = toolbox_gp.population(n=GP_POP_SIZE)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "type", "evals", "std", "min", "avg", "max"
    
    best_ga = tools.selRandom(pop_ga, 1)[0]
    best_gp = tools.selRandom(pop_gp, 1)[0]
    
    for ind in pop_gp:
        ind.fitness.values = toolbox_gp.evaluate(ind, points=best_ga)  
    
    for ind in pop_ga:
        ind.fitness.values = toolbox_gp.evaluate(best_gp, points=ind)
    
    record = stats.compile(pop_ga)
    logbook.record(gen=0, type='ga', evals=len(pop_ga), **record)
    
    record = stats.compile(pop_gp)
    logbook.record(gen=0, type='gp', evals=len(pop_gp), **record)
    
    print(logbook.stream)
    
    # Begin the evolution
    for g in range(1, NGEN):
        # Select and clone the offspring
        off_ga = toolbox_ga.select(pop_ga, len(pop_ga))
        off_gp = toolbox_gp.select(pop_gp, len(pop_gp))
        off_ga = [toolbox_ga.clone(ind) for ind in off_ga]        
        off_gp = [toolbox_gp.clone(ind) for ind in off_gp]
        
        # Apply crossover and mutation
        for ind1, ind2 in zip(off_ga[::2], off_ga[1::2]):
            if random.random() < GA_CXPB:
                toolbox_ga.mate(ind1, ind2)
                del ind1.fitness.values
                del ind2.fitness.values
    
        for ind1, ind2 in zip(off_gp[::2], off_gp[1::2]):
            if random.random() < GP_CXPB:
                toolbox_gp.mate(ind1, ind2)
                del ind1.fitness.values
                del ind2.fitness.values
    
        for ind in off_ga:
            if random.random() < GA_MUTPB:
                toolbox_ga.mutate(ind)
                del ind.fitness.values
    
        for ind in off_gp:
            if random.random() < GP_MUTPB:
                toolbox_gp.mutate(ind)
                del ind.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        for ind in off_ga:
            ind.fitness.values = toolbox_gp.evaluate(best_gp, points=ind)
        
        for ind in off_gp:
            ind.fitness.values = toolbox_gp.evaluate(ind, points=best_ga)
                
        # Replace the old population by the offspring
        pop_ga = off_ga
        pop_gp = off_gp
        
        record = stats.compile(pop_ga)
        logbook.record(gen=g, type='ga', evals=len(pop_ga), **record)
        
        record = stats.compile(pop_gp)
        logbook.record(gen=g, type='gp', evals=len(pop_gp), **record)
        print(logbook.stream)
        
        best_ga = tools.selBest(pop_ga, 1)[0]
        best_gp = tools.selBest(pop_gp, 1)[0]

    #--------------------------------------------------------------------
    
    # plot GP tree
    import plot_utils as plot_utils
    nodes, edges, labels = gp.graph(best_gp)
    plot_utils.plotTree(nodes,edges,labels,sys.argv[0][0:-3]+'_'+str(seed),'results')
    
    #--------------------------------------------------------------------

    # plot fitness trends
    import matplotlib.pyplot as plt
    
    import os
    folder = 'results'
    if folder is not None and not os.path.exists(folder):
        os.makedirs(folder)
    name = sys.argv[0][0:-3]+'_'+str(seed)
    
    gen = numpy.array(logbook.select("gen"))
    fit_type = numpy.array(logbook.select("type"))
    fit_min = numpy.array(logbook.select("min"))
    fit_max = numpy.array(logbook.select("max"))
    fit_avg = numpy.array(logbook.select("avg"))
    fit_std = numpy.array(logbook.select("std"))
    
    ga_entries = numpy.array([i for i,val in enumerate(fit_type) if val=='ga'])
    gp_entries = numpy.array([i for i,val in enumerate(fit_type) if val=='gp'])
    
    fig = plt.figure("GA (fitness trend)")
    ax1 = fig.add_subplot(111)
    line1 = ax1.plot(gen[ga_entries], fit_min[ga_entries], label="Min")
    line2 = ax1.plot(gen[ga_entries], fit_max[ga_entries], label="Max")
    line3 = ax1.errorbar(gen[ga_entries], fit_avg[ga_entries], yerr=fit_std[ga_entries], label="Avg")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness")
    ax1.set_yscale("log")
    ax1.set_xlim(0,len(gen[ga_entries])-1)
    ax1.set_title('GA')
    ax1.legend()
    plt.savefig(folder+'/'+'trends_'+name+'_ga.png')
    
    fig = plt.figure("GP (fitness trend)")
    ax2 = fig.add_subplot(111)
    line1 = ax2.plot(gen[gp_entries], fit_min[gp_entries], label="Min")
    line2 = ax2.plot(gen[gp_entries], fit_max[gp_entries], label="Max")
    line3 = ax2.errorbar(gen[gp_entries], fit_avg[gp_entries], yerr=fit_std[gp_entries], label="Avg")
    ax2.set_xlabel("Generation")
    ax2.set_ylabel("Fitness")
    ax2.set_yscale("log")
    ax2.set_xlim(0,len(gen[gp_entries])-1)
    ax2.set_title('GP')
    ax2.legend()
    plt.savefig(folder+'/'+'trends_'+name+'_gp.png')

    plt.show()

    # plot real vs. GP-approximated values
    x_ = points=[x/10. for x in range(-100,100)]
    y_real = [symbreg.generatorFunction(x) for x in x_]
    gpFunction = toolbox_gp.compile(expr=best_gp)
    y_gp = [gpFunction(x) for x in x_]
    fig = plt.figure("GP (real vs approximated values)")
    ax1 = fig.add_subplot(111)
    line1 = ax1.plot(x_, y_real, label="Real")
    line2 = ax1.plot(x_, y_gp, label="GP")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.legend()
    plt.show()

    #--------------------------------------------------------------------

    print("Best individual GA is %s, %s" % (best_ga, best_ga.fitness.values))
    print("Best individual GP is %s, %s" % (best_gp, best_gp.fitness.values))

    return pop_ga, pop_gp, best_ga, best_gp, logbook

if __name__ == "__main__":
    if len(sys.argv) > 1 :
        seed = int(sys.argv[1])
    else :
        seed = int(time.time())

    main(seed)
