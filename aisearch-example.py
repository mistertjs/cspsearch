# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 14:30:51 2016

@author: Administrator
"""
import numpy as np
import networkx as nx
rnd = np.random
from aisearch import AISearch


doExercise = True
# graph type (0,1,2)
graphType = rnd.randint(0,3)
if (doExercise):
    territories = [('WA','NT'),('WA','SA'),('NT','SA'),('NT','Q'),
            ('SA','Q'),('SA','NSW'),('SA','V'),('Q','NSW'),
            ('NSW','V'),('Q','T'),('NSW','T'), ('V','T'),
            ('NT','V')]
            
    # IMPORTANT...W needs to be a DiGraph, if you want the rootNode to be searched
    # for, otherwise you have to specify it
    rootNode = 'WA'
    W=nx.Graph()
    if (rootNode is None):
        W=nx.DiGraph() 
    W.add_edges_from(territories)    
else:
    rootNode = 'WA'
    values = ['WA', 'Q', 'V', 'SA', 'NT', 'NSW', 'T']
    mapping = {}
    idx = 0
    for value in values:
        mapping[idx]=value
        idx += 1
    if(graphType == 0):
        G=nx.path_graph(len(values))
    elif(graphType == 1):
        G=nx.star_graph(len(values)-1)
    elif(graphType == 2):
        G=nx.wheel_graph(len(values)-1)
        
    W=nx.relabel_nodes(G,mapping)
    
search = AISearch()
print search.dfs_recurse(W, rootNode)    
search.plotGraph(W)

'''
###############################################################################
Lattice graph
'''
search = AISearch()

# get true dfs queue
G1,colors,data = search.getLatticeGraph(3,3,directed=True, addColors=True)
search.plotGraph(G1,colors=colors)
print data[1]

G2,colors,data = search.getLatticeGraph(3,3,directed=False, addColors=True)
search.plotGraph(G2,colors=colors)
print data[1]

G3,colors,data = search.getLatticeGraph(3,3,directed=False,reverse=True,addColors=True)
search.plotGraph(G3,colors=colors)
print data[1]

# Depth first search...G1 is true depth first, forward and backwards
print search.dfs_recurse(G1, 'A', discovery=True)
print search.dfs_recurse(G1, 'A', discovery=False)

# Next two have similar results
print search.dfs_recurse(G2, 'A', discovery=True, sort=False)
print search.dfs_recurse(G2, 'A', discovery=False, sort=False)

print search.dfs_recurse(G3, 'A', discovery=True)
print search.dfs_recurse(G3, 'A', discovery=False)