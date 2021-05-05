# -*- coding: utf-8 -*-

import sys
import os.path
import matplotlib
import numpy as np

from pylab import *

if __name__ == "__main__":
    
    if len(sys.argv) == 2 :
        seed = sys.argv[1]
    else :
        print("Usage: python plot_run.py SEED")
        sys.exit(-1)

    os.chdir(seed)

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

    #ioff()
    show()
