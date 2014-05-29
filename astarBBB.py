# -*- coding: utf-8 -*-
"""
Created on Thu May 29 14:32:13 2014

@author: ankur
"""

import math
import networkx as nx
import matplotlib.pyplot as plt

    
  
class CFindPath:
    
    def __init__(self,data):
        
	self.G = nx.Graph()
	#need to add the position data also, 
	#only if some smart ass merges the pixelinfo and data.json together ,PROPERLY
 
    	for k, v in data.items():
        	self.G.add_node(k)
        	for key,value in v.items():
            		if  value != "-1":          
               			self.G.add_edge(k,value,weight=1)  


    def findPath(self,source,destination):
	    path = nx.astar_path(G,source,destination)
	    #Lets return next 3 indexes as we will have to compute it back again
	    return path

    def heuristic():
    
    	#only if I could put position data, 
        #only if some smart ass could merge the two files together, PROPERLY
	return
    

