#!/usr/bin/python
import numpy as np
from energy import get_energy
from force import get_forces, move_vertices
from transition import T1_transition
import sys
from parameters import get_parameters
from parser import *


def molecular_dynamics(vertices, edges, polys, parameters, T):

	delta_t = parameters['delta_t']

	# time
	t = 0



	while t < T:

		# get energy for network
		energy = get_energy(vertices, polys, edges, parameters)
		# print energy		
		
		# get forces for network
		forces = get_forces(vertices, polys, edges, parameters)
		print np.sum(forces**2)**(0.5)

	
		# move vertices
		vertices = move_vertices(vertices, forces, parameters)

		# check for T1 transitions
		cells, edges = T1_transition(vertices, polys, edges, parameters)

		# add routine to write vertices, energy, forces at every time step
		# can be used for plotting routines later...
	
		t += delta_t


	return






# command line arguments for data files
vertex_file = sys.argv[1]
edge_file = sys.argv[2]
poly_file = sys.argv[3]


# Parameters
lx = 9 * (2 / (3 * (3**0.5)))**0.5
ly = 4 * (2 / (3**0.5))**0.5
ka = 1.
A0 = 1. # current preferred area for polygon
gamma = 0.04 * ka * A0 # hexagonal network
# gamma = 0.1 * ka * A0 # soft network
Lambda = 0.12 * ka * (A0**(3/2)) # hexagonal network
# Lambda = -0.85 * ka * A0**(3/2) # soft network
lmin = 0.2
delta_t = 0.05
eta = 1.

# maximum Time
T = 0.1

# get parameter dictionary
parameters = get_parameters(lx, ly, ka, gamma, Lambda, eta, lmin, delta_t)

# get vertices
vertices = read_vertices(vertex_file)

# get edges
edges = read_edges(edge_file)

# get polygons
poly_indices = read_poly_indices(poly_file)
polys = build_polygons(poly_indices, A0)

molecular_dynamics(vertices, edges, polys, parameters, T)