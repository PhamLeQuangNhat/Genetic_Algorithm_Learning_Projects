import math
import numpy as np

def Rastrigin(particle):
    res = 10*len(x)
    for i in range(len(x)):
        res += (x[i]**2 - 10 * np.cos(2 * np.pi * x[i]))
    return res

def RosenBrock(particle):
    x = np.array(x)
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)

def Ackley(particle):
    part_1 = -0.2*math.sqrt(0.5*(pos[0]*pos[0] + pos[1]*pos[1]))
    part_2 = 0.5*(math.cos(2*math.pi*pos[0]) + math.cos(2*math.pi*pos[1]))
    value = math.exp(1) + 20 -20*math.exp(part_1) - math.exp(part_2)
    return value

def Eggholder(particle):
    return (-(particle[1] + 47) * np.sin(np.sqrt(abs(x[0]/2 + (x[1]  + 47)))) -x[0] * np.sin(np.sqrt(abs(x[0] - (x[1]  + 47)))))