from Onemax import OneMaxProblem
import numpy as np 

class Bisection:
    def __init__(self, times, seed, type_problem, type_crossover, problem_size,tournament_size):
        self.times = times
        self.seed = seed
        self.type_problem = type_problem
        self.type_crossover = type_crossover
        self.problem_size = problem_size
        self.tournament_size = tournament_size
        
    def run_multiple_times(self, population_size):
        sum_evals = 0
        seed = self.seed
        for i in range(self.times):

            number_of_evaluations = 0 
            
            print("number_of_evaluations before " + str(i)+ "th = {}".format(number_of_evaluations))
            print("Maximizing with random_seed = {}".format(seed))
            #Problem = OneMaxProblem(seed, _type, N, problem_size,tournament_size,number_of_evaluations)
            Problem = OneMaxProblem(seed, self.type_problem, self.type_crossover, population_size,
                                     self.problem_size, self.tournament_size, number_of_evaluations)
            number_of_evaluations, population = Problem.run()
            #print("number_of_evaluations = {}".format(number_of_evaluations))
            print("number_of_evaluations after " + str(i)+ "th = {}".format(number_of_evaluations))
            #print("Population = {}".format(population))
            population = np.unique(population)
            #print("Population = {}".format(population))
            #print("Len population = {}".format(len(population)))
            if len(population) != 1:
                return 0, False
            sum_evals += number_of_evaluations
            seed += 1
        return sum_evals/self.times, True

    def get_MRPS_upper_bound(self):
        N_upper = 4
        
        evals, success = self.run_multiple_times(N_upper)

        while (not success ):
            N_upper = N_upper * 2
            if N_upper <= 8192:
            
                print("Running N_upper: {}".format(N_upper))

                evals, success = self.run_multiple_times(N_upper)

                print("success: {}".format(success))
            else:
                return 0,0, False
        print("SEED : {}".format(self.seed))
        return N_upper, evals, success
    
    def find_MRPS(self,N_upper, evals_upper):
        evals = evals_upper
        N_lower = N_upper // 2
        while (N_upper - N_lower)/N_upper > 0.1:
            N = (N_upper + N_lower) // 2
            
            x, success = self.run_multiple_times(N)

            print(f'  N_upper: {N_upper} - N_lower: {N_lower} - success: {success} - x: {x}')
            if success:
                N_upper = N
                evals = x
            else:
                N_lower = N
            
            if (N_upper - N_lower) <= 2:
                
                return evals, N_upper
            
        return evals, N_upper

    def run(self):
        N_upper, evals_upper, success = self.get_MRPS_upper_bound()
        #print(N_upper,evals_upper,success)
        
        if not success:
             return 0, 0, False
        evals, MRPS = self.find_MRPS(N_upper, evals_upper)
        
        return evals, MRPS, True

"""
if __name__ == "__main__":
    bi =  Bisection(10,18520120,"OneMax","1X",80,4)
    bi.run()

    #N_upper, evals, success = bi.get_MRPS_upper_bound()
    evals, MRPS, success = bi.run()
    print(evals, MRPS, success)
"""
