import numpy as np
import matplotlib.pyplot as plt
from pso import *
from function_list import *


dims = [2,10]
func_10 = ['Rastrigin','RosenBrock'] 
func_2  = ['Rastrigin', 'RosenBrock','Ackley','Eggholder'] 
topos = ['star','ring']
problem_sizes = [128, 256, 512, 1024, 2048]

for dim in dims:
	if dim == 10:
		for topo in topos:
			for func in func_10:
				if func == 'Rastrigin':
					obj_func = Rastrigin
				elif func == 'RosenBrock':
					obj_func = RosenBrock

				for N in problem_sizes:
					SEED = 18520120
					avg = np.zeros((10,1))

					link_1 = 'log/' + topo + '/' + func + '_' + str(N) + '.txt'
					link_2 = 'log/' + topo + '/' + func + '_final.txt'
					with open(link_1,'w') as f:
						for i in range(10):
							np.random.seed(SEED)
							o = PSO(func=obj_func,  n_parts=N, n_dims = dim,topo=topo)
							pbest, swarm_best, swarm_best_perf = o.solver(1000000)
							print("{} - {} - (SEED: {})\n".format(swarm_best,swarm_best_perf,SEED))
							avg[i] = swarm_best_perf
							f.write("{} - {} - (SEED: {})\n".format(swarm_best,swarm_best_perf,SEED))
							SEED += 1
					with open(link_2,'a+') as f:
						print('N = {} - average: {} - std: {} \n'. format(N, round(avg.mean(), 3), round(avg.std(), 3)))
						f.write('N = {} - average: {} - std: {} \n'. format(N, round(avg.mean(), 3), round(avg.std(), 3)))

	elif dim == 2:
		for topo in topos:
			for func in func_2:
				if func == 'Rastrigin':
					obj_func = Rastrigin
				elif func == 'RosenBrock':
					obj_func = RosenBrock
				elif func == 'Ackley':
					obj_func = Ackley
				elif func == 'Eggholder':
					obj_func = Eggholder

				SEED = 18520120
				np.random.seed(SEED)
				o = PSO(func=obj_func,  n_parts=32, n_dims = dim,topo=topo, track = True)
				pbest, swarm_best, swarm_best_perf = o.solver(49)




  