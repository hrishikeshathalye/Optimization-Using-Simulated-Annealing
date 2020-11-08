import networkx as netx
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
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
def welshPowellHeuristic(G):
	global history
	#sorting the nodes based on its degree
	temp = initialTemp
	nodeList = sorted(G.nodes(), key =lambda x:len(list(G.neighbors(x))) )
	visitedColors = {} #dictionary to store the colors assigned to each node
	startNode = generateNode(visitedColors, nodeList)
	visitedColors[startNode] = 0 #assign the first color to the first node
	history.append(list(visitedColors.values()) + [1]*(len(nodeList)-1))
	while( (len(visitedColors)!=len(nodeList)) and temp-0.0001>finalTemp ):
		for i in range(0, 1+math.ceil(temp/10)):
			node = generateNode(visitedColors, nodeList)
			available = [True] * len(G.nodes()) #boolean list[i] contains false if the node color 'i' is not available
			#iterates through all the adjacent nodes and marks it's color as unavailable, if it's color has been set already
			for adj_node in G.neighbors(node): 
				if adj_node in visitedColors.keys():
					col = visitedColors[adj_node]
					available[col] = False
			clr = 0
			for clr in range(len(available)):
				if available[clr] == True:
					break
			if(clr in visitedColors.values()):
				visitedColors[node] = clr	
			else:
				if(accept(1, temp)):
					visitedColors[node] = clr
			history.append(list(visitedColors.values()) + [1]*(len(nodeList) - len(visitedColors)))
			if(len(visitedColors)==len(nodeList)):
				break
		temp*=alpha
	
	return visitedColors

def CreateGraph():
	G = netx.Graph()
	f = open('graph.txt')
	n = int(f.readline())
	for i in range(n):
		graph_edge_list = f.readline().split()
		G.add_edge(graph_edge_list[0], graph_edge_list[1]) 
	return G

def update():
	for h in history:
		yield h

color_map = update()

def update_frame(frames):
	global G, pos
	plt.cla()
	c_map = next(color_map, list(colorValues.values()))
	netx.draw(G, pos, with_labels = True, node_color = c_map, edge_color = 'black' ,width = 1, font_color='white')

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
	colorValues = welshPowellHeuristic(G)
	print("Node Colors Obtained: ", colorValues)
	print("Number Of Colors Needed: ", len(set(colorValues.values())) )
	pos = netx.spring_layout(G)
	ani = matplotlib.animation.FuncAnimation(plt.gcf(), update_frame, frames=len(history), interval=100, repeat=False)
	plt.show()
