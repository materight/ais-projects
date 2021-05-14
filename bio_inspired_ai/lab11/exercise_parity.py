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
import operator

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
GP_CXPB, GP_MUTPB = 0.8, 0.2    # crossover and mutation probability for GP
GP_TRNMT_SIZE = 7               # tournament size for GP
GP_HOF_SIZE = 3                 # size of the Hall-of-Fame for GP

PARITY_FANIN_M = 8              # input size of the Parity problem

"""
-------------------------------------------------------------------------
"""

# Initialize Parity problem input and output matrices
PARITY_SIZE_M = 2**PARITY_FANIN_M

inputs = [None] * PARITY_SIZE_M
outputs = [None] * PARITY_SIZE_M

for i in range(PARITY_SIZE_M):
    inputs[i] = [None] * PARITY_FANIN_M
    value = i
    dividor = PARITY_SIZE_M
    parity = 1
    for j in range(PARITY_FANIN_M):
        dividor /= 2
        if value >= dividor:
            inputs[i][j] = 1
            parity = int(not parity)
            value -= dividor
        else:
            inputs[i][j] = 0
    outputs[i] = parity

pset = gp.PrimitiveSet("MAIN", PARITY_FANIN_M, "IN")
pset.addPrimitive(operator.and_, 2)
pset.addPrimitive(operator.or_, 2)
pset.addPrimitive(operator.xor, 2)
pset.addPrimitive(operator.not_, 1)
pset.addTerminal(1)
pset.addTerminal(0)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=3, max_=5)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalParity(individual):
    func = toolbox.compile(expr=individual)
    return sum(func(*in_) == out for in_, out in zip(inputs, outputs)),

toolbox.register("evaluate", evalParity)
toolbox.register("select", tools.selTournament, tournsize=GP_TRNMT_SIZE)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

#--------------------------------------------------------------------

def main(seed):
    random.seed(seed)
    
    pop = toolbox.population(n=GP_POP_SIZE)
    hof = tools.HallOfFame(GP_HOF_SIZE)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    final_pop,logbook=algorithms.eaSimple(pop, toolbox, GP_CXPB, GP_MUTPB, GP_NGEN, \
                                          stats, halloffame=hof)
    
    #--------------------------------------------------------------------
    
    # plot GP tree
    import plot_utils as plot_utils
    nodes, edges, labels = gp.graph(hof[0])
    plot_utils.plotTree(nodes,edges,labels,'exercise_parity_'+str(seed),'results')

    # plot fitness trends
    plot_utils.plotTrends(logbook,'exercise_parity_'+str(seed),'results')
    
    #--------------------------------------------------------------------
    
    print("Best individual GP is %s, %s" % (hof[0], hof[0].fitness.values))
    
    return pop, stats, hof

if __name__ == "__main__":
    if len(sys.argv) > 1 :
        seed = int(sys.argv[1])
    else :
        seed = int(time.time())
    
    main(seed)

