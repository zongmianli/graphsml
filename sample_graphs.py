##########################################
##########################################

import functions as fct
import sys
import random
import itertools
from cycler import cycler
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
import math
import operator


def parseArguments():
	parser = argparse.ArgumentParser(description="Sample graphs with a given triangle density")
	
	parser.add_argument("n_nodes",
		type=int, help="Number of nodes in samples graphs (fixed)")

	parser.add_argument("target_density",
		type=float, help="Target triangle density")

	args = parser.parse_args()
	return args


##################################################
###################### MAIN ######################
##################################################

def plot_evol_proba(record_proba):
	values = np.array(record_proba)
	plt.plot(values)
	plt.ylabel("density")
	plt.xlabel("Number of iteration")

def main():
	args = parseArguments()
	n_nodes = args.n_nodes
	target_density = args.target_density

	k = 3 #only handling triangle density for the moment
	def prob(A):
		return fct.proba(A,target_density,k)

	def sampler(A):
		return fct.naive_sample_neighbor_graph(A)

	#init_A = np.zeros([n_nodes,n_nodes])
	init_A = fct.rand_sym(n_nodes)

	record_proba = fct.metropolis(init_A,1000,prob,sampler,k)	
	
	plot_evol_proba(record_proba)
	plt.show()

if __name__ == '__main__':
    main()
