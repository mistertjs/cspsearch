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

 
'''
###############################################################################
'''

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
        self.nodeAssignmentCnt = 0
        self.backtrackingCnt = 0
        self.valueAssignmentCnt = 0
        
    def incNodeAssignmentCnt(self):
        self.nodeAssignmentCnt += 1

    def incBacktrackingCnt(self):
        self.backtrackingCnt += 1

    def incValueAssignmentCnt(self):
        self.valueAssignmentCnt += 1
        
    def printStats(self):
        print "CSPStats: node assignments: %d, backtracks: %d," \
              " value assignments: %d" % \
            (self.nodeAssignmentCnt,self.backtrackingCnt,
             self.valueAssignmentCnt)
            
class CSPBacktracking(AISearch):
    '''
    Standard search formulation for CSP
    States defined by the values assigned so far (partial assignments)
        * Initial state: the empty assignment {}
        * Successor function: assign a value to an unassigned variable
        * Goal test: the current assignment is complete and satisfies all
          constraints
    '''
    
    def __init__(self, G, domain, rootNode, cspConstraint=None,
                 cspAlgorithm=None):
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
        if (cspConstraint is None):
            self.cspConstraint = ValueInequality()
        else:
            self.cspConstraint = cspConstraint
        
        # keep stats of various actions
        self.cspStats = CSPStats()
            
        # assign this once, then reuse           
        self.assignments = {}
        self.queue = None

    def printStats(self):
        self.cspStats.printStats()
        
    def getAlgorithm(self):
        return self.cspAlgorithm
        
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
        
    def solve(self):
        '''
        Primary interface for running the selected algorithm and solving
        the CSP
        '''
        
    def isAssignmentComplete(self, assignments, G):
        '''
        Checks if every node is assigned and assignments are valid
        '''
        
        if (self.isFilterArcConsistency()):
            # check if assignments are available for every node, if so
            # arc consistency guarantees validity
            for node in G.nodes():
                # check if node has been assigned
                if (node not in assignments):
                    return False
            # all nodes assigned, return True
            return True

            
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
        '''
        Find a node which is unassigned. 
        1. For the defaul, its the first node which is not in the assignment 
           list.
        2. For ArcConsistency, it is the node with the least number of value
           which have not already been assigned
        '''
        '''
        if (self.isFilterArcConsistency()):
            # find the next value with the least number of assignments
            minAssignments = 10000
            minNode = None
            for node in self.availableValues:
                if (node not in assignments):
                    valueList = self.availableValues[node]
                    numAvailAssignments = len(valueList)
                    if (numAvailAssignments < minAssignments):
                        minAssignments = numAvailAssignments
                        minNode = node
            # check if any assignments are available
            if (minNode is not None):
                return minNode
            else:
                return None
        '''
        # find next node not assigned                                          
        for node in self.queue:
            if (node not in assignments):
                return node
        return None
        
    def getNextValue(self, node, curValue):
        '''
        Return the next available value for this node
        '''
        if (self.isFilterArcConsistency()):
            '''
            Arc consistency returns whatever is available in the
            availability list
            '''
            valueList = self.availableValues[node]
            for value in valueList:
                return value
            # return none if none available
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

    def assignValueToNode(self, node, value):
        # assigne the value
        self.assignments[node] = value

        # remove the entry from availabel values
        if (self.isFilterArcConsistency()):
            remainingValues = self.availableValues[node]
            if (value not in remainingValues):
                print "Removing a value ", value, " that doesn't exsit", \
                      " for node", node
            else:
                remainingValues.remove(value)
            
        # update stats
        self.cspStats.incValueAssignmentCnt()
        
    def removeAssignment(self, node, value):
        if (node in self.assignments):
            self.assignments.pop(node)

        # add back to available values            
        if (self.isFilterArcConsistency()):
            self.availableValues[node].append(value)
            
    def recursiveBacktracking(self, assignments, G):
        '''
        Main search function, recursing through the graph and enforcing
        constraint consistency 
        '''
        if (self.isAssignmentComplete(assignments, G)):
            return assignments
        
        # assign next node...if no node available, and assignment was not complete
        # then backtrack...not sure how it could get here in the first place
        node = self.selectUnassignedVariable(assignments, G)
        if (node is None):
            return None
        else:
            self.cspStats.incNodeAssignmentCnt()
        
        # assign next value in domain
        value = self.getNextValue(node, None)
        while (value is not None):
            if (self.isFilterArcConsistency()):
                # assign the value first
                #prvValues = copy.deepcopy(self.availableValues[node])
                self.assignValueToNode(node, value)
                print "Assigning node ",node," to value ",value

                availableValueBackup = copy.deepcopy(self.availableValues)

                # then check consistency
                arcs = self.getArcQueue(G, node)
                if (self.isArcConsistent(G, arcs)):
                    # if consistent, recurse
                    # recurse to next node
                    assignmentsResults = self.recursiveBacktracking(assignments, G)
                    if (assignmentsResults is not None):
                        return assignmentsResults
                    # if assignment from previous was bad, push back previous
                        
                # redo the values
                self.availableValues = availableValueBackup
                # assignment and try again
                print "Reassign values back to node ", node, value
                # add value back to end of available values
                self.removeAssignment(node, value)
                self.cspStats.incBacktrackingCnt()
                # else, try next value
            else:
                if (self.isAssignmentConsistent(node, value, assignments, G)):
                    # add assignment
                    self.assignValueToNode(node, value)
                    # recurse to next node
                    assignmentsResults = self.recursiveBacktracking(assignments, G)
                    if (assignmentsResults is not None):
                        return assignmentsResults
                    # remove the assignment and try again
                    assignments.pop(node)
                    self.cspStats.incBacktrackingCnt()
                
            # get next value
            value = self.getNextValue(node, value)
        # no assignment was possible, so failure
        return None
        
    def backtrackingSearch(self, G):
        '''
        Start the backtracking search. Assumes the rootNode has been set in
        the constructor.
        Return assignments if successful, otherwise None
        '''
        self.assignments = {}
    
        # get the queue as DFS
        self.queue = self.dfs_recurse(G, self.rootNode, 
                                      discovery=False, sort=True)
                                      
        # check unary constraints
        if (self.isFilterArcConsistency()):                                      
            self.checkUnaryConstraints()
            print self.availableValues
            
        # recurse and assign
        assignmentsResults = self.recursiveBacktracking(self.assignments, G)
    
        # assign to graph
        if (assignmentsResults is not None):
            for node in assignmentsResults:
                G.node[node]['color'] = assignmentsResults[node]
    
        # return assignment results..None if failure
        return assignmentsResults
        
    def checkUnaryConstraints(self):
        for node in self.availableValues:
            removalList = []
            valueList = self.availableValues[node]
            for value in valueList:
                # check unary constraint...if valid, check binary constraint
                if (not self.cspConstraint.checkUnary(node, value)):
                    removalList.append(value)
            
            # remove violations from available values
            for value in removalList:
                valueList.remove(value)
                
    def removeInconsistentValues(self, head, tail):
        '''
        Iterate through the tail and check which values are inconsitent.
        Return True if any values were removed from the tail assignment
        '''        
        # get values either assigned, or available
        tailAssigned = False
        tailValues = self.availableValues[tail]
        if (tail in self.assignments):
            tailValues = [self.assignments[tail]]
            tailAssigned = True

        headValues = self.availableValues[head]
        if (head in self.assignments):
            headValues = [self.assignments[head]]
            
        #print tail,"->",head
        removeValues = []
        for tailValue in tailValues:
            # if any are consistent retain it
            retain = False
            for headValue in headValues:
                if (self.cspConstraint.checkBinaryConsistent(head,
                                                             headValue,
                                                             tail,
                                                             tailValue)):
                    # if any constraint works, retaint it
                    retain = True
                    break

            # add inconsistent value, and remove it after iteration
            if (not retain):
                removeValues.append(tailValue)
 
        # check if the removed value was the assignment
        if (tailAssigned and len(removeValues) > 0):
            return False
            
        # remove values from available assignments
        for value in removeValues:
            self.availableValues[tail].remove(value)

        # if any values were removed return true
        if (len(removeValues) > 0):
            print "Removing inconsistencies from node ", tail, removeValues
            return True
        else:
            return False
             
    def getArcQueue(self, G, node):
        arcQueue = []
        mainQueue = self.getBidirectionalArcs(G)
        for arc in mainQueue:
            # check if arc has node as head
            if (arc[1] == node and arc not in arcQueue):
                arcQueue.append(arc)
        return arcQueue
        
    def isArcConsistent(self, G, arcQueue, maxIterations=-1):
        '''
        Arc consist of (tail -> head) configuration
        '''
        iterCnt = 0
        while (len(arcQueue) > 0):
            edge = arcQueue.pop(0)
            head = edge[1]
            tail = edge[0]
            if (self.removeInconsistentValues(head, tail)):
                 # if the tail was modified, add all arcs to the queue
                 # where the tail is now the head
                newArcs = self.getArcQueue(G, tail)          
                # check if new arcs have remaing values
                hasEmptyAssignments = False
                for arc in newArcs:
                    node = arc[0]
                    remaingValues = self.availableValues[node]
                    if (len(remaingValues) == 0):
                        hasEmptyAssignments = True
                        
                # check empty assignments
                if (hasEmptyAssignments):
                    # replace the availableAssignments
                    print "Reset available values:", self.availableValues
                    return False
                # otherwise add new arcs for testing
                arcQueue.extend(newArcs)
                
            # if the loop never ends, stop it
            iterCnt += 1
            if (maxIterations >= 0 and iterCnt >= maxIterations):
                return False

        return True

  