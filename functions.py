import random
import math
import numpy as np

# static
M = 1000

def rand_sym(n_nodes):
	A = np.round(np.random.rand(n_nodes,n_nodes))
	for i in range(A.shape[0]):
		for j in range(i,A.shape[1]):
			A[i,j] = A[j,i]
		A[i,i] = 0
	return A

# combinatorics, r among n
def nCr(n,r):
	f = math.factorial
	return f(n) / f(r) / f(n-r)

def proba(A,density_objective,k):
# density_objective is the desired density of k-cliques
# A is the adjacency matrix
	d = density(A,k)
	result = math.exp(-M*(d-density_objective)**2)
	return result

def count_cliques(A,k):
	if k != 3:
		print "Not implemented yet, keeping k=3 (triangles)"
		k = 3
	
	result = 0
	n_nodes = A.shape[0]
	for i in range(n_nodes-1):
		neighbors_i = []
		for j in range(i+1,n_nodes):
			if (A[i,j] != 0):
				neighbors_i.append(j)
		
		result += np.sum(A[np.ix_(neighbors_i,neighbors_i)]!=0)/2
	return result

def density(A,k):
# k is the desired number of elements in a clique
	if k != 3:
		print "Not implemented yet, keeping k=3 (triangles)"
		k = 3
	n_cliques = count_cliques(A,k)
	density = float(n_cliques) / float(nCr(A.shape[0],k))
	return density

def naive_sample_neighbor_graph(A,n_nodes_to_modify=1):
# select a random edge in the graph and either add it or remove (according to if it already exists or not)
	candidate_A = A.copy()
	
	
# uniform probability
	T_proba = 1.0 / nCr(nCr(candidate_A.shape[0],2),n_nodes_to_modify)

# generate random edges
	lim_iterations = 10
	counter = 0

	while counter < lim_iterations:	
		random_edges = np.floor(np.random.rand(n_nodes_to_modify,2)*candidate_A.shape[0]).astype(int)
		b = np.ascontiguousarray(random_edges).view(np.dtype((np.void, random_edges.dtype.itemsize * random_edges.shape[1])))
		_, idx = np.unique(b, return_index=True)
		if (len(idx)==n_nodes_to_modify):
			break

	if counter == lim_iterations:
		print 'Warning: in naive_sample_neighbor_graph, the max number of iterations has been reached'		

	for edge in random_edges:
		candidate_A[edge[0],edge[1]] = 0 if candidate_A[edge[0],edge[1]] else 1
		candidate_A[edge[1],edge[0]] = candidate_A[edge[0],edge[1]]
	
	return T_proba, T_proba, candidate_A

def accept_or_reject(A,candidate_A,prob,T_proba_1, T_proba_2):
	#acceptance_proba = min(1,prob(candidate_A)*T_proba_1/(prob(A)*T_proba_2))
	print "candidate: %.6f, original: %.6f" % (prob(candidate_A),prob(A))
	#if (prob(candidate_A)==prob(A)):
	#	return False
	acceptance_proba = min(1,prob(candidate_A)/prob(A))
	assert (acceptance_proba >= 0 and acceptance_proba <= 1), "Acceptance probability out of bounds"
	return (random.random() <= acceptance_proba)

def metropolis(init_A,n_iter,prob,sampler,k):
	count_accept = 0
	count_reject = 0
	A = init_A.copy()
	record_proba = [density(A,k)]
	print "Beginning Metropolis Hastings sampling"
	for j in range(n_iter):
		#print '\r%d' % k
		T_proba_1, T_proba_2, candidate_A = sampler(A)
		if (accept_or_reject(A,candidate_A,prob,T_proba_1,T_proba_2)):
			A = candidate_A.copy()
			record_proba.append(density(A,k))
			count_accept += 1
		else:
			record_proba.append(record_proba[-1])
			count_reject += 1
	print "Accepted:%d, Rejected:%d" % (count_accept, count_reject)
	return record_proba


		
		
	
	
