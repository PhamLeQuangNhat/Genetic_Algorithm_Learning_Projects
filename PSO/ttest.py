import numpy as np
import matplotlib.pyplot as plt
from function_list import *
from scipy.stats import ttest_ind
import re

funcs = ['RosenBrock', 'Rastrigin']

for func in funcs:
    print("********************************************")
    print("func = {} ". format(func))
    for N in [128, 256, 512, 1024, 2048]:
        print("_____________________________________________")
        res_star = []
        res_ring = []

        link_1 = 'log/ring/' + func + '_' +  str(N) + '.txt'
        link_2 = 'log/star/' + func + '_' +  str(N) + '.txt'
        with open(link_1, 'r') as fi:
            for line in fi:
                m = re.search(r'(?<= - )(.*?)(?= - )',line)
                if m != None:
                    res_ring.append(float(m.group(0)))
        print(" res_ring = {}".format(res_ring))
        print (" ")
        with open(link_2, 'r') as fi:
            for line in fi:
                m = re.search(r'(?<= - )(.*?)(?= - )',line)
                if m != None:
                    res_star.append(float(m.group(0)))
        print(" res_start = {}".format(res_star))
        print (" ")
        print(" N = {} - ttest {} ".format(N, ttest_ind(res_ring, res_star)))
        print (" ")
