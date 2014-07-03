# -*- coding: utf-8 -*-
"""
Created on Thu May 29 14:32:13 2014

@author: ankur
"""
import json
#import math
import networkx as nx
#import matplotlib.pyplot as plt
import random,copy

'''
def config():
        with open('data.json') as data_file:
                data = json.load(data_file)
        return data
'''


MAX_NODE_LOOKUP = 13  
class CFindPath:
    
    def __init__(self,data):
        
	self.G = nx.Graph()
 	self.data = data
    	for k, v in data.items():
		i = int(data[k]["x"])
		j = int(data[k]["y"])
        	self.G.add_node(k,pos=(i,j),visited=False)
        	for key,value in v.items():
            		if  value != "-1" and key!="x" and key!="y" and key!="type":        
               			self.G.add_edge(k,value,weight=1)  
	self.pos=nx.get_node_attributes(self.G,'pos')

	#sorry for hard coding but thats how scatter function for the ghost is implemented
        self.corners = ['92','71','250','229']	

	self.flip = 1
	self.scatterMode = True    



    #using this to mark nodes as visited
    def getNewScoreDict(self):
	return	nx.get_node_attributes(self.G,'visited')



    #A* path finding
    def findPathAstar1(self,source,destination):
	    
	    #check scatter mode, change the destination and set scatterMode to false again
	    if (self.scatterMode == True):
		print "---------------in scatter mode-------------------------------"
	        destination = self.corners[random.randrange(0,4)]
	    	
	
	    path = nx.astar_path(self.G,source,destination,self.heuristics1)
	    #return the path's next index other than 0, if not then return 0 itself
	    if(len(path)>1):
		    return path[1]
	    else: 
		    return path[0]


    #A* with 4th position indexed
    def findPathAstar2(self,source,destination):
	for i in range(0,4):
	    key = [k for k,v in self.data[destination].items()if v!= "-1" and k != "x" and k!="y" and k!="type"]
	    index = random.randrange(0,len(key))
	    destination = self.data[destination][key[index]]
	
	path = nx.astar_path(self.G,source,destination,self.heuristics2)
	if(len(path)>1):
	    return path[1]
	else: 
	    return path[0]



    def findPathDijkstra(self,source,destination):
        if self.flip == 1:
	    for i in range(0,4):
	        key = [k for k,v in self.data[destination].items()if v!= "-1" and k != "x" and k!="y" and k!="type"]
	        index = random.randrange(0,len(key))
	        destination = self.data[destination][key[index]]
	    
	self.flip *= -1
	path = nx.dijkstra_path(self.G,source,destination)
	return path



    def findPathScattered(self,source,destination):
	    path = nx.astar_path(self.G,source,destination,self.heuristics1)
	    if len(path)< MAX_NODE_LOOKUP:
		#print "recompute the destination as one of the random 4 corners "
		destination = self.corners[random.randrange(0,4)]
		#print "destination", destination
	    	path = nx.astar_path(self.G,source,destination,self.heuristics1)
	    if(len(path)>1):
	        return path[1]
	    else: 
	        return path[0]

    def heuristics1(self,a, b):
        x1, y1 = self.pos[a]
	x2, y2 = self.pos[b]
	return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    
    def heuristics2(self,a, b):
        x1,y1 = self.pos[a]
        x2,y2 = self.pos[b]   
        return (abs(y2-y1) + abs(x2-x1)) 


'''
data = config()
test = CFindPath(data)
#path = test.findPathAstar1("164","123")
#print path
for i in range(0,10):
	path = test.findPathAstar2("164","123")
	print path
#	path = test.findPathDijkstra("164","123")
#	print path

'''
