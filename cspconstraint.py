# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 15:44:30 2016

CSP constraint interface, used to create custome constraints which get passed
into the CSPBacktracking search class

@author: Administrator
"""

import numpy as np
rnd = np.random

class CSPConstraint(object):
    def checkUnary(self, node, value):
        raise NotImplementedError
        
    def checkBinaryComplete(self, head, tail, assignments):
        raise NotImplementedError        

    def checkBinaryConsistent(self, head, headValue, tail, tailValue):
        raise NotImplementedError        
        
    def checkNnaryComplete(self, nodes, assignments):
        raise NotImplementedError
        
    def checkNnaryConsistent(self, nodes, assignments):
        raise NotImplementedError        
        