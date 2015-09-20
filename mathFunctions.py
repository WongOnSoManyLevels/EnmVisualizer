# -*- coding: utf-8 -*-
"""
Created on Sun Mar 08 14:59:58 2015

@author: Yuan
"""
from __future__ import division
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def dis(cor_a, cor_b):
    '''
    returns distance between two points in 3 dimensions given the coordinates of the two points
    '''    
    summ = 0    
    for i in xrange (0,3):
        summ = summ + (cor_a[i]-cor_b[i]) ** 2
        
    distance = summ ** 0.5
    return distance

def mat2vec(np_matrix):
    '''
    transfers a matrix to a vector
    '''    
    vector = np.asarray(np_matrix).reshape(-1)
    return vector
    
def vec2mat(np_vector):
    '''
    transfers a vector to a 3D matrix
    '''
    
    length = len(np_vector)
    if length%3 != 0:
        raise ValueError('vector length cannot be divided by 3')
    else:
        matrix = np_vector.reshape((length/3,3))
    
    return matrix
    
def waitingEffects(function):
    def newFunction(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        function(self)
        QApplication.restoreOverrideCursor()
    return newFunction