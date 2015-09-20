# -*- coding: utf-8 -*-
"""
Created on Sun Mar 08 14:25:00 2015

@author: Yuan
"""

from __future__ import division
import numpy as np
from PdbParser import *
import warnings
from mathFunctions import *
from pymol.cgo import *

class ANM:    
    def __init__(self, model, cutoff = 12, useCA = True, method = 'cutoff', power = 4):
        '''
        initiation of class ANM
        '''        
        self.model = model        
        self.cx = None
        self.hess = None
        self.hinv = None
        self.freq = None
        self.modes = None
        self.cutoff = cutoff
        self.e = None
        self.v = None
        self.method = method
        self.power = power
        self.MSF = None
        self.arrows = list()
        self.internalDis = None
        self.T = 300
        self.KB = 1.38065e-23
        self.GAMMA = 1e-20
        self.PI = 3.1415926
        
        if isinstance(self.model, pdbModel):
            pass
        elif isinstance(self.model, pdbParser):
            if len(model) > 1:
                warnings.warn('Mutiple models found, will use the first model')
            self.model = self.model.getModel()
        else:
            raise TypeError('Unrecgonized model type')
                
        if useCA:
            try:
                self.model = self.model.toCA()
            except:
                raise ValueError('Failed to extract alpha carbons')
                
    def __len__(self):
        return self.model.length
            
    def getCX(self):
        if self.cx is None:
            warnings.warn("Contact Matrix not found, Rebuilding now...") 
            self.buildCX()
        
        return self.cx
            
    def resetCX(self):
        self.cx = None
        
    def getHess(self):
        if self.hess is None:
            warnings.warn("Hessian Matrix not found, Rebuilding now...")
            self.buildHess()
        
        return self.hess
        
    def resetHess(self):
        self.hess = None
        
    def getMSF(self):
        if self.MSF is None:
            self.calcMSF()
            
        return self.MSF
        
    def resetMSF(self):
        self.MSF = None
        
    def getE(self):
        if self.e is None:
            self.calcModes()
            
        return self.e
    
    def resetE(self):
        self.e = None
        
    def getV(self):
        if self.v is None:
            self.calcModes()
            
        return self.v
        
    def resetV(self):
        self.v = None
        
    def getHinv(self):
        if self.hinv is None:
            self.calcHessInv()
            
        return self.hinv
        
    def resetHinv(self):
        self.hinv = None
        
    def getInternalDis(self):
        if self.internalDis is None:
            self.calcInternalDis()
            
        return self.internalDis
        
    def resetInternalDis(self):
        self.internalDis = None
        
    def buildCX(self):
        '''
        build contact matrix
        '''
        if not isinstance(self.model.cor, np.ndarray):        
            raise ValueError('self.modelture coordinates are not numpy arrays')
        if self.model.cor.shape[1] != 3:
            raise ValueError('Dimension of coordinates does not equal 3')
            
        self.contactPair_x = list()
        self.contactPair_y = list()    
        #length = model.length    
        if self.method == 'pf':        
            self.cx = np.zeros((self.model.length, self.model.length), dtype = float)
        elif self.method == 'cutoff':
            self.cx = np.zeros((self.model.length, self.model.length), dtype = int)
        for i in xrange(1, self.model.length):
            for j in xrange(0,i):
                distance = dis(self.model.cor[i,:], self.model.cor[j,:])
                if distance <= self.cutoff:
                    self.contactPair_x.append(i)
                    self.contactPair_y.append(j)
                    if self.method == 'cutoff':
                        self.cx[i, j] = 1
                    elif self.method == 'pf':
                        self.cx[i, j] = (1/distance) ** self.power
                    else:
                        raise TypeError('Unrecgonized ANM method -- %s' % self.method)
                    
    def buildHess(self):
        '''
        build hessian matrix
        '''
        self.cx = self.getCX()
        length = self.cx.shape[0]
        contactNumber = len(self.contactPair_x)
        self.hess = np.zeros((3*length,3*length),dtype = float)
        for i in xrange (0,contactNumber):
            x = self.contactPair_x[i]
            y = self.contactPair_y[i]
            dR = self.model.cor[y,:] - self.model.cor[x,:]
            dR = dR/np.linalg.norm(dR)
            K33 = -dR[np.newaxis,:].T*dR
            self.hess[3*x:3*x+3,3*y:3*y+3] = K33
            self.hess[3*y:3*y+3,3*x:3*x+3] = K33
            self.hess[3*x:3*x+3,3*x:3*x+3] = self.hess[3*x:3*x+3,3*x:3*x+3] - K33
            self.hess[3*y:3*y+3,3*y:3*y+3] = self.hess[3*y:3*y+3,3*y:3*y+3] - K33
            
    def calcHessInv(self, eigRange = None):
        
        self.hess = self.getHess()
        self.e = self.getE()
        
        if eigRange is None:
            startInd = 6
            endInd = self.model.cor.shape[0]*3
        else:
            try:
                startInd = eigRange[0]
                endInd = eigRange[1]
            except:
                raise ValueError('Unrecognized Eigenvector Range')
        
        length = self.cx.shape[0]        
        self.hinv = np.zeros((3*length, 3*length), dtype = float)
        
        for ind in xrange(startInd, endInd):
            a = self.v[:,ind][np.newaxis]
            b = a.T            
            self.hinv = self.hinv + (1/self.e[ind])*np.dot(b, a)
                
    def calcModes(self, numeig = None):
        '''
        calculat modes for ANM
        
        numeig: number of eigen values calculated
                default value is none
                all modes are calculated
        '''
        self.hess = self.getHess()
        if not isinstance(self.hess, np.ndarray):        
            raise ValueError('Hessian Matrix is not in the type of numpy arrays')
            
        if numeig is None:
            numeig = self.model.cor.shape[0]*3
        
        [self.e,self.v] = np.linalg.eig(self.hess)
        self.v = self.v[:,self.e.argsort()]
        self.e.sort()
        self.v = self.v[:,0:numeig]
        self.e = self.e[0:numeig]
            
        if not self.freqChecker():
            warnings.warn("Not all eigenvalues converged, results might be inaccurate")
            print self.e[0:7]
            
    
    def freqChecker(self):
        '''
        checks if the first 6 modes have a frequency of 0
        '''
        flag = False
        if sum(self.e[0:6]) < 1e-10 and sum(self.e[0:7]) > 1e-10:
            flag = True
        
        return flag
        
    def calcInternalDis(self):
        self.getHinv()
        length = self.model.cor.shape[0]
        self.internalDis = np.zeros((length, length), dtype = float)
        
        for i in xrange(length):
            for j in xrange(length):
                self.internalDis[i, j] = self.hinv[i, i] + self.hinv[j, j] - 2*self.hinv[i, j]
            
        
    
    
    def calcMSF(self):
        '''
        calculate the Mean Square Fluctuations from ANM
        '''
        self.cx = self.getCX()
        self.hess = self.getHess()
        
        if self.e is None:
            self.calcModes()
            
        self.MSF = np.zeros((1, self.model.length), dtype = float)
        
        cv1 = range(0, self.model.length*3, 3)
        cv2 = range(1, self.model.length*3, 3)
        cv3 = range(2, self.model.length*3, 3)
        
        for i in range(6, self.model.length*3):
            v_temp = self.v[:,i]**2
            self.MSF = self.MSF + (1/(self.e[i])) * (v_temp[cv1]+v_temp[cv2]+v_temp[cv3])
        
        self.MSF =  (8/3)*(self.PI**2)*self.KB*(self.T/self.GAMMA)*self.MSF
     
    def arrowGenerator(self, mode = 1, color = [1,1,1], size = 5):
        self.v = self.getV()
        self.arrows = list()
        
        for i in range(self.model.length):
            tail = [CYLINDER, self.model.cor[i,0], self.model.cor[i,1], self.model.cor[i,2],\
                    self.model.cor[i,0]+size*16*self.v[3*i,mode+5], self.model.cor[i,1]+size*16*self.v[3*i+1,mode+5], self.model.cor[i,2]+size*16*self.v[3*i+2,mode+5],\
                    0.3, color[0], color[1], color[2], color[0], color[1], color[2]]
            self.arrows.extend(tail)
            
            head = [CONE, self.model.cor[i,0]+size*16*self.v[3*i,mode+5], self.model.cor[i,1]+size*16*self.v[3*i+1,mode+5], self.model.cor[i,2]+size*16*self.v[3*i+2,mode+5],\
                   self.model.cor[i,0]+size*20*self.v[3*i,mode+5], self.model.cor[i,1]+size*20*self.v[3*i+1,mode+5], self.model.cor[i,2]+size*20*self.v[3*i+2,mode+5],\
                   1, 0.0, color[0], color[1], color[2], color[0], color[1], color[2], 1.0, 1.0]
            self.arrows.extend(head)
            
    def modeAnimator(self, modes = [1,2,3], useAllAtom = False, scaler = 5):
        self.v = self.getV()
        for i in modes:
            movieFileName = 'movie.pdb'
            outfile = open(movieFileName,'w')
            
            for j in range(11):
                tempCor = self.model.cor + scaler*j*(self.v[:,i+5].reshape((len(self.v)/3, 3)))
                outfile.write('MODEL  %4d\n' %(j+1))
                for k in range(self.model.length):
                    outfile.write('%-6s%5d  %-4s%3s %1s%4d    %8.3f%8.3f%8.3f%6.2f%6.2f           %-4s\n' %(self.model.line_type[k], self.model.atom_number[k], self.model.atom_name[k], self.model.residue_name[k], self.model.chain_id[k], self.model.residue_number[k],tempCor[k,0], tempCor[k,1], tempCor[k,2], self.model.occupancy[k], self.model.b_factor[k], self.model.element[k]))
                outfile.write('ENDMDL\n')
            
            for j in range(10):
                tempCor = self.model.cor + scaler*(10-j)*(self.v[:,i+5].reshape((len(self.v)/3, 3)))
                outfile.write('MODEL  %4d\n' %(j+12))
                for k in range(self.model.length):
                    outfile.write('%-6s%5d  %-4s%3s %1s%4d    %8.3f%8.3f%8.3f%6.2f%6.2f           %-4s\n' %(self.model.line_type[k], self.model.atom_number[k], self.model.atom_name[k], self.model.residue_name[k], self.model.chain_id[k], self.model.residue_number[k],tempCor[k,0], tempCor[k,1], tempCor[k,2], self.model.occupancy[k], self.model.b_factor[k], self.model.element[k]))
                outfile.write('ENDMDL\n')
            
            for j in range(11):
                tempCor = self.model.cor - scaler*j*(self.v[:,i+5].reshape((len(self.v)/3, 3)))
                outfile.write('MODEL  %4d\n' %(j+22))
                for k in range(self.model.length):
                    outfile.write('%-6s%5d  %-4s%3s %1s%4d    %8.3f%8.3f%8.3f%6.2f%6.2f           %-4s\n' %(self.model.line_type[k], self.model.atom_number[k], self.model.atom_name[k], self.model.residue_name[k], self.model.chain_id[k], self.model.residue_number[k],tempCor[k,0], tempCor[k,1], tempCor[k,2], self.model.occupancy[k], self.model.b_factor[k], self.model.element[k]))
                outfile.write('ENDMDL\n')
                
            for j in range(10):
                tempCor = self.model.cor - scaler*(10-j)*(self.v[:,i+5].reshape((len(self.v)/3, 3)))
                outfile.write('MODEL  %4d\n' %(j+33))
                for k in range(self.model.length):
                    outfile.write('%-6s%5d  %-4s%3s %1s%4d    %8.3f%8.3f%8.3f%6.2f%6.2f           %-4s\n' %(self.model.line_type[k], self.model.atom_number[k], self.model.atom_name[k], self.model.residue_name[k], self.model.chain_id[k], self.model.residue_number[k],tempCor[k,0], tempCor[k,1], tempCor[k,2], self.model.occupancy[k], self.model.b_factor[k], self.model.element[k]))
                outfile.write('ENDMDL\n')
            
            outfile.close()