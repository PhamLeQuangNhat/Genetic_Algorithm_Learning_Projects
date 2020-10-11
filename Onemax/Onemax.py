import numpy as np 
import random 

# Uniform Crossover
def uniform_cross_over(parent_x, parent_y, rate):

    offspring_1 = parent_x.copy()
    offspring_2 = parent_y.copy()

    length = len(parent_x)

    for i in range(length):
        random_rate = random.random()
        #print(random_rate)
        if random_rate < rate:
        
            offspring_1[i], offspring_2[i] = parent_y[i], parent_x[i]
    
    return offspring_1, offspring_2

# Single Point  Crossover
def single_point_cross_over(parent_x, parent_y):

    offspring_1 = parent_x.copy()
    offspring_2 = parent_y.copy()

    # generating the random number to perform crossover 
    length = len(parent_x)
    length_random = length - 1
    cross_point = random.randint(0, length_random)
    #print(cross_point)

    # interchanging the genes 
    for i in range(cross_point, length):
        offspring_1[i], offspring_2[i] = parent_y[i], parent_x[i]
    
    return offspring_1, offspring_2

class OneMaxProblem:
    def __init__(self, seed, type_problem, type_crossover, population_size,problem_size,tournament_size, number_of_evaluations):
        self.seed = seed
        self.type_problem = type_problem
        self.type_crossover = type_crossover
        self.population_size = population_size
        self.problem_size = problem_size
        self.tournament_size = tournament_size
        self.number_of_evaluations = number_of_evaluations
        self.population = []
    
    """ Initialize populattion Step"""

    def initialize_population(self):

        popu1 = np.zeros(shape=(self.population_size//2,self.problem_size),dtype=int)
        popu2 = np.ones(shape=(self.population_size//2,self.problem_size),dtype=int)

        self.population = np.concatenate((popu1 , popu2),axis=0)
        random.seed(self.seed)
        np.random.seed(self.seed)

        for i in range(self.problem_size):
            np.random.shuffle(self.population[:,i])
        #return self.population
    
    """Cross over Step """

    def cross_over(self):
        offspring = []

        if self.type_crossover == "1X":

            for i in range(0,self.population_size,2):

                offspring_1, offspring_2 = single_point_cross_over(self.population[i],self.population[i+1])
                offspring.append(offspring_1)
                offspring.append(offspring_2)
            return np.array(offspring)

        elif self.type_crossover == "UX":
            rate = 0.5
            for i in range(0,self.population_size,2):

                offspring_1, offspring_2 = uniform_cross_over(self.population[i],self.population[i+1],rate)
                offspring.append(offspring_1)
                offspring.append(offspring_2)

            return np.array(offspring)
    
    """ POOL Step """
    def pool_POP(self, offspring):
        combination_population = np.concatenate((self.population, offspring),axis=0)
        return combination_population
    
    """ Tournament Step """

    # Fitness Function
    def fitness(self,chromosome):
        #score_fitness = np.sum(chromosome)
        if self.type_problem == "Normal":
            return np.sum(chromosome)
        elif self.type_problem =="Trap5":
            return False
            # Fix code
            # if score_fitness != len(chromosome):
            #     return len(chromosome) - score - 1 
            # else:
            #     return score_fitness
            
    
    def tournament(self, pool):
        pool_copy = pool.copy()
        times  = self.tournament_size // 2
        selected_population = []
        i = 0
        groups = []
        length_pool = len(pool)
        while i < (len(pool)):
                low = i
                i = i + self.tournament_size
                groups.append((low, i-1))
        #print(groups)
        
        for _ in range(times):
            #print("selected_population_before = {}".format(selected_population))
        
            #print(pool_copy)
        
            for (low, high) in groups:
                index_best_chromosome = -9

                best_fitness = -999
                for i in range(low, high+1):
                    
                    current_fitness = self.fitness(pool_copy[i])
                    
                    if current_fitness > best_fitness:
                        index_best_chromosome = i
                        best_fitness = current_fitness
                        
                selected_population.append(pool_copy[index_best_chromosome].copy())
            
            #print("selected_population = {}".format(selected_population))

        
            np.random.shuffle(pool_copy)
        return np.array(selected_population)
    
    """ Check covergence """
    def check_convergence(self):
   
        N = self.population_size

        for i in range(0, N-1):
            comparison = self.population[i] == self.population[N-1]
            if not comparison.all():
                return False
        return True
    
    """ RUN """
    def run(self):

        # initialize population 
        self.initialize_population()
        #print("population: {}".format(self.population))

        self.number_of_evaluations += self.population_size
        
        while (not self.check_convergence()):
            #print("population: {}".format(self.population))
            
            # cross over
            offspring = self.cross_over()
            #print("offspring = {}".format(offspring))

            self.number_of_evaluations += self.population_size
            #print("number_of_evaluations = {}".format(self.number_of_evaluations))

            # P+O Pool step
            combination_population = self.pool_POP(offspring)
            #print("combination_population = {}".format(combination_population))

            # Tournament selection
            selected_population = self.tournament(combination_population)
            #print("selected_population = {}".format(selected_population))
        
            # Update the population
            self.population = selected_population.copy()
        return self.number_of_evaluations, self.population
"""     
if __name__ == "__main__":
    Problem =OneMaxProblem(18520120,"Normal","UX",4,10,4,0)
    number_of_evaluations,population = Problem.run()
    print("------- Finsh ----------------")
    print("number_of_evaluations = {}".format(number_of_evaluations))
    print("population = {}".format(population))
"""


            

