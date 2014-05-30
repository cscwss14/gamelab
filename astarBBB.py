# -*- coding: utf-8 -*-
"""
Created on Thu May 29 14:32:13 2014

@author: ankur
"""
#import json
#import math
import networkx as nx
#import matplotlib.pyplot as plt

'''
def config():
        with open('data.json') as data_file:
                data = json.load(data_file)
        return data
'''
    
  
class CFindPath:
    
    def __init__(self,data):
        
	self.G = nx.Graph()
 
    	for k, v in data.items():
		i = int(data[k]["x"])
		j = int(data[k]["y"])
        	self.G.add_node(k,pos=(i,j))
        	for key,value in v.items():
            		if  value != "-1" and key!="x" and key!="y" and key!="type":        
               			self.G.add_edge(k,value,weight=1)  
	self.pos=nx.get_node_attributes(self.G,'pos')

    def findPath(self,source,destination):
	    path = nx.astar_path(self.G,source,destination,self.dist)
	    #Lets return next 3 indexes as we will have to compute it back again
	    return path

    def dist(self,a, b):
        x1, y1 = self.pos[a]
	x2, y2 = self.pos[b]
	return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
'''    
data = config()
test = CFindPath(data)
path = test.findPath("164","123")
print path
#nx.draw(test.G)
#nx.draw(test.G,nodelist=path,node_color = 'g')
#plt.show()    
'''
