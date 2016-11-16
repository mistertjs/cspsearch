# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 06:35:32 2016
Utility functions for CSP program
@author: Administrator
"""

def getMatrixDomain(size=(3,3), zeroIndex=False):
    '''
    Returns a matrix domain of either string or numeric fashion
    '''
    domain = []
    rows = size[0]
    cols = size[1]
    for i in range(rows):
        for j in range(cols):
            if (not zeroIndex):
                domain.append(str(i+1)+str(j+1))
            else:
                domain.append(str(i)+str(j))
    return domain
    
def getColors():
    return ['b','g','r','c','m','y']

def mapColorsToDomain(domain, colors):
    return None