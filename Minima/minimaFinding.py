import random
import numpy as np
from numpy import (
power, sqrt, log, sin, sinh, cos, 
cosh, tan, tanh, arcsin, arccos, 
arctan, arcsinh, arccosh, arctanh
)
import matplotlib.pyplot as plt
import matplotlib.animation as animation
y_min = 0
y_max = 0
x = []
y = []
x_init = 0
y_init = 0
moves = []
moveIndex = 0
ani = 0
domainStart = 0
domainEnd = 0

def init_plotter(f, start):
    global x, y, x_init, y_init
    x = np.linspace(domainStart, domainEnd, 2000)
    y = f(x)
    x_init = start # Starting point
    y_init = f(x_init)

def animate(i, line, scat, text):
    global moves, moveIndex, ani
    try:
        nextx = moves[moveIndex][0]
    except IndexError:
        ani.event_source.stop()
    else:
        nexty = moves[moveIndex][1]
        moveIndex+=1
        # Update the plot
        scat.set_offsets([[nextx,nexty]])
        text.set_text("Value : %.5f" % nexty)
        line.set_data(x, y)
        return line, scat, text

def visualiser():
    global ani
    fig, ax = plt.subplots()
    ax.set_xlim([domainStart-0.5, domainEnd+0.5])
    ax.set_ylim([y_min-0.5, y_max+0.5])
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    plt.title("Simulated Annealing")
    line, = ax.plot([], [])
    line.set_data([], [])
    scat = ax.scatter([], [], c="red")
    text = ax.text((domainStart+domainEnd)/2,y_max+0.25,"")

    ani = animation.FuncAnimation(fig, animate, fargs = (line, scat, text), interval=50, blit=False)

    plt.show()

def probFunction(cost, temp):
    return 1/(1+np.exp(-cost/temp))

def optima_solver(f, initTemp, finalTemp, mode, innerIter):
    global moves, x_init, y_min, y_max
    curr = random.random()*(domainEnd-domainStart) + domainStart
    init_plotter(f, curr)
    temp = initTemp
    y_min = f(domainStart)
    y_max = f(domainEnd)
    if(y_min>y_max):
        tmp = y_min
        y_min = y_max
        y_max = tmp
    while(temp>finalTemp):
        # print(temp, curr)
        for i in range(0, innerIter):
            currcost = f(curr)
            y_min = min(currcost, y_min)
            y_max = max(currcost, y_max)
            moves.append((curr, currcost))
            if(random.randint(0, 1)):
                if(curr-step<domainStart):
                    continue
                nextcost = f(curr-step)
                next = curr-step
            else:
                if(curr+step>domainEnd):
                    continue
                nextcost = f(curr+step)
                next = curr+step
            if(nextcost>=currcost and mode=="maxima"):
                curr = next
            elif(nextcost<=currcost and mode=="minima"):
                curr = next
            else:
                p = probFunction(nextcost-currcost, temp)
                # print(p)
                if(random.random()<=p):
                    curr = next
        temp*=0.8
    y_min = min(f(curr), y_min)
    y_max = max(f(curr), y_max)
    moves.append((curr, f(curr)))
    return (curr, f(curr))

if __name__ == "__main__":
    exprStr = input("Enter y as a function of x:\n")
    f = lambda x: eval(exprStr)
    mode = input("Mode (Maxima/Minima):\n").lower()
    print("Set Following Parameters:")
    domainStart = float(input("Domain Start:\n"))
    domainEnd = float(input("Domain End:\n"))
    initialTemp = float(input("Initial Temperature:\n"))
    finalTemp = float(input("Final Temperature:\n"))
    innerIter = int(input("No of times to run inner loop:\n"))
    # alpha = float(input("Temperature step size:\n")
    step = float(input("Step size:\n"))
    print("(x,y) For Optima:")
    print(optima_solver(f, initialTemp, finalTemp, mode, innerIter))
    visualiser()