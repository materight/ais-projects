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
import operator
import math
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

"""
-------------------------------------------------------------------------
Edit this part to do the exercises
"""

GP_POP_SIZE = 300               # population size for GP
GP_NGEN = 40                    # number of generations for GP
GP_CXPB, GP_MUTPB = 0.5, 0.1    # crossover and mutation probability for GP
GP_TRNMT_SIZE = 3               # tournament size for GP
GP_HOF_SIZE = 1                 # size of the Hall-of-Fame for GP

"""
-------------------------------------------------------------------------
"""

# Define new functions
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
pset.renameArguments(ARG0='x')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

# TODO: try to change the expression e.g. to include trigonometric functions
def generatorFunction(x):
    #return math.sin(x)+math.cos(x)
    #return math.sin(x)*x**2
    #return math.sin(x)+5*x**2
    return x**4 + x**3 + x**2 + x

def evalSymbReg(individual, points):
    # Transform the tree expression in a callable function
    gpFunction = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression and the real function
    sqerrors = ((gpFunction(x) - generatorFunction(x))**2 for x in points)
    return math.fsum(sqerrors) / len(points),

toolbox.register("evaluate", evalSymbReg, points=[x/10. for x in range(-10,10)])
toolbox.register("select", tools.selTournament, tournsize=GP_TRNMT_SIZE)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

#--------------------------------------------------------------------

def main(seed):
    random.seed(seed)

    pop = toolbox.population(n=GP_POP_SIZE)
    hof = tools.HallOfFame(GP_HOF_SIZE)
    
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    final_pop,logbook=algorithms.eaSimple(pop, toolbox, GP_CXPB, GP_MUTPB, GP_NGEN, \
                                          stats=mstats, halloffame=hof, verbose=True)
               
    #--------------------------------------------------------------------
    
    # plot GP tree
    import plot_utils as plot_utils
    nodes, edges, labels = gp.graph(hof[0])
    plot_utils.plotTree(nodes,edges,labels,sys.argv[0][0:-3]+'_'+str(seed),'results')
    
    #--------------------------------------------------------------------
    
    # plot fitness vs size trends
    import matplotlib.pyplot as plt
    
    gen = logbook.select("gen")
    fit_mins = logbook.chapters["fitness"].select("min")
    size_avgs = logbook.chapters["size"].select("avg")
    
    fig = plt.figure("GP (fitness and tree size trend)")
    ax1 = fig.add_subplot(111)
    line1 = ax1.plot(gen, fit_mins, "b-", label="Minimum Fitness")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness", color="b")
    for tl in ax1.get_yticklabels():
        tl.set_color("b")

    ax2 = ax1.twinx()
    line2 = ax2.plot(gen, size_avgs, "r-", label="Average Size")
    ax2.set_ylabel("Size", color="r")
    for tl in ax2.get_yticklabels():
        tl.set_color("r")

    lns = line1 + line2
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc=0)
    import os
    folder = 'results'
    if folder is not None and not os.path.exists(folder):
        os.makedirs(folder)
    name = sys.argv[0][0:-3]+'_'+str(seed)
    plt.savefig(folder+'/'+'trends_'+name+'.png')

    # plot real vs approximated values
    x_ = points=[x/10. for x in range(-100,100)]
    y_real = [generatorFunction(x) for x in x_]
    gpFunction = toolbox.compile(expr=hof[0])
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
    
    print("Best individual GP is %s, %s" % (hof[0], hof[0].fitness.values))

    return final_pop, logbook, hof

if __name__ == "__main__":
    if len(sys.argv) > 1 :
        seed = int(sys.argv[1])
    else :
        seed = int(time.time())

    main(seed)
