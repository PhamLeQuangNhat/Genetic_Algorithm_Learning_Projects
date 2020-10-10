class Bisection:

def run_multiple_times(seed, times, _type, population_size, problem_size, tournament_size):
    evals = 0
    for i in range(times):
        result = True
        number_of_evaluations = 0 
        #x = 0
        print("number_of_evaluations before " + str(i)+ "th = {}".format(number_of_evaluations))
        print("Maximizing with random_seed = {}".format(seed))
        #Problem = OneMaxProblem(seed, _type, N, problem_size,tournament_size,number_of_evaluations)
        number_of_evaluations, population = OneMaxProblem(seed, _type, population_size, problem_size, tournament_size, number_of_evaluations)
        #print("number_of_evaluations = {}".format(number_of_evaluations))
        print("number_of_evaluations after " + str(i)+ "th = {}".format(number_of_evaluations))
        print("Population = {}".format(population))
        population = np.unique(population)
        print("Population = {}".format(population))
        print("Len population = {}".format(len(population)))
        if len(population) != 1:
            return 0, False
        evals += number_of_evaluations
        seed += 1

def get_MRPS_upper_bound(seed, _type, problem_size, tournament_size):
    N_upper = 4
    times = 10
    evals, success = run_multiple_times(seed, times, _type, N_upper, problem_size, tournament_size)

    while (not success ):
        N_upper = N_upper * 2
        if N_upper <= 8192:
        
            print("Running N_upper: {}".format(N_upper))

            evals, success = run_multiple_times(seed, times, _type, N_upper, problem_size, tournament_size)
            print("success: {}".foamat(success))
        else:
            return 0,0, False
    return N_upper, evals, success

