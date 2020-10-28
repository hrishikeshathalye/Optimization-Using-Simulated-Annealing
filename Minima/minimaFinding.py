import random
import numpy as np
from numpy import (
power, sqrt, log, sin, sinh, cos, 
cosh, tan, tanh, arcsin, arccos, 
arctan, arcsinh, arccosh, arctanh
)
import matplotlib.pyplot as plt
import matplotlib.animation as animation
x_min = 0
x_max = 0
x = []
y = []
x_init = 0
y_init = 0
moves = []
moveIndex = 0

def init_plotter(f, start, domainStart, domainEnd):
    global x_min, x_max, x, y, x_init, y_init
    x_min = domainStart
    x_max = domainEnd
    x = np.linspace(x_min, x_max, 20000)
    y = f(x)
    x_init = start # Starting point
    y_init = f(x_init)

def animate(i, line, scat, text):
    global moves
    global moveIndex
    try:
        nextx = moves[moveIndex][0]
    except IndexError:
        print(i)
        return
    nexty = moves[moveIndex][1]
    moveIndex+=1
	# Update the plot
    scat.set_offsets([[nextx,nexty]])
    text.set_text("Value : %.5f" % nexty)
    line.set_data(x, y)
    return line, scat, text

def visualiser():
    fig, ax = plt.subplots()
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([-3, 3])
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    plt.title("Simulated Annealing")
    line, = ax.plot([], [])
    line.set_data([], [])
    scat = ax.scatter([], [], c="red")
    text = ax.text(0,2.5,"")

    ani = animation.FuncAnimation(fig, animate, fargs = (line, scat, text), interval=100, blit=True)

    plt.show()

def probFunction(cost, temp):
    # print(cost)
    # print(temp)
    return 1/(1+np.exp(-cost/temp))

def optima_solver(f, step, initTemp, finalTemp, reductionRule):
    global moves
    curr = -1.57
    temp = initTemp
    while(temp>finalTemp):
        # print(temp, curr)
        currcost = f(curr)
        moves.append((curr, currcost))
        if(random.randint(0, 1)):
            nextcost = f(curr-step)
            next = curr-step
        else:
            nextcost = f(curr+step)
            next = curr+step
        if(nextcost>=currcost):
            curr = next
        else:
            p = probFunction(nextcost-currcost, temp)
            # print(p)
            if(random.random()<=p):
                curr = next
        temp-=0.1
        # print(temp)
    moves.append((curr, f(curr)))
    return f(curr)

if __name__ == "__main__":
    exprStr = input("Enter y as a function of x:\n")
    f = lambda x: eval(exprStr)
    # mode = input("Mode (Maxima/Minima):\n").lower()
    # print("Set Following Parameters:")
    # domainStart = int(input("Domain Start:\n"))
    # domainEnd = int(input("Domain End:\n"))
    print(optima_solver(f, 0.5, 100, 0, "abc"))
    init_plotter(f, 0, -7, 7)
    visualiser()