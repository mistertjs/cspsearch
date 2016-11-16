# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 13:57:17 2016

Uses a lattice graph

Using Arc Consistency, this example never seems to back track with a lattic

This example uses:
constraint: default ValueInequality
algorithms: Arc Consistency

Setting cspAlgorithm=None will use basic forward checking and take much
longer to run

@author: Administrator
"""

import numpy as np
rnd = np.random
import networkx as nx
from aisearch import AISearch
from cspbacktracking import CSPBacktracking
from cspbacktracking import CSPAlgorithms

doExercise = False
        
# generate test graph (directed lattice mxn)   
search = AISearch()
if (doExercise):
    territories = [('WA','NT'),('WA','SA'),('NT','SA'),('NT','Q'),
        ('SA','Q'),('SA','NSW'),('SA','V'),('Q','NSW'),
        ('NSW','V'),('Q','T'),('NSW','T'), ('V','T'),
        ('NT','V')]
        
    # IMPORTANT...W needs to be a DiGraph, if you want the rootNode to be searched
    # for, otherwise you have to specify it
    G=nx.DiGraph() 
    G.add_edges_from(territories)    
else:
    G,colors,data=search.getLatticeGraph(4,5, directed=True,reverse=False)

# get root node
rootNode = search.getRootNode(G)

# assign the variables (which are also the colors)
domain = ['r','g','b']
# create an instance of the inequality
algorithms = CSPAlgorithms(filtering=CSPAlgorithms.FILTER_ARC_CONSISTENCY)
bk = CSPBacktracking(G, domain, rootNode=rootNode,
                     cspConstraint=None, cspAlgorithm=algorithms)

# run backtracking search and solve
assignments = bk.backtrackingSearch(G)

# print results and show graph
if (assignments is not None):
    print "Successfully solved CSP!"
    print assignments
    search.plotGraph(G, colors=domain)
else:
    print "Failed to solve CSP!"
bk.printStats()