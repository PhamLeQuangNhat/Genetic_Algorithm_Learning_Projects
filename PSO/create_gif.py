from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from pso import *
from function_list import *

def animate(i,ln, ax, name):
    res = []
    link = name + str(i) +".csv"
    with open(link) as fi:
        for line in fi:
            li = np.array([0,0], dtype='float64')
            li[0],li[1] = map(float,line.split())
            res.append(li)
        res = np.array(res)
    xdata = res[:,0]
    ydata = res[:,1]
    ax.set_title(f'GEN {i + 1}')
    ln.set_data(xdata, ydata)
    return ln,

function_list = [Rastrigin, RosenBrock, Ackley, Eggholder]
topos = ['ring', 'star']

for topo in topos:
    for func in function_list:
        if func == Rastrigin:
            name = 'Rastrigin'
        elif func == RosenBrock:
            name = 'RosenBrock'
            func['search_domain'][0] =  -1
            func['search_domain'][1] = 2
        elif func == Ackley:
            name = 'Ackley'
        elif func == Eggholder:
            name = 'Eggholder'

        name = 'gif/'+ topo + '/' + name + '/gen_' 

        xlist = np.linspace(func['search_domain'][0], func['search_domain'][1], 100)
        ylist = np.linspace(func['search_domain'][0], func['search_domain'][1], 100)
        X, Y = np.meshgrid(xlist, ylist)
        
        if func == Rastrigin:
            Z = (X**2 - 10 * np.cos(2 * 3.14 * X)) + \
                (Y**2 - 10 * np.cos(2 * 3.14 * Y)) + 20
        elif func == RosenBrock:
            Z = (1.-X)**2 + 100.*(Y-X*X)**2
        elif func == Ackley:
            a = 20
            b = 0.2
            c = 2 * np.pi
            sum_sq_term = -a * np.exp(-b * np.sqrt(X*X + Y*Y) / 2)
            cos_term = -np.exp((np.cos(c*X) + np.cos(c*Y)) / 2)
            Z = a + np.exp(1) + sum_sq_term + cos_term
        elif func == Eggholder:
            Z = -(Y + 47) * np.sin(np.sqrt(abs(X/2 + (Y + 47)))) -X * np.sin(np.sqrt(abs(X - (Y + 47))))

        fig,ax=plt.subplots(1,1)
        cp = ax.contourf(X, Y, Z)
        ln, = plt.plot([], [], 'ro')
        ani = FuncAnimation(fig, animate, fargs = (ln, ax, name),  frames=50, blit=True,interval=500)

        link_save = "gif/" + func['name'] + "_" + topo +".gif"
        ani.save(link_save)
