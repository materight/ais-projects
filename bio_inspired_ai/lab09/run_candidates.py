# -*- coding: utf-8 -*-

import sys
import os.path

if __name__ == "__main__":
    
    if len(sys.argv) != 3 :
        print("Usage: python run_candidates.py CONFIG_FILE BEST_FILE")
    else :
        config_file = sys.argv[1]
        best_file = sys.argv[2]
        seed = os.path.dirname(os.path.normpath(best_file))

        os.chdir("Java2dRobotSim")
        command = "./runApplet.sh config/" + config_file + " . ../" + best_file + " " + str(seed)
        result = os.system(command)
        if os.path.exists("results.txt"):
            os.remove("results.txt")
