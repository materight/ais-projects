# -*- coding: utf-8 -*-

from random import Random
from random import shuffle
from queue import Queue

import time
import sys
import math
import shutil
import os.path
import threading
import inspyred
import matplotlib
import numpy as np

from pylab import *

from inspyred import ec
from inspyred_utils import NumpyRandomWrapper

"""
-------------------------------------------------------------------------
Edit this part to do the exercises
"""

display = True
showArchives = True

config_file = "config2d2_prey_predator.txt"

# parameters for standard GA
popSize = 20                # population size
numGen = 20                 # used with generation_termination
numEval = 2500              # used with evaluation_termination
tournamentSize = 2          # tournament size (default 2)
mutationRate = 0.2          # mutation rate, per gene (default 0.1)
gaussianMean = 0            # mean of the Gaussian distribution used for mutation
gaussianStdev = 0.1         # std. dev. of the Gaussian distribution used for mutation
crossoverRate = 1.0         # rate at which crossover is performed (default 1.0)
numCrossoverPoints = 1      # number of crossover points used (default 1)
selectionSize = popSize     # selection size (i.e. how many individuals are selected for reproduction)
numElites = 1               # no. of elites (i.e. best individuals that are kept in the population)

# parameters for competitive coevolution
numOpponents = 5            # number of opponents against which each robot competes at each generation
archiveType = "HALLOFFAME"        # possible types: {GENERATION,HALLOFFAME,BEST}
archiveUpdate = "AVERAGE"     # possible types: {WORST,AVERAGE}
updateBothArchives = False  # True is each generation should update both archives, False otherwise

# 1. Generational competition: the archive is filled with the best individuals from previous n generations (e.g. n=5)
# 2. Hall-of-Fame: each new individual is tested against *all best opponents* obtained so far.
#    NOTE: Using this method, the no. of tournaments increases along generations!
#    However, it is sufficient to test new individuals only against a limited sample of n opponents (e.g. n=10)
# 3. Best competition: the archive is filled with the best n (e.g. n=5) individuals from *all* previous generations

"""
-------------------------------------------------------------------------
"""

# --------------------------------------------------------------------------- #
# Stores a (limited or not) archive of solutions with their fitnesses

class ArchiveSolutions():
    
    def __init__(self,size=None):
        self.candidates = []
        self.fitnesses = []
        self.size = size
    
    def appendToArchive(self,candidate,fitness=None,maximize=None,archiveType=None):
        if self.size is None or \
            archiveType is None or \
            archiveType == "HALLOFFAME" or \
            ( len(self.candidates) < self.size and len(self.fitnesses) < self.size ):
            if candidate in self.candidates:
                index = self.candidates.index(candidate)
                self.fitnesses[index] = fitness
            else:
                self.candidates.append(candidate)
                self.fitnesses.append(fitness)
        else:
            if archiveType == "GENERATION":
                # delete the oldest candidate and add the new one
                if candidate in self.candidates:
                    index = self.candidates.index(candidate)
                    self.fitnesses[index] = fitness
                else:
                    del self.candidates[0]
                    del self.fitnesses[0]
                    self.candidates.append(candidate)
                    self.fitnesses.append(fitness)
            elif archiveType == "BEST":
                # find worst candidate in the archive
                if maximize:
                    worstFitness = min(self.fitnesses)
                else:
                    worstFitness = max(self.fitnesses)
                worstIndex = self.fitnesses.index(worstFitness)
                # replace it if the new candidate is better than the worst candidate in the archive
                if (fitness > worstFitness and maximize) or \
                    (fitness < worstFitness and not maximize):
                    if candidate in self.candidates:
                        index = self.candidates.index(candidate)
                        self.fitnesses[index] = fitness
                    else:
                        del self.candidates[worstIndex]
                        del self.fitnesses[worstIndex]
                        self.candidates.append(candidate)
                        self.fitnesses.append(fitness)

    def getIndexesOfOpponents(self,numOpponents):
        archiveSize = len(self.candidates)
        indexes = list(range(archiveSize))
        shuffle(indexes)
        numOpponents = min(numOpponents,archiveSize)
        return indexes[0:numOpponents]

# --------------------------------------------------------------------------- #
# Global objects

# These two archives keep the best preys and best predators
global archivePreys, archivePredators
if archiveType == "GENERATION" or archiveType == "BEST":
    archivePreys = ArchiveSolutions(numOpponents)
    archivePredators = ArchiveSolutions(numOpponents)
elif archiveType == "HALLOFFAME":
    archivePreys = ArchiveSolutions()
    archivePredators = ArchiveSolutions()

# the initial popolations (we need to make initialize them externally to initialize the archives)
global initialPreys, initialPredators
initialPreys = ArchiveSolutions(popSize)
initialPredators = ArchiveSolutions(popSize)

# TODO: change maximize flag depending on how fitness is defined
global problemPreysMaximize, problemPredatorsMaximize
problemPreysMaximize = True         # e.g. maximize (final/min) distance from predator or maximize time-to-contact
problemPredatorsMaximize = False    # e.g. minimize (final/min) distance from prey or minimize time-to-contact

# --------------------------------------------------------------------------- #
# Util functions

def readConfigFile(file):
    myvars = {}
    with open(file) as f:
        lines = f.read().splitlines()
        for line in lines:
            if line.startswith("#"):
                pass
            else:
                if "=" in line:
                    name, var = line.partition("=")[::2]
                    myvars[name.strip()] = var.strip()
    return myvars

def writeCandidatesToFile(file,candidates):
    with open(file, "w") as f:
        for candidate in candidates:
            for i in np.arange(len(candidate)-1):
                f.write(str(candidate[i]) + " ")
            f.write(str(candidate[i]) + "\n")

def readFileAsMatrix(file):
    with open(file) as f:
        lines = f.read().splitlines()
        matrix = []
        for line in lines:
            row = []
            for value in line.split():
                row.append(float(value.replace(",",".")))
            matrix.append(row)
        return matrix

def getAggregateFitness(fitness_tmp,maximize):
    if archiveUpdate == "AVERAGE":
        fitness = np.mean(fitness_tmp)
    elif archiveUpdate == "WORST":
        if maximize:
            fitness = np.min(fitness_tmp)
        else:
            fitness = np.max(fitness_tmp)
    return fitness

def getIndexOfBest(fitnesses,maximize):
    if maximize:
        bestFitness = max(fitnesses)
    else:
        bestFitness = min(fitnesses)
    bestIndex = fitnesses.index(bestFitness)
    return bestIndex

# --------------------------------------------------------------------------- #
# The robot evaluator class

class RobotEvaluator():

    def __init__(self, config_file, name, q_mine, q_his, seed, maximize):

        self.config_file = config_file
        self.name = name
        self.q_mine = q_mine
        self.q_his = q_his
        self.seed = seed
        
        parameters = readConfigFile("Java2dRobotSim/config/" + self.config_file)
        basePhi = parameters["basePhi"]
        
        nrIRSensors = (len(basePhi.split(" ")) if " " in basePhi else 0) + 2
        nrInputNodes = nrIRSensors
        nrHiddenNodes = int(parameters["nrHiddenNodes"])
        nrOutputNodes = 2

        # calculate the no. of weights
        networkType = parameters["networkType"]
        if nrHiddenNodes > 0:
            if networkType == "FFNN":
                nrWeights = (nrInputNodes+1)*nrHiddenNodes + (nrHiddenNodes+1)*nrOutputNodes
            elif networkType == "ELMAN":
                nrWeights = (nrInputNodes+1)*nrHiddenNodes + (nrHiddenNodes+1)*nrOutputNodes + nrHiddenNodes*nrHiddenNodes
            elif networkType == "JORDAN":
                nrWeights = (nrInputNodes+1)*nrHiddenNodes + (nrHiddenNodes+1)*nrOutputNodes + nrOutputNodes*nrOutputNodes
        else:
            nrWeights = (nrInputNodes+1)*nrOutputNodes

        self.geneMin = float(parameters["geneMin"])
        self.geneMax = float(parameters["geneMax"])
        self.nrTimeStepsGen = int(parameters["nrTimeStepsGen"])
        
        self.nrWeights = nrWeights
        self.bounder = ec.Bounder([self.geneMin]*self.nrWeights, [self.geneMax]*self.nrWeights)
        
        self.maximize = maximize

        self.genCount = 0
    
    def generator(self, random, args):
        return [random.uniform(self.geneMin,self.geneMax) for _ in range(self.nrWeights)]
    
    def evaluator(self, candidates, args):
        
        global archivePreys, archivePredators
        global initialPreys, initialPredators
        global problemPreysMaximize, problemPredatorsMaximize
        
        # get lock
        self.q_mine.get()
        
        # identify candidates and opponents
        if self.genCount == 0:
            # at the first generation, let all preys compete against all predators
            preys = initialPreys.candidates
            predators = initialPredators.candidates
        else:
            # at the next generations, let all preys (predators) compete against individuals in the archives of predators (preys)
            if self.name == "Preys":
                preys = candidates
                if archiveType == "HALLOFFAME":
                    indexesOfOpponents = archivePredators.getIndexesOfOpponents(numOpponents)
                    predators = []
                    archiveSize = len(archivePredators.candidates)
                    for i in range(min(numOpponents,archiveSize)):
                        predators.append(archivePredators.candidates[indexesOfOpponents[i]])
                else:
                    predators = archivePredators.candidates
            elif self.name == "Predators":
                predators = candidates
                if archiveType == "HALLOFFAME":
                    indexesOfOpponents = archivePreys.getIndexesOfOpponents(numOpponents)
                    preys = []
                    archiveSize = len(archivePreys.candidates)
                    for i in range(min(numOpponents,archiveSize)):
                        preys.append(archivePreys.candidates[indexesOfOpponents[i]])
                else:
                    preys = archivePreys.candidates
        
        # create the candidate populations to evaluate
        # we assume that the population is split in two halves, one for preys and one for predators
        """
            n (preys) repeated m (predators) times
            vs
            1 predator -repeated n (preys)- repeated m (predators) times
            
            [                   [               -
            prey_1              predator_1      |
            prey_2              predator_1      |
            ...                 ...             n
            prey_n              predator_1      |
            ]                   ]               -
            
            [                   [
            prey_1              predator_2
            prey_2              predator_2
            ...                 ...
            prey_n              predator_2
            ]                   ]
            
            ...                 ...
            
            [                   [
            prey_1              predator_m
            prey_2              predator_m
            ...                 ...
            prey_n              predator_m
            ]                   ]
        """
        preysPredators = []
        
        # append preys
        for predator in predators:
            for prey in preys:
                preysPredators.append(prey)
        # append predators
        for predator in predators:
            for prey in preys:
                preysPredators.append(predator)
                            
        # run the simulator
        communication_dir = "."
        request_file = communication_dir + "/to_eval" + self.name + ".txt"
        results_file = communication_dir + "/results.txt"
        
        results = writeCandidatesToFile(request_file, preysPredators)
        
        command = "java -jar Java2dRobotSim/Java2dRobotSim.jar Java2dRobotSim/config/" + \
            self.config_file + " " + communication_dir + " -f " + request_file + " -s " + str(self.seed) + " >/dev/null"
        result = os.system(command)
    
        results = readFileAsMatrix(results_file)
        numRobots = len(results)
        
        # TODO: calculate fitness here
        fitnessTmp = []
        for i in np.arange(numRobots):
            finalDistanceToTarget = results[i][0]
            minDistanceToTarget = results[i][1]
            timeToContact = results[i][2]
            #fitnessTmp.append(minDistanceToTarget)
            #fitnessTmp.append((minDistanceToTarget+0.01) * timeToContact)
            #fitnessTmp.append(timeToContact)
            if i < numRobots/2:
                # preys
                fitnessTmp.append(minDistanceToTarget)
            else:
                # predators
                fitnessTmp.append(timeToContact)
            

        # update fitness and archives
        fitness_preys = []
        fitness_predators = []
        
        numPredators = len(predators)
        numPreys = len(preys)

        # --------------------------------------------------------------------------- #
        if updateBothArchives:
            # (update alternative) in this case at each step we update both archives
            # update fitness of preys
            for i in range(numPreys):
                prey = preysPredators[i]
                indexes = np.arange(i,numPreys*numPredators,numPreys)
                fitness_prey = getAggregateFitness(np.array(fitnessTmp)[indexes],problemPreysMaximize)
                fitness_preys.append(fitness_prey)
            if archiveType == "GENERATION" or archiveType == "HALLOFFAME":
                # get best prey in the current population
                indexOfBestPrey = getIndexOfBest(fitness_preys,problemPreysMaximize)
                bestPrey = preysPredators[indexOfBestPrey]
                bestPreyFitness = fitness_preys[indexOfBestPrey]
                # update archive of preys
                archivePreys.appendToArchive(bestPrey,bestPreyFitness,problemPreysMaximize,archiveType)
            elif archiveType == "BEST":
                # update archive of preys
                for i in range(numPreys):
                    prey = preysPredators[i]
                    fitness_prey = fitness_preys[i]
                    archivePreys.appendToArchive(prey,fitness_prey,problemPreysMaximize,archiveType)

            # update fitness of predators
            for i in range(numPredators):
                predator = preysPredators[numPreys*numPredators+i*numPreys]
                indexes = np.arange(numPreys*numPredators+i*numPreys,numPreys*numPredators+i*numPreys+numPreys)
                fitness_predator = getAggregateFitness(np.array(fitnessTmp)[indexes],problemPredatorsMaximize)
                fitness_predators.append(fitness_predator)
            if archiveType == "GENERATION" or archiveType == "HALLOFFAME":
                # get best predator in the current population
                indexOfBestPredator = getIndexOfBest(fitness_predators,problemPredatorsMaximize)
                bestPredator = preysPredators[numPreys*numPredators+indexOfBestPredator*numPreys]
                bestPredatorFitness = fitness_predators[indexOfBestPredator]
                # update archive of predators
                archivePredators.appendToArchive(bestPredator,bestPredatorFitness,problemPredatorsMaximize,archiveType)
            elif archiveType == "BEST":
                # update archive of predators
                for i in range(numPredators):
                    predator = preysPredators[numPreys*numPredators+i*numPreys]
                    fitness_predator = fitness_predators[i]
                    archivePredators.appendToArchive(predator,fitness_predator,problemPredatorsMaximize,archiveType)
        else:
            # (update alternative) in this case at each step we update only one archive
            if self.name == "Preys":
                # update fitness of preys
                for i in range(numPreys):
                    prey = preysPredators[i]
                    indexes = np.arange(i,numPreys*numPredators,numPreys)
                    fitness_prey = getAggregateFitness(np.array(fitnessTmp)[indexes],problemPreysMaximize)
                    fitness_preys.append(fitness_prey)
                if archiveType == "GENERATION" or archiveType == "HALLOFFAME":
                    # get best prey in the current population
                    indexOfBestPrey = getIndexOfBest(fitness_preys,problemPreysMaximize)
                    bestPrey = preysPredators[indexOfBestPrey]
                    bestPreyFitness = fitness_preys[indexOfBestPrey]
                    # update archive of preys
                    archivePreys.appendToArchive(bestPrey,bestPreyFitness,problemPreysMaximize,archiveType)
                elif archiveType == "BEST":
                    # update archive of preys
                    for i in range(numPreys):
                        prey = preysPredators[i]
                        fitness_prey = fitness_preys[i]
                        archivePreys.appendToArchive(prey,fitness_prey,problemPreysMaximize,archiveType)
            elif self.name == "Predators":
                # update fitness of predators
                for i in range(numPredators):
                    predator = preysPredators[numPreys*numPredators+i*numPreys]
                    indexes = np.arange(numPreys*numPredators+i*numPreys,numPreys*numPredators+i*numPreys+numPreys)
                    fitness_predator = getAggregateFitness(np.array(fitnessTmp)[indexes],problemPredatorsMaximize)
                    fitness_predators.append(fitness_predator)
                if archiveType == "GENERATION" or archiveType == "HALLOFFAME":
                    # get best predator in the current population
                    indexOfBestPredator = getIndexOfBest(fitness_predators,problemPredatorsMaximize)
                    bestPredator = preysPredators[numPreys*numPredators+indexOfBestPredator*numPreys]
                    bestPredatorFitness = fitness_predators[indexOfBestPredator]
                    # update archive of predators
                    archivePredators.appendToArchive(bestPredator,bestPredatorFitness,problemPredatorsMaximize,archiveType)
                elif archiveType == "BEST":
                    # update archive of predators
                    for i in range(numPredators):
                        predator = preysPredators[numPreys*numPredators+i*numPreys]
                        fitness_predator = fitness_predators[i]
                        archivePredators.appendToArchive(predator,fitness_predator,problemPredatorsMaximize,archiveType)
        # --------------------------------------------------------------------------- #

        if self.name == "Preys":
            fitness = fitness_preys
        elif self.name == "Predators":
            fitness = fitness_predators

        # copy/remove results files
        if not os.path.exists(str(seed)):
            os.makedirs(str(seed))
        shutil.copy(request_file, str(seed) + "/candidates_" + str(self.genCount) + "_" + self.name + ".txt")
        shutil.copy(results_file, str(seed) + "/results_" + str(self.genCount) + "_" + self.name + ".txt")
        if os.path.exists(request_file):
            os.remove(request_file)
        if os.path.exists(results_file):
            os.remove(results_file)
        
        # show archives
        if showArchives:
            archive = "Archive preys: [ "
            for x in archivePreys.fitnesses:
                archive += "{:.4f}".format(x) + " "
            print(archive + "]")
            
            archive = "Archive predators: [ "
            for x in archivePredators.fitnesses:
                archive += "{:.4f}".format(x) + " "
            print(archive + "]")

        print(self.name, self.genCount, "/", numGen)

        # increment generation counter
        self.genCount += 1

        # release lock
        self.q_his.put(1)
        
        return fitness

# --------------------------------------------------------------------------- #

def runEA(problem):
    
    # --------------------------------------------------------------------------- #
    # EA configuration
    
    # the evolutionary algorithm (EvolutionaryComputation is a fully configurable evolutionary algorithm)
    # standard GA, ES, SA, DE, EDA, PAES, NSGA2, PSO and ACO are also available
    ea = inspyred.ec.EvolutionaryComputation(rng)
    
    # observers: provide various logging features
    if display:
        ea.observer = [inspyred.ec.observers.file_observer]
                       #inspyred.ec.observers.stats_observer
                       #inspyred.ec.observers.file_observer,
                       #inspyred.ec.observers.best_observer,
                       #inspyred.ec.observers.population_observer,

    # selection operator
    #ea.selector = inspyred.ec.selectors.truncation_selection
    #ea.selector = inspyred.ec.selectors.uniform_selection
    #ea.selector = inspyred.ec.selectors.fitness_proportionate_selection
    #ea.selector = inspyred.ec.selectors.rank_selection
    ea.selector = inspyred.ec.selectors.tournament_selection

    # variation operators (mutation/crossover)
    ea.variator = [inspyred.ec.variators.gaussian_mutation,
                   inspyred.ec.variators.n_point_crossover]
                    #inspyred.ec.variators.random_reset_mutation,
                    #inspyred.ec.variators.inversion_mutation,
                    #inspyred.ec.variators.uniform_crossover,
                    #inspyred.ec.variators.partially_matched_crossover,

    # replacement operator
    #ea.replacer = inspyred.ec.replacers.truncation_replacement
    #ea.replacer = inspyred.ec.replacers.steady_state_replacement
    #ea.replacer = inspyred.ec.replacers.random_replacement
    #ea.replacer = inspyred.ec.replacers.plus_replacement
    #ea.replacer = inspyred.ec.replacers.comma_replacement
    #ea.replacer = inspyred.ec.replacers.crowding_replacement
    #ea.replacer = inspyred.ec.replacers.simulated_annealing_replacement
    #ea.replacer = inspyred.ec.replacers.nsga_replacement
    #ea.replacer = inspyred.ec.replacers.paes_replacement
    ea.replacer = inspyred.ec.replacers.generational_replacement

    # termination condition
    #ea.terminator = inspyred.ec.terminators.evaluation_termination
    #ea.terminator = inspyred.ec.terminators.no_improvement_termination
    #ea.terminator = inspyred.ec.terminators.diversity_termination
    #ea.terminator = inspyred.ec.terminators.time_termination
    ea.terminator = inspyred.ec.terminators.generation_termination

    # --------------------------------------------------------------------------- #

    if problem.name == "Preys":
        initialPopulation = initialPreys.candidates
    elif problem.name == "Predators":
        initialPopulation = initialPredators.candidates

    # run the EA
    final_pop = ea.evolve(seeds=initialPopulation,
                  generator=problem.generator,
                  evaluator=problem.evaluator,
                  bounder=problem.bounder,
                  maximize=problem.maximize,
                  pop_size=popSize,
                  max_generations=numGen,
                  #max_evaluations=numEval,
                  tournament_size=tournamentSize,
                  mutation_rate=mutationRate,
                  gaussian_mean=gaussianMean,
                  gaussian_stdev=gaussianStdev,
                  crossover_rate=crossoverRate,
                  num_crossover_points=numCrossoverPoints,
                  num_selected=selectionSize,
                  num_elites=numElites,
                  statistics_file=open("stats_"+problem.name+".csv","w"),
                  individuals_file=open("individuals_"+problem.name+".csv","w"))
                              
    # --------------------------------------------------------------------------- #

    return final_pop

# --------------------------------------------------------------------------- #

def main(rng, seed, display=False):

    # the following queues allow the two threads to alternate their execution
    qAB = Queue()
    qBA = Queue()
    
    # create the robot evaluator instances
    problemPreys = RobotEvaluator(config_file, "Preys", qAB, qBA, seed, problemPreysMaximize)
    problemPredators = RobotEvaluator(config_file, "Predators", qBA, qAB, seed, problemPredatorsMaximize)
    
    # create the initial populations
    for i in np.arange(popSize):
        candidatePrey = [(problemPreys.geneMax-problemPreys.geneMin)*rng.random_sample()+problemPreys.geneMin \
                         for _ in range(problemPreys.nrWeights)]
        initialPreys.appendToArchive(candidatePrey)
    for i in np.arange(popSize):
        candidatePredator = [(problemPredators.geneMax-problemPredators.geneMin)*rng.random_sample()+problemPredators.geneMin \
                             for _ in range(problemPredators.nrWeights)]
        initialPredators.appendToArchive(candidatePredator)

    t1 = threading.Thread(target=runEA, args=(problemPreys,))
    t2 = threading.Thread(target=runEA, args=(problemPredators,))

    # this is needed to unlock the thread "Preys" first
    qAB.put(1)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
    if display:

        """
        # rerun every prey in the archive against every predator in the archive
        preysPredators = []
        
        # append preys
        for predator in archivePredators.candidates:
            for prey in archivePreys.candidates:
                preysPredators.append(prey)
        # append predators
        for predator in archivePredators.candidates:
            for prey in archivePreys.candidates:
                preysPredators.append(predator)
        """
        
        # rerun the best prey in the archive against the best predator in the archive
        preysPredators = []
        indexOfBestPrey = getIndexOfBest(archivePreys.fitnesses,problemPreysMaximize)
        bestPrey = archivePreys.candidates[indexOfBestPrey]
        bestPreyFitness = archivePreys.fitnesses[indexOfBestPrey]
        indexOfBestPredator = getIndexOfBest(archivePredators.fitnesses,problemPredatorsMaximize)
        bestPredator = archivePredators.candidates[indexOfBestPredator]
        bestPredatorFitness = archivePredators.fitnesses[indexOfBestPredator]
        preysPredators.append(bestPrey)
        preysPredators.append(bestPredator)
        
        writeCandidatesToFile("best.txt", preysPredators)

        os.chdir("Java2dRobotSim")
        command = "./runApplet.sh config/" + config_file + " .. ../best.txt " + str(seed)
        result = os.system(command)
        os.chdir("..")
        
        if not os.path.exists(str(seed)):
            os.makedirs(str(seed))
        shutil.copy("best.txt", str(seed) + "/best_candidates.txt")
        shutil.copy("results.txt", str(seed) + "/best_results.txt")
        if os.path.exists("best.txt"):
            os.remove("best.txt")
        if os.path.exists("results.txt"):
            os.remove("results.txt")

        # format of these files : {generation number, population size, worst, best, median, average, standard deviation}
        statsPreys = np.transpose(np.loadtxt(open("stats_Preys.csv", "r"), delimiter=","))
        statsPredators = np.transpose(np.loadtxt(open("stats_Predators.csv", "r"), delimiter=","))

        # plot fitness trends of preys and predators
        figure("Preys")
        plot(statsPreys[2],label="Worst")
        plot(statsPreys[3],label="Best")
        plot(statsPreys[4],label="Median")
        plot(statsPreys[5],label="Mean")
        #yscale("log")
        xlabel("Generation")
        ylabel("Fitness")
        legend()

        figure("Predators")
        plot(statsPredators[2],label="Worst")
        plot(statsPredators[3],label="Best")
        plot(statsPredators[4],label="Median")
        plot(statsPredators[5],label="Mean")
        #yscale("log")
        xlabel("Generation")
        ylabel("Fitness")
        legend()

        # copy/remove results files
        shutil.copy("stats_Predators.csv", str(seed))
        shutil.copy("stats_Preys.csv", str(seed))
        shutil.copy("individuals_Predators.csv", str(seed))
        shutil.copy("individuals_Preys.csv", str(seed))
        if os.path.exists("stats_Predators.csv"):
            os.remove("stats_Predators.csv")
        if os.path.exists("stats_Preys.csv"):
            os.remove("stats_Preys.csv")
        if os.path.exists("individuals_Predators.csv"):
            os.remove("individuals_Predators.csv")
        if os.path.exists("individuals_Preys.csv"):
            os.remove("individuals_Preys.csv")

if __name__ == "__main__":
    
    if len(sys.argv) > 1 :
        seed = int(sys.argv[1])
    else :
        seed = int(time.time())
    rng = NumpyRandomWrapper(seed)
    
    main(rng,seed,display)

    if display:
        ioff()
        show()
