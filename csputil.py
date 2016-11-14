# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 06:35:32 2016
Utility functions for CSP program
@author: Administrator
"""

def getMatrixDomain(size=3, zeroIndex=False):
    '''
    Returns a matrix domain of either string or numeric fashion
    '''
    domain = []
    for i in range(size):
        for j in range(size):
            if (not zeroIndex):
                domain.append(str(i+1)+str(j+1))
            else:
                domain.append(str(i)+str(j))
    return domain
    
def getColors():
    return ['b','g','r','c','m','y']

def mapColorsToDomain(domain, colors):
    return None