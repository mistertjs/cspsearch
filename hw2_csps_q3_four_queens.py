# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 10:13:11 2016

CSPs Homework 2: hw2_csps_q1_campus_layout

This uses a Constraint object to check constraints which have:
1-Consistency: unary constraints (single node constraint)
2-Consistency: binary constraints (pair of node constraints)
K-Consistency: n-nary constraints (k-node constraints)

You are asked to determine the layout of a new, small college. 
The campus will have four structures: 
(A) An administration structure
(B) A bus stop
(C) A classroom
(D) A dormitory (D). 

The layout must satisfy the following constraints:

1. The bus stop (B) must be adjacent to the road.
2. The administration structure (A) and the classroom (C) must both be adjacent 
   to the bus stop (B).
3. The classroom (C) must be adjacent to the dormitory (D).
4. The administration structure (A) must not be adjacent to the dormitory (D).
5. The administration structure (A) must not be on a hill.
6. The dormitory (D) must be on a hill or adjacent to the road.
7. All structures must be in different grid squares.
8. Here, adjacent means that the structures must share a grid edge, not just a 
   corner.

Campus Layout:
Each structure (including the bus stop) must be placed somewhere on the grid 
shown below.
------------------------------------||
|      (1,1)| hill (1,2)|      (1,3)||
------------------------------------||Road
| hill (2,1)|      (2,2)|      (2,3)||
------------------------------------||

@author: Administrator
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
rnd = np.random
from aisearch import AISearch
from cspbacktracking import CSPBacktracking
from cspbacktracking import CSPConstraint
import csputil as cu


class HW2QueensConstraint(CSPConstraint):
    
    def checkUnary(self, node, value):
        return True
        
    def getPositionsFromValue(self, value):
        '''
        Return float row,col tuple from value
        '''
        return [float(value[0]),float(value[1])]
        
    def checkBinaryComplete(self, head, tail, assignments):
        # check rows
        headValue = assignments[head]    
        tailValue = assignments[tail]
        hrow,hcol = self.getPositionsFromValue(headValue)
        trow,tcol = self.getPositionsFromValue(tailValue)
        
        # check not similar row or column
        if (hrow == trow):
            return False
        if (hcol == tcol):
            return False
        # not on a diagonal
        if (abs(hrow-trow) == abs(hcol-tcol)):
            return False
        
        return True
        
            

    def checkBinaryConsistent(self, head, headValue, tail, tailValue):
        hrow,hcol = self.getPositionsFromValue(headValue)
        trow,tcol = self.getPositionsFromValue(tailValue)
        
        # check not similar row or column
        if (hrow == trow):
            return False
        if (hcol == tcol):
            return False
        # not on a diagonal
        if (abs(hrow-trow) == abs(hcol-tcol)):
            return False

        # check
        return True

rootNode = 'Q1'
# get four domain
domain = cu.getMatrixDomain(size=4,zeroIndex=False)
colors = ['b','g','r','c','m','y']
edges = [('Q1','Q2'),('Q1','Q3'),('Q1','Q4'),
         ('Q2','Q3'),('Q2','Q4'),
         ('Q3','Q4')]

# create graph from edges
G=nx.Graph()
G.add_edges_from(edges)

# get constraint
constraint = HW2QueensConstraint()
bk = CSPBacktracking(G, domain, rootNode='Q1', 
                     cspConstraint=constraint)
assignments = bk.backtrackingSearch(G)
# print results and show graph
if (assignments is not None):
    print "Successfully solved CSP!"
    print assignments
    # map colors
    for node in G.nodes():
        value = assignments[node]
        colorIdx = domain.index(value)
        color = colors[colorIdx]
        G.node[node]['color'] = color
    # plot
    bk.plotGraph(G, colors=colors)
else:
    print "Failed to solve CSP!"
bk.printStats()

'''
##############################################################################
'''
'''
search = AISearch()
G,colors,data=search.getLatticeGraph(3,3, directed=False)
bk = CSPBacktracking(G, domain=colors)
result, assignments = bk.backtrackingSearch('A')
print result, assignments
bk.plotGraph(G,colors=colors)
'''