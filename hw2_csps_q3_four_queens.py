# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 10:13:11 2016

CSPs Homework 2: hw2_csps_q3_four_queens

https://courses.edx.org/courses/BerkeleyX/CS188x_1/1T2013/courseware/5fab202f219447c79915d6ba6eb08344/0460a6606a3e4630b0b4e913dd88c135/
This is four queens using AC, not min-conflicts

@author: Administrator
"""

import numpy as np
import networkx as nx
rnd = np.random
from cspbacktracking import CSPBacktracking
from cspbacktracking import CSPConstraint
from cspbacktracking import CSPAlgorithms
import csputil as cu


class HW2QueensConstraint(CSPConstraint):
    
    def checkUnary(self, node, value):
        return True
        
    def getPositionsFromValue(self, value):
        '''
        Return float row,col tuple from value
        '''
        return [float(value[0]),float(value[1])]
        

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
domain = cu.getMatrixDomain(size=(4,4),zeroIndex=False)
colors = ['b','g','r','c','m','y']
edges = [('Q1','Q2'),('Q1','Q3'),('Q1','Q4'),
         ('Q2','Q3'),('Q2','Q4'),
         ('Q3','Q4')]

# create graph from edges
G=nx.Graph()
G.add_edges_from(edges)

# get constraint
constraint = HW2QueensConstraint()
algorithms = CSPAlgorithms(filtering=CSPAlgorithms.FILTER_ARC_CONSISTENCY)
bk = CSPBacktracking(G, domain, rootNode=rootNode, 
                     cspConstraint=constraint,
                     cspAlgorithm=algorithms)
assignments = bk.backtrackingSearch(G)
# print results and show graph
if (assignments is not None):
    print "Successfully solved CSP!"
    print assignments
    # map colors
    colors = cu.mapColorsToDomain(G, domain, colors)
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