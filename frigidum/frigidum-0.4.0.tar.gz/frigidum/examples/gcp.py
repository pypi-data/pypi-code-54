"""

	Graph Coloring Problem

import frigidum
from frigidum.examples import gcp

print( "Trying to color DSJC1000.9 in {} colors".format(gcp.goal_number_of_colors) )
local_opt = frigidum.sa(random_start=gcp.random_start,
           objective_function=gcp.objective_function,
           neighbours=[gcp.force_add_random_vertex, gcp.force_add_random_vertex_on_low_used_color,
           gcp.parallel_add_random_vertex, gcp.parallel_force_add_random_vertex_on_low_used_color],
           copy_state=frigidum.annealing.naked,
           T_start=10,
           alpha=.999,
           T_stop=0.05,
           O_stop=0,
           repeats=10**2)

local_opt = frigidum.sa(random_start=random_start, 
    ...:            objective_function=objective_function, 
    ...:            neighbours=[force_add_random_vertex, force_add_random_vertex_on_low_used_color, 
    ...:            parallel_add_random_vertex], 
    ...:            copy_state=frigidum.annealing.naked, 
    ...:            T_start=10, 
    ...:            alpha=.999, 
    ...:            T_stop=0.01, 
    ...:            O_stop=0, 
    ...:            repeats=10**3)


"""
import numpy as np
from frigidum.examples import dsjc1000_9


edges_matrix = np.zeros( (1000,1000), dtype=np.bool )

edges_matrix[ dsjc1000_9.edges_coords[:,1], dsjc1000_9.edges_coords[:,0] ] = 1
edges_matrix[ dsjc1000_9.edges_coords[:,0], dsjc1000_9.edges_coords[:,1] ] = 1

assert np.sum(edges_matrix) == 2 * 449449


vertices_degree = np.sum( edges_matrix, axis = 1 )  

goal_number_of_colors = 250
goal_average = edges_matrix[0].size / goal_number_of_colors

class_exponent = 1.5

"""

Strategy:

Start with 1 color, 
and optimize the number of vertices to color.

When the average number of vertices of used color(s) 
is >= average to reach goal, 
add another color.

Hence it is very conservative using colors,
and only will add a new color when it is 'happy'
about usage/coverage of current colors.

If we only add colors if the average vertices/color
is high, we can use the number of colors
short as the objective.

The objective is indeed reflects the numbers of 
colors short,
where we also take in account the current 
averate vertices/color, such that a neighbor
who will increate the average vertices/color, but not 
necessart enough to add a new color is accepted.

The rational behind this strategy is to guide
the difficulty part of the GCP very controlled, 
finding large independent sets.

Down-side of this controlled strategy,
is we have a small window for the cooling
schedule that works.


Welsh_and_Powell can be used to quickly find
an upper-bound for a GCP.

"""

def set_goal_colors( k ):
	global goal_number_of_colors
	global goal_average
	goal_number_of_colors = k
	goal_average = edges_matrix[0].size / goal_number_of_colors


def welsh_and_powell():
	colored = np.repeat( False, edges_matrix.shape[0]  )

	colors = np.full((1000,1000),False, dtype=np.bool) 

	active_color = 0

	adjecent_vertices = np.repeat( False, edges_matrix.shape[0] )
	
	while np.any(~colored):
		while np.any(~adjecent_vertices & ~colored):

			largest_degree_uncolored_vertices = np.max(vertices_degree * (~adjecent_vertices & ~colored))
			possible_to_color = (largest_degree_uncolored_vertices == vertices_degree) & (~adjecent_vertices & ~colored)

			potential_next_to_color = np.nonzero(possible_to_color)[0]

			next_to_color = np.random.choice(potential_next_to_color)

			colors[active_color][next_to_color] = True
			colored[next_to_color] = True

			adjecent_vertices[ next_to_color ] = True
			adjecent_vertices[ np.nonzero(edges_matrix[next_to_color])[0] ] = True

		active_color = active_color + 1

		adjecent_vertices = np.repeat( False, edges_matrix.shape[0] )

	return colors[:active_color]

def partial_welsh_and_powell(C):
	colored = np.any(C, axis=0)

	colors = np.full((1000,1000),False, dtype=np.bool)
	colors[:C.shape[0]] = C 

	active_color = C.shape[0]

	adjecent_vertices = np.repeat( False, edges_matrix.shape[0] )
	
	while np.any(~colored):
		while np.any(~adjecent_vertices & ~colored):

			largest_degree_uncolored_vertices = np.max(vertices_degree * (~adjecent_vertices & ~colored))
			possible_to_color = (largest_degree_uncolored_vertices == vertices_degree) & (~adjecent_vertices & ~colored)

			potential_next_to_color = np.nonzero(possible_to_color)[0]

			next_to_color = np.random.choice(potential_next_to_color)

			colors[active_color][next_to_color] = True
			colored[next_to_color] = True

			adjecent_vertices[ next_to_color ] = True
			adjecent_vertices[ np.nonzero(edges_matrix[next_to_color])[0] ] = True

		active_color = active_color + 1

		adjecent_vertices = np.repeat( False, edges_matrix.shape[0] )

	return colors[:active_color]


def partial_dsatur(C):
	C = C.copy()
	colored_vertices = np.any( C,axis=0 )

	uncolored_vertices = np.nonzero( ~colored_vertices )[0]

	saturation = np.array([ np.sum( np.any( C[ :, edges_matrix[u] ] ,axis=1)  ) for u in uncolored_vertices ])
	degree = vertices_degree[ uncolored_vertices ]

	ordered_by_sat = np.argsort( - saturation - degree/(C.shape[1] + 1) )

	need_to_color = np.repeat(True, uncolored_vertices.size)

	while( np.any(need_to_color) ):

		vertex_to_color = uncolored_vertices[ ordered_by_sat ][need_to_color[ordered_by_sat]][0]

		colors_available = np.nonzero( [ np.all( ~edges_matrix[ c,vertex_to_color ] ) for c in C ] )[0]

		if colors_available.size > 0 :
			color_weights = 1 + np.sum( C[ colors_available, :] ,axis=1)**2
			weights = color_weights / np.sum(color_weights)
			random_color = np.random.choice( colors_available, p=weights)
			C[random_color,vertex_to_color] = True
			need_to_color[uncolored_vertices == vertex_to_color] = False 
		else:
			need_to_color[uncolored_vertices == vertex_to_color] = False 

	return C


def random_start():
	W = welsh_and_powell()
	C = W[ np.flip(np.argsort( np.sum(W,axis=1) ) )] 
	return C[:3]

def force_add_random_vertex(C):
	C = C.copy()
	colored_vertices = np.any( C,axis=0 )

	if np.any(~colored_vertices):
		vertices_per_color = np.sum(C,axis=1)
		proposal_weights = np.max(vertices_per_color) - vertices_per_color + 0.2
		skewed_proposal_weights = (proposal_weights / np.max(proposal_weights))**2
		weights = skewed_proposal_weights / np.sum(skewed_proposal_weights)

		uncolored_vertex = np.random.choice( np.nonzero(~colored_vertices)[0] )

		color = np.random.choice( np.arange(C.shape[0]), p=weights )

		C[color] = ~edges_matrix[ uncolored_vertex ] & C[color]
		C[color][uncolored_vertex] = True
		
		return check_average_and_add_row(C)

	return C

def force_add_random_vertex_on_low_used_color(C):
	C = C.copy()
	colored_vertices = np.any( C,axis=0 )

	if np.any(~colored_vertices):
		vertices_per_color = np.sum(C,axis=1)
		proposal_weights = np.max(vertices_per_color) - vertices_per_color + 0.2
		skewed_proposal_weights = (proposal_weights / np.max(proposal_weights))**8
		weights = skewed_proposal_weights / np.sum(skewed_proposal_weights)

		uncolored_vertex = np.random.choice( np.nonzero(~colored_vertices)[0] )

		color = np.random.choice( np.arange(C.shape[0]), p=weights )

		C[color] = ~edges_matrix[ uncolored_vertex ] & C[color]
		C[color][uncolored_vertex] = True
		
		return check_average_and_add_row(C)

	return C

def kempe_chain_swap(C):
	C = C.copy()
	left, right = np.random.choice( np.arange( C.shape[0] ),2, replace=False)
	
	"""
		Select random vertex on the left
	"""
	if np.sum( C[left]) > 0:
		left_conflicts = np.array([np.random.choice( np.nonzero(C[left])[0] )])

		to_the_right = False

		right_conflicts = np.nonzero( C[right])[0][ np.any(edges_matrix[ C[right]][:,left_conflicts], axis=1 ) ]

		new_conflicts = right_conflicts.size > 0

		while new_conflicts:
			if to_the_right:
				new_right_conflicts = np.nonzero( C[right])[0][ np.any(edges_matrix[ C[right]][:,left_conflicts], axis=1 ) ]

				if not new_right_conflicts.size > right_conflicts.size:
					new_conflicts = False

				right_conflicts = new_right_conflicts
			else: 
				new_left_conflicts = np.nonzero( C[left])[0][ np.any( edges_matrix[ C[left]][:,right_conflicts],axis=1 ) ] 

				if not new_left_conflicts.size > left_conflicts.size:
					new_conflicts = False

				left_conflicts = new_left_conflicts
			
			to_the_right = ~to_the_right

		C[left][left_conflicts] = False
		C[right][right_conflicts] = False

		C[left][right_conflicts] = True
		C[right][left_conflicts] = True

		return C

	return C


def parallel_add_random_vertex(C):
	"""
		Stikk need to check average

		alse cost of shuffle
	"""
	C = C.copy()
	np.random.shuffle(C)

	colored_vertices = np.any( C,axis=0 )

	uncolored_count = np.sum(~colored_vertices)
	colors_used = C.shape[0]

	parallel_recolor = np.min([uncolored_count, colors_used])
	colored_vertices = np.any( C,axis=0 )
	
	uncolored_vertices = np.random.choice( np.nonzero(~colored_vertices)[0] , parallel_recolor ,replace=False)


	"""
		Create vector 
	"""

	a_range = np.arange(parallel_recolor)

	proposal = ~edges_matrix[ uncolored_vertices ] & C[:parallel_recolor]
	proposal[ a_range,uncolored_vertices ] = True

	"""
		Old / new with extra dimension
	"""

	stacked_coloring = np.stack([C[:parallel_recolor], proposal], axis=0)

	"""
		Accept/reject true/false
	"""

	same_or_better = np.sum(proposal, axis=1) >= np.sum(C[:parallel_recolor], axis=1)
	same_or_better_index = (1 * same_or_better)

	"""
		Reutnr only if bigger or same
	"""

	best_of_both = stacked_coloring[ same_or_better_index.reshape(1,-1), a_range, :][0] 
	C[:parallel_recolor] = best_of_both

	return check_average_and_add_row(C)


def massive_try_single_vertex(C):
	C = C.copy()
	colored_vertices = np.any( C,axis=0 )

	if np.any(~colored_vertices):
		uncolored_vertices = np.nonzero(~colored_vertices)[0]
		uncolored_vertex = np.random.choice(uncolored_vertices)

		conflict_in_colors = np.array([ np.sum(edges_matrix[c][:,uncolored_vertex]) for c in C])

		if np.any(conflict_in_colors == 0):
			color_without_conflict = np.nonzero(conflict_in_colors == 0 )[0][0]
			C[color_without_conflict, uncolored_vertex] = True

			return check_average_and_add_row(C)

		if np.any(conflict_in_colors == 1):
			single_conflicts = conflict_in_colors == 1

			random_single_conflict_color = np.random.choice( np.nonzero(single_conflicts)[0] )


			C[random_single_conflict_color] = ~edges_matrix[ uncolored_vertex ] & C[random_single_conflict_color]
			C[random_single_conflict_color][uncolored_vertex] = True
			
			return check_average_and_add_row(C)
	
	return C

def check_free_vertex_recoloring(C):
	C = C.copy()
	np.random.shuffle(C)

	for c in C:
		if np.any( np.all( ~edges_matrix[c],axis=0 ) ):
			vertices_available =  np.all( ~edges_matrix[c],axis=0 )

			if np.sum( c ) != np.sum(vertices_available):
				extra_vertex = vertices_available & ~c
				free_vertex = np.random.choice( np.nonzero(extra_vertex)[0] )
				C[:,free_vertex] = False
				c[free_vertex] = True

				break
	return C

def clean_unused_colors(C):
	used = np.sum(C,axis=1) > 0
	C = C[used]

def check_average_and_add_row(C):
	C = C.copy()
	colors_used = C.shape[0]
	vertices_colored = np.sum(C)
	average_vertices = vertices_colored / colors_used

	colored = np.sum(C)

	if average_vertices >= goal_average and colored < C.shape[1]:

		new_color = np.repeat( False, C.shape[1] )
		colored_vertices = np.any( C,axis=0 )
		uncolored_vertex = np.random.choice( np.nonzero(~colored_vertices)[0] )
		new_color[uncolored_vertex] = True

		C = np.concatenate( [C,new_color.reshape(1,-1)] )
		return C

	return C

def check_valid_coloring(C):
	if np.sum(C) < C.shape[1]:
		return False
	for c in C:
		if np.any( edges_matrix[c,:][:,c] ):
			return False
	return True 


def squared_sum_of_classes(C):
	clean_unused_colors(C)
	sum_of_squared_classes = np.sum( np.sum(C,axis=1)**class_exponent )
	return -sum_of_squared_classes


def fill_the_gaps(C):
	pass
	"""Idea to calculate gaps for each color and minimize gaps"""

def squared_classes(C):
	max_value = 10**6 * (1 + goal_number_of_colors)
	colors_used = C.shape[0]
	sum_of_squared_classes = np.sum(np.sum(C,axis=1)**class_exponent)
	all_vertices_colored = np.sum(C) == C.shape[1]
	return max_value - (10**6 * colors_used) - sum_of_squared_classes - (10**6 * all_vertices_colored)

def objective_function(C):
	"""
		Cost that represent the number of 
		colors still need to be aded to reach goal.

		Neighbors only add color if average
		vertices/color is high enough to reach goal.

	"""
	max_value = goal_number_of_colors
	colors_used = C.shape[0]
	vertices_colored = np.sum(C)
	average_vertices = vertices_colored / colors_used

	return 1000 * (1 + max_value - colors_used - average_vertices/goal_average)
