# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 13:57:17 2016

Austrailian territories example, where adjacent nodes cannot have the same
color. Except, I'm using a directed lattice graph

Interesting to change the mxn size of the lattice and notic the exponential
number of assignments and backtracks.

Also, increasing or decreasing the number of colors (values) in the domain,
where anything > 3 isn't used, anything < 3 fails

@author: Administrator
"""

import numpy as np
rnd = np.random
from aisearch import AISearch
from cspbacktracking import CSPBacktracking
 
# generate test graph (directed lattice mxn)   
search = AISearch()
G,colors,data=search.getLatticeGraph(5,3, directed=True,reverse=False)

# assign the variables (which are also the colors)
domain = ['r','g','b']
bk = CSPBacktracking(G, domain, 'A')
assignments = bk.backtrackingSearch(G)

# print results and show graph
if (assignments is not None):
    search.plotGraph(G, colors=domain)
    print "Successfully solved CSP!"
    print assignments
else:
    print "Failed to solve CSP!"
    
# show stats    
bk.printStats()
