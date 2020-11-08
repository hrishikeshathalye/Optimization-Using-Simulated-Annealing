import networkx as netx
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
from collections import OrderedDict
import numpy as np
import random
import math

initialTemp = 0
finalTemp = 0
alpha = 0
history = []
color_map = []
pos = 0

def probFunction(cost, temp):
	return 1/(1+np.exp(-cost/temp))

def accept(cost, temp):
	if(cost == 0):
		return 1
	elif(random.random()<=probFunction(cost, temp)):
		return 1
	return 0

def generateNode(visitedColors, nodeList):
	unvisited = []
	for i in nodeList:
		if(i not in visitedColors.keys()):
			unvisited.append(i)
	return random.choice(unvisited)

#Welsh Powell Heuristic on which SA will be used
def welshPowellHeuristicWithSA(G):
	global history
	#sorting the nodes based on its degree
	temp = initialTemp
	nodeList = G.nodes()
	visitedColors = OrderedDict() #dictionary to store the colors assigned to each node
	history = []
	tmp = []
	sa_on = 1
	remNodes = list(set(nodeList) - set(visitedColors.keys()))
	remNodes = sorted(remNodes, key =lambda x:len(list(G.neighbors(x))))
	while( (len(visitedColors)!=len(nodeList))):
		if(sa_on):
			range_end = 1+math.ceil(temp/10)
		else:
			range_end = len(remNodes)
		for i in range(0, range_end):
			node = remNodes[i%len(remNodes)]
			available = set(range(len(G.nodes())))
			for adj_node in G.neighbors(node): 
				if adj_node in visitedColors.keys():
					col = visitedColors[adj_node]
					available = available - set([col])
			clr = list(available)[0]
			if(clr in visitedColors.values()):
				visitedColors[node] = clr
			else:
				if(sa_on==0 or accept(1, temp)):
					visitedColors[node] = clr
			visitedColors = OrderedDict(sorted(visitedColors.items(), key=lambda x: x[0]))
			tmp = []
			for i in range(len(nodeList)):
				if(i in visitedColors.keys()):
					tmp.append(visitedColors[i])
				else:
					tmp.append(0)
			if(len(history)==0 or tmp!=history[-1]):
				history.append([i for i in tmp])
			remNodes = list(set(nodeList) - set(visitedColors.keys()))
			remNodes = sorted(remNodes, key =lambda x:len(list(G.neighbors(x))))
			if(len(visitedColors)==len(nodeList)):
				break
		temp*=alpha
		if(temp-0.0001<finalTemp):
			sa_on = 0

	return visitedColors

def CreateGraph():
	G = netx.Graph()
	f = open('graph.txt')
	n = int(f.readline())
	for i in range(n):
		graph_edge_list = f.readline().split()
		G.add_edge(int(graph_edge_list[0]), int(graph_edge_list[1])) 
	return G

def update():
	for h in history:
		yield h

color_map = update()

def update_frame(frames):
	global G, pos
	plt.cla()
	c_map = next(color_map, list(colorValues.values()))
	netx.draw(G, pos, with_labels = True,nodelist=sorted(G.nodes()) ,node_color = c_map, edge_color = 'black' ,width = 1, font_color='white', alpha=0.9)

if __name__ == "__main__":
	mode = input("Mode - Random Graph (r) / From File (f):\n")
	if(mode == "r"):
		numNodes =int(input("Enter Number Of Nodes:\n"))
	initialTemp = float(input("Enter Starting Temperature:\n"))
	finalTemp = float(input("Enter Final Temperature:\n"))
	alpha = float(input("Enter Cooling Rate:\n"))
	if(mode == "f"):
		G = CreateGraph()
	else:
		G = netx.gnp_random_graph(numNodes,0.5)
	colorValues = welshPowellHeuristicWithSA(G)
	print("Node Colors Obtained: ", colorValues)
	print("Number Of Colors Needed: ", len(set(colorValues.values())) )
	pos = netx.spring_layout(G)
	ani = matplotlib.animation.FuncAnimation(plt.gcf(), update_frame, frames=len(history), interval=500, repeat=False)
	manager = plt.get_current_fig_manager()
	manager.window.showMaximized()
	plt.show()
