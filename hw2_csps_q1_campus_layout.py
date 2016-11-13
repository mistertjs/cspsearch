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


class HW2CampusConstraint(CSPConstraint):
    
    def __init__(self, G):
        self.G = G        

    def isAdjacent(self, value1, value2):
        '''
        Returns True if the values are adjacent (not diagonal, or same)
        '''
        # check if same row
        row1 = value1[0]
        row2 = value2[0]
        col1 = value1[1]
        col2 = value2[2]
        
        # if values are equal, return failure now, otherwise assumption can
        # be made to continue check
        if (value1 == value2):
            return False
            
        # adjacent row
        if (row1 == row2):
            if (abs(col1-col2) == 1):
                return True
            else:
                return False

        # adjacent col, simple since there is only two rows and they are 
        # not the same cell, they have to be adjacent
        if (col1 == col2):
            return True
            
        # must be diagonal, or displaced too far
        return False
        
    def checkUnary(self, node, value):
        '''
        For nodes (variables) with unary constraints. 
        1. If the unary does not apply to the node, return 0
        2. If the unary applies, return 1 if the constraint is satisfied,
           otherwise, return -1
        '''
        result = 0
        if (node == 'B'):
            # B must be adjacent to the Road
            if (value == '13' or value == '23'):
                result = 1
            else:
                # otherwise it fails
                result = -1
        if (node == 'A'):
            # A cannot be on a hill
            if (value == '12' or value == '21'):
                result = -1
            else:
                # otherwise it fails
                result = 1
        if (node == 'D'):
            # D must me on a hill or adjacent to the road
            if ((value == '12' or value == '21') or 
                (value == '13' or value == '23')):
                result = 1
            else:
                result = -1
        
        return result
        
    def checkBinaryConstaint(self, head, tail, assignments):
        '''
        Checks all values of tail assignments relative to the head. All valid
        assignments will go into the validValue list. All invalid values go
        into the invalidValues. Check of validitiy can be done by checking
        the length of either list
        '''
        
        validValues = []
        invalidValues = []

        constraintCheck = False
        
        def checkAdjacentVariables(head, tail, assignments, 
                                   validValues, invalidValues):
            # iterate through tail values (A or C) and check adjacent to B
            tailValues = assignments[tail]
            headValues = assignments[head]
            for tailValue in tailValues:
                foundValid = False
                for headValue in headValues:
                    if (self.isAdjacent(tailValue, headValue)):
                        validValues.append(tailValue)
                        foundValid = True
                # check if not B values were valid
                if (not foundValid):
                    invalidValues.append(tailValue)
                                       
        # The administration structure (A) and the classroom (C) must both be 
        # adjacent to the bus stop (B)
        # A->B, C->B, B->A, B->C
        constraintCheck = ((head == 'B' and (tail == 'A' or tail == 'C')) or
                           ((head == 'A' or head== 'C') and tail == 'B'))
        if (constraintCheck):                           
          checkAdjacentVariables(head, tail, assignments, 
                                 validValues, invalidValues)
                    
        # The classroom  (C) must be adjacent to the dormitory (D)
        constraintCheck = ((head == 'C' and tail == 'D') or
                           (head == 'D' and tail == 'C'))
        if (constraintCheck):                           
          checkAdjacentVariables(head, tail, assignments, 
                                 validValues, invalidValues)
                        
        return [validValues, invalidValues]
        

'''            
rootNode = '11'
domain = ['r','g','b','w']
edges = [('11','12'),('11','21'),('12','22'),('12','13'),
         ('13','23'),('13','Road'),('21','22'),('22','23'),('23','Road')]
colors = domain
'''
'''
rootNode = 'WA'
domain = ['b','r','g']    
edges = [('WA','NT'),('WA','SA'),('NT','SA'),('NT','Q'),
        ('SA','Q'),('SA','NSW'),('SA','V'),('Q','NSW'),('T','T')]
colors = domain
'''
rootNode = 'A'
domain = ['11','12','13','21','22','23']
edges = [('A','B'),('A','C'),('A','D'),
         ('B','C'),('B','D'),
         ('C','D')]
colors = None

# IMPORTANT...W needs to be a DiGraph, if you want the rootNode to be searched
# for, otherwise you have to specify it
G=nx.Graph()
G.add_edges_from(edges)  
# add assignments to each

# get constraint
constraint = HW2CampusConstraint(G)
bk = CSPBacktracking(G, domain, constraint)
result, assignments = bk.backtrackingSearch(rootNode)
print result, assignments
bk.plotGraph(G,colors=colors)

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