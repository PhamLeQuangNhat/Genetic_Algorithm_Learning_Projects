from bisection import Bisection
import argparse
import numpy as np 

def option():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--times", type = int,default=10,
                                    help="run_multiple_times in 1 Bisection")

    ap.add_argument("-m", "--mssv", type = int, required=True, help="MSSV")

    ap.add_argument("-p", "--problem",type=str, required=True, help="Type Problem")

    ap.add_argument("-c", "--crossover",type=str, required=True,help="Type cross_over")    

    ap.add_argument("-n", "--tournament", type = int, default=4, help="Tournament Size")
    args = vars(ap.parse_args())
    return args

def run_Bisections(times_bisections, times, seed, type_problem, type_crossover, problem_size,tournament_size):
    evals = []
    MRPS = []
    
    for i in range(times_bisections):
        
        print("RUN BISECTION WITH RANDOM_SEED: == {}.format(seed)")
        
        bi = Bisection(times, seed, type_problem, type_crossover, problem_size,tournament_size)
        
        e, m, success = bi.run()
        
        path_file_eval = "Data/Eval/" + type_problem + "_" + type_crossover + "_" + str(problem_size) + ".txt"
        path_file_mrps = "Data/MRPS/" + type_problem + "_" + type_crossover + "_" + str(problem_size) + ".txt"
        
        with open( path_file_eval, 'a') as f:
            f.write(str(e) + " ")

        with open( path_file_mrps, 'a') as f:
            f.write(str(m) + " ")
        
        if success:
            evals.append(e)
            MRPS.append(m)
            seed += 10

    return evals, MRPS, True

def main():
    args = option()
    problems_size = [10,20,40,80,160]

    times_bisections = 10

    for i in problems_size:
        print("BEGIN EXPERIMENT : Type Problem _ {} , Type Cross_over _ {}, Problem_size _ {}".
                format(args["problem"], args["crossover"], i))

        evals, MRPS, success = run_Bisections(times_bisections, args["times"], args["mssv"], 
                            args["problem"], args["crossover"], i, args["tournament"])

        print("evals: ={}".format(evals))
        eval_std = np.std(evals)
        print("----> avg evals: {} with std of {}".format(np.mean(evals),eval_std))

        print("MRPS: = {}".format(MRPS))
        mrps_std = np.std(MRPS)
        print("----> avg MRPS: {} with std of {}".format(np.mean(MRPS),mrps_std))

if __name__ == "__main__":
    main()