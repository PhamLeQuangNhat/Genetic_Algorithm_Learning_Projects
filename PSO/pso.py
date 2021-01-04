import numpy as np
import numpy.random as np_rand

from time import sleep
import matplotlib.pyplot as plt
from function_list import *

class PSO():
	def __init__(self, func, n_parts, n_dims, topo="star", minimise=True,track=False):
		self.minimise = minimise
		self.func = func['score']
		self.name_func = func['name']
		self.cnt = n_parts
		self.w_inertia = 0.7298
		self.w_nostalgia = 1.49618
		self.w_societal = 1.49618
		self.topo = topo 
		self.lower_bounds, self.upper_bounds = func['search_domain'][0], func['search_domain'][1]

		if np.any(self.lower_bounds >= self.upper_bounds):
			raise ValueError("All lower bounds must be < upper bounds")

		self.n_parts = n_parts
		self.n_dims = n_dims

		if self.upper_bounds == inf:
			self.pos = np_rand.random_sample((self.n_parts, self.n_dims))
		else:
			self.pos = np_rand.uniform(self.lower_bounds, self.upper_bounds,
										(self.n_parts, self.n_dims))
		self.pbest = self.pos.copy()

		if self.upper_bounds == inf:
			self.vel = np_rand.random_sample((self.n_parts, self.n_dims))
		else:
			self.vel = np_rand.uniform(- (self.upper_bounds - self.lower_bounds),
										self.upper_bounds - self.lower_bounds,
										(self.n_parts, self.n_dims))
		
		self._eval_perf()
		self.pbest_perf = self.perf.copy()

		if self.minimise:
			self.swarm_best = self.pbest[self.perf.argmin()]
			self.swarm_best_perf = self.pbest_perf.min()
		else:
			self.swarm_best = self.pos[self.perf.argmax()]
			self.swarm_best_perf = self.perf.max()

		self._cache_neighbourhoods(topo)
		print("self.swarm_best = {}".format(self.swarm_best))
		print("self.swarm_best_perf = {}".format(self.swarm_best_perf))
		self.track = track 

		if self.track == True:
			link = 'gif/' + topo + '/' + func['name'] + '/gen_0.csv'
			np.savetxt(link, self.pbest)
		
	def _eval_perf(self):
		self.perf = []
		for i in range(len(self.pos)):
			self.perf.append(self.func(self.pos[i]))
		self.perf = np.array(self.perf)
	
	def _cache_neighbourhoods(self, topo):
		self.topo = topo
		if self.topo == "star":
			return

		n = self.n_parts
		if self.topo == "ring":
			self.neighbourhoods = np.zeros((n, 3), dtype=int)
			for p in range(n):
				self.neighbourhoods[p] = [
					(p - 1) % n,  # particle to left
					p,            # particle itself
					(p + 1) % n   # particle to right
					]
	
	def _velocity_updates(self):

		inertia_vel_comp = self.w_inertia * self.vel
		nostalgia_vel_comp = self.w_nostalgia * np_rand.rand() * \
			(self.pbest - self.pos)
		societal_vel_comp = self.w_societal * np_rand.rand() * \
			(self.best_neigh - self.pos)

		self.vel = inertia_vel_comp + nostalgia_vel_comp + societal_vel_comp
		
	def _box_bounds_checking(self):

		too_low = self.pos < self.lower_bounds
		too_high = self.pos > self.upper_bounds

		self.pos.clip(self.lower_bounds, self.upper_bounds, out=self.pos)

		old_vel = self.vel.copy()
		self.vel[too_low | too_high] *= \
				-1. * np_rand.random((self.vel[too_low | too_high]).shape)

		
	def _tstep(self):

		if self.topo == "ring":
			if self.minimise:
				best_neigh_idx = self.neighbourhoods[np.arange(self.n_parts),self.perf[self.neighbourhoods].argmin(axis=1)]
			else:
				best_neigh_idx = self.neighbourhoods[np.arange(self.n_parts),
					self.perf[self.neighbourhoods].argmax(axis=1)]

			self.best_neigh = self.pos[best_neigh_idx]

		else:

			self.best_neigh = self.swarm_best

		self._velocity_updates()

		self.pos += self.vel
	
		self._box_bounds_checking()
		
		self._eval_perf()
		
		if self.minimise:
			improvement_made_idx = self.perf < self.pbest_perf
		else:
			improvement_made_idx = self.perf > self.pbest_perf


		self.pbest[improvement_made_idx] = self.pos[improvement_made_idx]
		
		self.pbest_perf[improvement_made_idx] = self.perf[improvement_made_idx]
		
		if self.minimise:
			
			self.swarm_best = self.pbest[self.perf.argmin()]
			self.swarm_best_perf = self.pbest_perf.min()
		else:
			self.swarm_best = self.pbest[self.perf.argmax()]
			self.swarm_best_perf = self.pbest_perf.max()
		print("self.swarm_best = {}".format(self.swarm_best))
		print("self.swarm_best_perf = {}".format(self.swarm_best_perf))
		return self.pbest, self.swarm_best, self.swarm_best_perf
	
	def solver(self, max_itr=100):
		self.swarm_best_hist = np.zeros((max_itr, self.n_dims))
		self.swarm_best_perf_hist = np.zeros((max_itr,))
		itr = 0
		
		while itr < max_itr:
			print("===============================Iter {}================================".format(itr+1))
			self.pbest, self.swarm_best_hist[itr], self.swarm_best_perf_hist[itr] = self._tstep()
			if self.track == True:
				link = 'gif/' + self.topo +'/' + self.name_func + '/gen_' + str(itr+1) + '.csv'
				np.savetxt(link, self.pbest)
				link_2 = 'gif/' + self.topo +'/' + self.name_func + '/final.txt'
				if itr == 48:
					with open(link_2,'w') as f:
						f.write("Position: {} - Objective_value: {}".format(self.swarm_best,self.swarm_best_perf))
			self.cnt += self.n_parts

			if self.cnt > 10**6:
				return self.pbest, self.swarm_best, self.swarm_best_perf
			if np.array(self.pbest_perf).std() < 0.00001:
				return self.pbest, self.swarm_best, self.swarm_best_perf
			itr += 1

		return self.pbest, self.swarm_best, self.swarm_best_perf


	