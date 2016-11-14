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
from cspbacktracking import CSPConstraint
 
class ValueInequality(CSPConstraint):
    def checkUnary(self, node, value):
        return True
        
    def checkBinaryComplete(self, head, tail, assignments):
        headValue = assignments[head]
        tailValue = assignments[tail]
        # results should not be the same
        return (headValue != tailValue)
        
    def checkBinaryConsistent(self, head, headValue, tail, tailValue):        
        return (headValue != tailValue)
        
    def checkNnaryComplete(self, nodes, assignments):
        return True
        
    def checkNnaryConsistent(self, nodes, assignments):
        return True
                
        
# generate test graph (directed lattice mxn)   
search = AISearch()
G,colors,data=search.getLatticeGraph(3,4, directed=True,reverse=False)

# assign the variables (which are also the colors)
domain = ['r','g','b']
# create an instance of the inequality
constraint = ValueInequality()

bk = CSPBacktracking(G, domain, rootNode='A',
                     cspConstraint=constraint)
assignments = bk.backtrackingSearch(G)

# print results and show graph
if (assignments is not None):
    print "Successfully solved CSP!"
    print assignments
    search.plotGraph(G, colors=domain)
else:
    print "Failed to solve CSP!"
bk.printStats()