# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 13:41:45 2016

@author: Administrator
"""
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
rnd = np.random

class AISearch(object):
    
    def getRootNode(self, G):
        if (G.is_directed()):
            for n,d in G.in_degree().items():
                if (d==0):
                    return n
        return None
    
    def addDetachedNodes(self, G, stack):
        for node in G.nodes():
            if (node not in stack):
                stack.append(node)
    
    def plotGraph(self, G, pos=None, colors=None, figsize=(10,8)):
        if (pos is None):
            pos=nx.spring_layout(G)

        fig, ax = plt.subplots(figsize=figsize)
            
        labels = {}
        nodeColors = {}
        if (colors is not None):
            for color in colors:
                nodeColors[color] = []
            for node in G.nodes():
                color = G.node[node]['color']
                if (color is not None):
                    nodeColors[color].append(node)
                else:
                    nodeColors['w'].append(node)
                labels[node] = node
        else:
            colors = ['w','b','g','r','c','m','y']
            for color in colors:
                nodeColors[color] = []            
            idx=0
            for node in G.nodes():
                color = colors[idx]
                nodeColors[color].append(node)
                idx += 1
                if (idx >= len(colors)):
                    idx=0
                labels[node] = node
                
        for color in nodeColors:        
            if (len(nodeColors[color]) > 0):
                nx.draw_networkx_nodes(G,pos,ax=ax,
                                   nodelist=nodeColors[color],
                                   node_color=color,
                                   node_size=500,
                               alpha=0.8)
        
        nx.draw_networkx_edges(G,pos,ax=ax,
                           edgelist=G.edges(),
                           width=2,alpha=0.5,edge_color='k')
                   
        nx.draw_networkx_labels(G,pos,labels,font_size=16) 

        plt.show()
        
    def getLatticeGraph(self, rows, cols, directed=True, reverse=False, addColors=True):
        '''
        Generate a lattice graph, for examples.
        To get a true dfs, set directed=True, and dfs(discovery=False)
        '''
        colors = ['y','0.75','m','0.5','c','r','g','b','k','w']
        
        colorMap = {}
        colorIdx = 0
        nodes = []
        value = 'A'
        for row in range(rows):
            for col in range(cols):
                # add to nodes
                nodes.append(value)
                # add color
                colorMap[value] = colors[colorIdx]
                # update value
                value = chr(ord(value) + 1)
            # keep columns the same color
            colorIdx += 1
            if (colorIdx >= len(colors)):
                colorIdx = 0
    
        edges = []
        # do horizontals
        for row in range(rows):
            idx = (row * cols)
            for col in range(cols):
                if (col > 0):
                    edges.append((nodes[idx-1],nodes[idx]))
                idx += 1
        # do verticals and diagonals
        for col in range(cols):
            idx = col
            for row in range(rows):
                if (row > 0):
                    # do vertical
                    if (reverse):
                        edges.append((nodes[idx],nodes[idx-cols]))
                    else:
                        edges.append((nodes[idx-cols],nodes[idx]))
                    if (col < (cols-1)):
                        # do diagonal
                        if (reverse):
                            edges.append((nodes[idx+1],nodes[idx-cols]))
                        else:
                            edges.append((nodes[idx-cols],nodes[idx+1]))
                idx += cols            
    
        # create the graph
        G=None
        if (directed):
            G=nx.DiGraph()
        else:
            G=nx.Graph()
        G.add_nodes_from(nodes)                    
        G.add_edges_from(edges)
        # add colors
        if (addColors):
            nx.set_node_attributes(G, 'color', colorMap)
            
        return G,colors,[nodes,edges]
        
    def dfs_recurse(self, G, node, stack=None, discovery=True, sort=True):
        '''
        To get a default DFS on a lattice(3,3) use:
            1. getLatticeGraph(3,3, directed=True,reverse=False)
            2. dfs_recurse(G,'A')
        Setting discovery=True will give the finished order
        '''
        # initialize the stack and identify top node recursion
        topNode = False
        if (stack is None):
            stack = []
            topNode = True
    
        if (node not in stack):
            if (discovery):
                stack.append(node)
            else:
                stack.insert(0,node)        
    
        # get associated neighbors
        nodes = G.neighbors(node)
        if (sort):
            nodes = list(np.sort(G.neighbors(node)))
    
        for neighbor in nodes:
            if (neighbor not in stack):
                self.dfs_recurse(G, neighbor, stack, discovery)

        # get any detached nodes     
        if (topNode):
            self.addDetachedNodes(G, stack)
            
        return stack
        
    def bfs_recurse(self, G, node, stack=None, discovery=True, sort=True):
        '''
        To get a default BFS on a lattice(3,3) use:
            1. getLatticeGraph(3,3, directed=True,reverse=False)
            2. bfs(G, 'A')
        Setting discovery=True will give the finished order
        '''
        if (stack is None):
            stack = [node]
    
        def addNode(node, stack):
            #print node
            if (node not in stack):
                if (discovery):
                    stack.append(node)        
                else:
                    stack.insert(0,node)
                return True
            return False
            
        # get associated neighbors
        nodes = G.neighbors(node)
        if (sort):
            nodes = list(np.sort(G.neighbors(node)))
    
        # add each child to the stack
        neighborsAdded = []
        for neighbor in nodes:
            # recurse if the node was added
            if (addNode(neighbor, stack)):
                neighborsAdded.append(neighbor)
                
        # recurse through each untraversed neighbor
        for neighbor in neighborsAdded:
            self.bfs_recurse(G, neighbor, stack, discovery)
    
        return stack        
