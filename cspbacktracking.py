# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 15:20:58 2016

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov 05 11:34:03 2016

SearchGraph for exercise: hw1_search_q11_lookahead_graph_search
https://courses.edx.org/courses/BerkeleyX/CS188x_1/1T2013/courseware/eafff8d8427440069a749c1b825c0561/d35abd173ee745dda5417aaa89b97b02/

A∗-graph-search-with-Cost-Sensitive-Closed-Set (A∗- CSCS).

@author: Administrator
"""
import numpy as np
import networkx as nx
import copy
rnd = np.random
from aisearch import AISearch
from cspconstraint import CSPConstraint
            
class CSPAlgorithms(object):

    # algorithm constants
    FILTER_FORWARD_CHECK = 'Forward Checking'
    FILTER_ARC_CONSISTENCY = 'Arc Consistency'
    ORDER_MRV = 'Ordering MRV'
    ORDER_MRV_LCV = 'Ordering MRV w LCV'
    
    '''
    This class defines the algorithm used in the backtracking search. It
    defaults to a basic backtracking search with no filtering or ordering
    
    Backtracking:
        Assigns each variable without any notion of constraint checking
    Filtering:
        Keep track of domains for unassigned variables and cross off bad 
        options
        1. Forward checking: Cross off values that violate a constraint when
           added to the existing assignment. Iterate the assigned variables
           neighbors (tail) and remove inconsistenciesrelatve to the 
           new assigned variable (head). For example, A has neighbors B,C,D,
           you add to the check queue arcs B->A, C->A, D->A 
           After every assignment, you recheck the graph (neighbors)
        2. Arc consistency: 
    '''
    def __init__(self, filtering=None, ordering=None):
        self.algorithm = 'Backtracking'
        self.filtering = filtering
        self.ordering = ordering
        
    def setForwardCheckingFilter(self):
        self.filtering = self.FILTER_FORWARD_CHECK
        
    def setArcConsistencyFilter(self):
        self.filtering =  self.FILTER_ARC_CONSISTENCY
        
    def setMRVOrdering(self):
        self.ordering =  self.ORDER_MRV

    def setMRVwLCVOrdering(self):
        self.ordering =  self.ORDER_MRV_LCV
        
    def isForwardChecking(self):
        return self.filtering ==  self.FILTER_FORWARD_CHECK

    def isArcConsistency(self):
        return self.filtering ==  self.FILTER_ARC_CONSISTENCY

    def isMRVOrdering(self):
        return self.ordering ==  self.ORDER_MRV

    def isMRVwLCVOrdering(self):
        return self.ordering ==  self.ORDER_MRV_LCV
    
    def getFiltering(self):
        return self.filtering
        
    def getOrdering(self):
        return self.ordering
        
class CSPStats(object):
    def __init__(self):
        self.assignmentCnt = 0
        self.backtrackingCnt = 0
        
    def incAssignmentCnt(self):
        self.assignmentCnt += 1

    def incBacktrackingCnt(self):
        self.backtrackingCnt += 1
        
    def printStats(self):
        print "CSPStats: assignments: %d, backtracks: %d" % \
            (self.assignmentCnt,self.backtrackingCnt)
            
class CSPBacktracking(AISearch):
    '''
    Standard search formulation for CSP
    States defined by the values assigned so far (partial assignments)
        * Initial state: the empty assignment {}
        * Successor function: assign a value to an unassigned variable
        * Goal test: the current assignment is complete and satisfies all
          constraints
    '''
    
    def __init__(self, G, domain, rootNode, 
                 cspAlgorithm=None,
                 cspConstraint=None):
        self.G = G
        self.domain = domain
        self.rootNode = rootNode
        self.domainLen = len(domain)
        
        # assign default forward checking
        if (cspAlgorithm is None):
            cspAlgorithm = CSPAlgorithms(filtering=CSPAlgorithms.FILTER_FORWARD_CHECK)
        self.cspAlgorithm = cspAlgorithm

        # using arc-consistency, now we persist the available domain values
        # for each node
        self.availableValues = {}
        if (self.getFilteringType() == \
            CSPAlgorithms.FILTER_ARC_CONSISTENCY):
            for node in self.G.nodes():
                self.availableValues[node] = copy.deepcopy(domain)
        
        # default constraint is 'inequality'
        self.cspConstraint = cspConstraint
        
        # keep stats of various actions
        self.cspStats = CSPStats()
            
        # assign this once, then reuse            
        self.queue = None

    def printStats(self):
        self.cspStats.printStats()
        
    def getAlgorithm(self):
        return cspAlgorithm
        
    def getFilteringType(self):
        if (self.cspAlgorithm is not None):
            return self.cspAlgorithm.getFiltering()
        return None

    def isFilterForwardChecking(self):
        return self.getFilteringType() == CSPAlgorithms.FILTER_FORWARD_CHECK

    def isFilterArcConsistency(self):
        return self.getFilteringType() == CSPAlgorithms.FILTER_ARC_CONSISTENCY
        
    def getOrderingAlgorithm(self):
        if (self.cspAlgorithm is not None):
            return self.cspAlgorithm.getOrdering()
        return None
        
    def isArcConsistent(self):
        '''
        Checks the current assignments for arc consistency
        '''

    def solve(self):
        '''
        Primary interface for running the selected algorithm and solving
        the CSP
        '''
        
    def isAssignmentComplete(self, assignments, G):
        '''
        Checks if every node is assigned and assignments are valid
        '''
        constraintCheck = {'unary':True, 'binary':True, 'knary':True}
        
        for node in G.nodes():
            # check if node has been assigned
            if (node in assignments):
                headValue = assignments[node]
                
                # check unary constraint on head
                if (self.cspConstraint is not None):
                    success = self.cspConstraint.checkUnary(node, headValue)
                    constraintCheck['unary'] = success
                    if (not success):
                        return False
                    
                # check binary constraints                    
                for neighbor in G.neighbors(node):
                    if (neighbor in assignments):
                        tailValue = assignments[neighbor]
                        # use inequalityconstraint if no csp constraint
                        if (self.cspConstraint is None):
                            if (tailValue == headValue):
                                return False
                        else:
                            # use custome constraint to check binary 
                            success = self.cspConstraint.checkBinaryComplete(
                                node, neighbor, assignments)
                            constraintCheck['binary'] = success
                            if (not success):
                                return False
                            
                    else:
                        # neighbor is not assigned
                        return False
            else:
                # all nodes are not assigned
                return False
        return True
        
    def isAssignmentConsistent(self, node, value, assignments, G):
        '''
        Check forward the neighbors associated with the currently assigned values
        '''
        
        # check unary constraint on node itself
        if (self.cspConstraint is not None):
            success = self.cspConstraint.checkUnary(node, value)
            if (not success):
                return False
                        
        # check binary constraint of node and neighbors                        
        for neighbor in G.neighbors(node):
            if (neighbor in assignments):
                tailValue = assignments[neighbor]
                # use inequalityconstraint if no csp constraint
                if (self.cspConstraint is None):
                    if (tailValue == value):
                        return False
                else:
                    # use custom constraint is consistent before assignment
                    success = self.cspConstraint.checkBinaryConsistent(
                        node, value, neighbor, tailValue)
                    if (not success):
                        return False
        return True
                
    def selectUnassignedVariable(self, assignments, G):
        # find next node not assigned                                          
        for node in self.queue:
            if (node not in assignments):
                return node
        return None
        
    def getNextValue(self, curValue):
        if (self.isFilterArcConsistency()):
            return None
            
        '''
        Default forward checking
        '''
        # first value is index=0
        if (curValue is None):
            return self.domain[0]
        # else return next value
        idx = self.domain.index(curValue)
        # get next value if valid
        idx += 1
        if (idx < len(self.domain)):
            return self.domain[idx]
        else:
            return None
        
    def recursiveBacktracking(self, assignments, G):
        if (self.isAssignmentComplete(assignments, G)):
            return assignments
        
        # assign next node...if no node available, and assignment was not complete
        # then backtrack...not sure how it could get here in the first place
        node = self.selectUnassignedVariable(assignments, G)
        if (node is None):
            return None
        else:
            self.cspStats.incAssignmentCnt()
        
        # get next value in domain
        value = self.getNextValue(None)
        while (value is not None):
            if (self.isAssignmentConsistent(node, value, assignments, G)):
                # add assignment
                assignments[node] = value
                # recurse to next node
                assignmentsResults = self.recursiveBacktracking(assignments, G)
                if (assignmentsResults is not None):
                    return assignmentsResults
                # remove the assignment and try again
                assignments.pop(node)
                self.cspStats.incBacktrackingCnt()
                
            # get next value
            value = self.getNextValue(value)
        # no assignment was possible, so failure
        return None
        
    def backtrackingSearch(self, G):
        '''
        Start the backtracking search. Assumes the rootNode has been set in
        the constructor.
        Return assignments if successful, otherwise None
        '''
        assignments = {}
    
        # get the queue as DFS
        self.queue = self.dfs_recurse(G, self.rootNode, 
                                      discovery=False, sort=True)
            # recurse and assign
        assignmentsResults = self.recursiveBacktracking(assignments, G)
    
        # assign to graph
        if (assignmentsResults is not None):
            for node in assignmentsResults:
                G.node[node]['color'] = assignmentsResults[node]
    
        # return assignment results..None if failure
        return assignmentsResults
        
 