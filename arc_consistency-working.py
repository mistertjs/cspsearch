# -*- coding: utf-8 -*-
"""
Created on Sat Nov 05 11:34:03 2016
https://courses.edx.org/courses/BerkeleyX/CS188x_1/1T2013/courseware/5fab202f219447c79915d6ba6eb08344/6f8a9aab61e44c4b93458e72a6da100b/

And here, there are some general purpose ideas that apply to any CSP
that will give us huge gains in speed.
One idea is ordering.
So, which variable should be assigned next?
As we'll see, there is better orderings and worse orderings.
Similarly, for values, which order should we try them in?
Some values are going to work out, some values aren't.
Maybe we should be smart about the order we try them.

Is there some way to detect an inevitable failure early so we don't
have to go through a whole bunch of assigning to discover it?
And then finally, we're going to look at structure methods where we look at
the constraint graph and exploit its structure in some way in order to get
a better algorithm.

##############################################################################

Filtering is about ruling out suspects

Filtering is about going ahead of the backtracking search and figuring out
elements in the domains of the unassigned variables, which can safely
be eliminated.

##############################################################################
Arc Consistency

This should help you remember you always "delete from the tail" of an arc.

So in essence, forward checking is just looking at the arcs that point
towards our new assignments, in this case WA, and enforcing their
consistency.

What we're going to do is we're going to make sure all of the arcs are
consistent all at once.

In order to enforce arc consistency, the algorithm's actually
pretty simple.
We're going to visit every single arc, check if it's consistent, and if not,
we're going to delete stuff from the tail.

Essentially, iterate the tail values against the head. If any tail value
breaks a constraint remove it

The important thing to remember is that we're going to visit all of the
arcs over and over and over again until everybody is simultaneously
consistent.

* Important: If X loses a value, neighbors of X need to be rechecked
* Arc consistency detects failure earlier than forward checking
* Can be run as a preprocessor or after each assignment
* What's the downside of enforcing arc consistency?

It makes each step slower, but hopefully you'll have to do less
backtracking.

This should remind you of A* from search, where computing the heuristic
cost time, but hopefully reduced the amount of actual search tree action
you had to do.

Hows It Work?

The important bits are there is going to be a queue, which initially is all
of the arcs in the CSP.

And as long as there's stuff in the queue, we're going to take something
off the queue, we're going to make that arc consistent by removing values
from its tail as needed.

If anything was actually removed, stuff may go back on the queue.

*** Because any time a variable's domain shrinks, all of its neighbors pointing
to it have to go back on to the queue. ***

And then we'd run this until the queue becomes empty.

Can this run forever?
This can't run forever, because every time an arc goes on the queue, it went
on the queue because its head's domain shrank.
That can only happen so many times.
In particular, for a given arc it can only happen d many times.

Arc consistency does not detect all failures.
It only detects a subclass of failures.
Arc consistency only traffics in pairs.
Because of this, arc consistency is only part of a backtracking search.
It's a filtering algorithm.
If I enforce arc consistency, I have to do it after every assignment in a
backtracking search.
So arc consistency here fixed that problem of having the violation that
we couldn't detect.

##############################################################################
while (queue is not empty):
    node = queue.pop(0)
    assignValue(node)
    arcQueue.insert(0,node) # as head
    if (arcConsistency(arcQueue) not consistent)
        backTrack and reassign previous node

Any node that gets changed becomes the head, and the tails (neighbors) are
check against the head, and made consistent. If after checking consistency
there is a node with no available values, you have to backtrack

@author: Administrator
"""
import networkx as nx
import numpy as np
import copy
rnd = np.random

class BacktrackingWithArcConsistency:
    
    def __init__(self, W, domain):
        self.W = W
        self.unassignedCount = 0
        self.queue = None
        self.fig = None
        self.domain = domain
        
        # stats on performance, the number of times a value was assigned
        self.valueAssignmentCount = 0

        # contains partial assignments
        self.assignments={} 
        
        # set up available domains
        self.avaliableDomains = {}
        for node in W.nodes():
            self.avaliableDomains[node] = copy.copy(domain)
            W.node[node]['domain'] = None
        
    
    def getRootNode(self):
        for n,d in self.W.in_degree().items():
            if (d==0):
                return n
        return None
        
    def addDetachedNodes(self, queue):
        for node in self.W.nodes():
            if (node not in queue):
                queue.append(node)
    
    def dfsRecurse(self, node, stack, discover=True):
        if (discover):
            if (node not in stack):
                stack.append(node)
            
        for childNode in np.sort(self.W.neighbors(node)):
            # if not discovered, recurse
            if (childNode not in stack):
                self.dfsRecurse(childNode, stack, discover)   
    
        if (not discover):
            if (node not in stack):
                stack.append(node)
        
    def dfs(self, G, node, discover=True):
        stack = []
        self.dfsRecurse(node, stack, discover)
        self.addDetachedNodes(stack)
        return stack
        
    def getQueue(self, topNode=None):
        if (topNode is None):
            topNode = self.getRootNode()
        queue = self.dfs(self.W, topNode)    
        self.addDetachedNodes(queue) 
        return queue

    def getBidirectionalQueue(self):
        queue = []
        for node in self.W.nodes():
            for neighbor in self.W.neighbors(node):
                queue.append((node,neighbor))    
        return queue
       
    def isConsistent(self, node, color):
        '''
        Checking for consistency across neighbors, but this time, you remove
        the available color from the domain, and propigate to forward check
        '''
        for v in self.W.neighbors(node):
            v_color = self.W.node[v]['domain']
            # if the color is the only one in list, constraint if broken
            if (v_color == color):
                return False
        return True
    
    def forwardCheck(self, node, color):
        '''
        Potential forward check
        Go through each neighbor and shrink their "copied" available domains.
        Don't actually shrink them until a node is assigned a value
        Return False if the domain is then empty on any neighbors
        '''
        for v in self.W.neighbors(node):
            domain = copy.deepcopy(self.avaliableDomains[v])
            if (color in domain):
                domain.remove(color)
                if (len(domain) == 0):
                    return False
        return True
        
    def selectUnassignedNode(self):
        #raw_input('Enter your input:')
        #self.plotGraph()
        
        '''
        Return the following node after cur node found in assignments
        ['V', 'NSW', 'NT', 'Q', 'SA', 'WA', 'T']
        For example, if V is assigned, return NSW
        '''
        self.unassignedCount += 1
        
        parser = self.queue[::-1]
        priorNode = None
        for node in parser:
            if (node in self.assignments):
                break
            priorNode = node
        return priorNode

    def orderDomain(self, color=None):
        '''
        Selects the next color in the domain, given an input color from before
        '''
        if (color is None):
            # pick a random color
            domain = ['r','g','b']
            clrIdx = rnd.randint(0,3)
            return domain[clrIdx]
        if (color == 'b'):
            return 'g'
        elif (color == 'g'):
            return 'r'
        else:
            return 'b'
    
    def isAssignmentComplete(self):
        '''
        Checks if the assignment is complete by comparing if there is the
        same number of nodes in both queue and assignments
        '''
        return len(self.assignments) == len(self.queue)
    
    def printDomains(self):
        for node in self.W.nodes():
            print node,"-",self.W.node[node]['domain']
    
    def plotGraph(self):
        pos=nx.spring_layout(self.W)
        labels = {}
        nodeColors = {'r':[],'b':[],'g':[], 'w':[]}
        for node in self.W.nodes():
            color = self.W.node[node]['domain']
            if (color is not None):
                nodeColors[color].append(node)
            else:
                nodeColors['w'].append(node)
            labels[node] = node
        for color in nodeColors:        
            if (len(nodeColors[color]) > 0):
                nx.draw_networkx_nodes(self.W,pos,
                                   nodelist=nodeColors[color],
                                   node_color=color,
                                   node_size=500,
                               alpha=0.8)
        
        nx.draw_networkx_edges(self.W,pos,
                           edgelist=W.edges(),
                           width=8,alpha=0.5,edge_color='k')
                   
        nx.draw_networkx_labels(self.W,pos,labels,font_size=16)                       
        

    def assignNodeValue(self, node, color):
        '''
        Assigns a valid (forward checked) value to the node, 
        and does basic house keeping on the graph object. Also removes from 
        choices in availableDomains from neighbors
        '''
        self.assignments[node] = color
        W.node[node]['domain'] = color   
        # remove all available colors after selecting one
        del self.avaliableDomains[node][:]

        # increment stat count
        self.valueAssignmentCount += 1
        
        # shrink neighbors        
        for v in self.W.neighbors(node):
            domain = self.avaliableDomains[v]
            # remove assigned value from neighbors
            if (color in domain):
                domain.remove(color)        
        
    def getAvailableValueCount(self, node):
        '''
        Returns the number of values in the available domain
        '''        
        domain = self.avaliableDomains[node]
        return len(domain)
        
    def getAvailableValue(self, node, idx=0):
        '''
        Returns the next available value from the domain, defaults to first
        in the list
        '''
        domain = self.avaliableDomains[node]
        return domain[idx]
        
    def backtrackAssignment(self, node, color):
        # remove the assignment
        self.assignments.pop(node)
        # clear the node domain color
        self.W.node[node]['domain'] = None
        # add back in all selections when selection is removed
        self.avaliableDomains[node] = copy.copy(self.domain)
        
        # add color back to neighbors
        for v in self.W.neighbors(node):
            domain = self.avaliableDomains[v]        
            domain.insert(0,color)
        
    def recursiveBacktrack(self):
        '''
        Recurse backwards through the tree, assigning and forward checking.
        If all assignments are made, return the assignments, otherwase
        return None to show that an assignment was unable to be made
        
        The while loop will try each available domain value. If it cannot
        assign any value without breaking a constraint, it returns None or 
        (failure)
        '''
        if (self.isAssignmentComplete()):
            return self.assignments
        
        # get next available node in queue
        node = self.selectUnassignedNode()
        
        domainIdx = 0
        while (domainIdx < self.getAvailableValueCount(node)):
            color = self.getAvailableValue(node, domainIdx)
            # assign the color now instead of after the check as with Filtering
            self.assignNodeValue(node, color)
            # check for consistency throughout the whole graph
            if (self.AC3(node, color)):
                # if consistent, assign the value, shrink neighbor domains
                print node, "=", color
                # recurse on success to assign next node in queue
                result = self.recursiveBacktrack()
                if (result is not None):
                    return result
                else:
                    # remove assignment and add back to domain
                    self.backtrackAssignment(node, color)
                    print node,"- backtrack ", color

            # get next assignment
            domainIdx += 1
            
        return None
            
    def backtrackSearch(self, topNode=None):
        # initialize dfs queue, with any unconnected nodes
        self.queue = self.getQueue(topNode)

        # reset counter, for stats
        self.unassignedCount = 0
        self.valueAssignmentCount = 0

        # recurse, assign, and return assignments
        results = self.recursiveBacktrack()
        if (results is None):
            return None

        return self.assignments

    def checkConsistency(self, nodeColor, neighborColors):
        # check if any colors other than nodeColor exist in neighborColors
        isConsistent = False
        a = list(neighborColors)
        if (nodeColor in a):
            a.remove(nodeColor)
            isConsistent = len(a) > 0
        else:
            isConsistent = True
        return isConsistent
    
    
    def removeInconsistentValues(self, edge):
        '''
        Remove inconsistent values from the tail (Xi)
        '''
        # get node names
        Xi = edge[0]
        Xj = edge[1]
        # get domain value lists from head (Di) and tail (Dj)
        Di = self.W.node[Xi]['domain']
        Dj = self.W.node[Xj]['domain']
        
        # remove inconsistencies
        removalList = []
        for x in Di:
            # check constraint...if invalid, remove x from domain Xi
            if (not self.checkConsistency(x, Dj)):
                # delete from tail
                removalList.append(x)

        # if anything was removed, remove it permanently
        for x in removalList:
            Di.remove(x)
            
        # return results        
        anythingRemoved = len(removalList) > 0
        return anythingRemoved        
        
    def revise(self, tail, color):
        '''
        If the color is removed from the tail node, then return True
        '''
        Dt = self.avaliableDomains(tail)
        curCnt = len(Dt)
        Dt.remove(color)
        prvCnt = len(Dt)
            
        return (curCnt != prvCnt)        

    def getArcNeighbors(self, node, arcQueue):
        neighbors = []
        for edge in arcQueue:
            if (edge[1] == node):
                neighbors.append(edge)
        return neighbors
        
    def AC3(self, node, color):
        '''
        We want to assign the input color to the input node
        '''
        arcQueue = []
        print node,"AC3"
        arcQueue.insert(0,node)
        while (len(arcQueue) > 0):
            node = arcQueue.pop(0)
            pairQueue = self.getArcNeighbors(node, arcQueue)
            for edge in pairQueue:
                print edge
                tail = edge[0]
                # revise the tail to be consistent
                if (self.revise(tail,color)):
                    # if the tail has no more colors, then stop and return
                    # False, otherwise, add the tail to the arcQueue to have
                    # its neighbors revised
                    tailLen = len(self.avaliableDomains(tail))
                    if (tailLen == 0):
                        return False
                    else:
                        arcQueue.insert(0,tail)
                        print node,"Arc Queue"
                else:
                    # if no change, then leave it and continue
                    continue
                
        # return true if all arcs are consistent
        return True

'''
###############################################################################
'''
'''
territories = [('WA','NT'),('WA','SA'),('NT','SA'),('NT','Q'),
        ('SA','Q'),('SA','NSW'),('SA','V'),('Q','NSW'),
        ('NSW','V'),('Q','T'),('NSW','T'), ('V','T')]
values = list(np.unique(territories))

# IMPORTANT...W needs to be a DiGraph, if you want the rootNode to be searched
# for, otherwise you have to specify it
rootNode = None
W=nx.Graph()
if (rootNode is None):
    W=nx.DiGraph() 
W.add_edges_from(territories)     
'''
rootNode = 'WA'
territories = [('WA','NT'),('WA','SA'),('NT','SA'),('NT','Q'),
        ('SA','Q'),('SA','NSW'),('SA','V'),('Q','NSW'),
        ('NSW','V'),('Q','T'),('NSW','T'), ('V','T')]
values = list(np.unique(territories))
mapping = {}
labels = {}
idx = 0
for value in values:
    mapping[idx]=value
    labels[value] = value
    idx += 1
G=nx.complete_graph(len(values))
W=nx.relabel_nodes(G,mapping)

# set the domain values in any order    
domain = ['b','r','g']    

# create the search obect and solve the problem
csp = BacktrackingWithArcConsistency(W, domain)
# start with the root node to get a dfs search
assignments = csp.backtrackSearch(rootNode)

if (assignments is None):
    print "Unable to find solution in %d assignments:" % \
            csp.valueAssignmentCount
    csp.printDomains()
else:
    print assignments
    print "Found solution in %d assignments:" % csp.valueAssignmentCount    
    csp.plotGraph()

