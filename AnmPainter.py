# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 20:44:40 2015

@author: Yuan
"""

from __future__ import division
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ANM import *
import scipy
import pylab
import scipy.cluster.hierarchy as sch
from mathFunctions import *



class anmPainter(QDialog):
    FONT = {'weight' : 'bold',
            'size'   : 18}
    matplotlib.rc('font', **FONT)
            
    def __init__(self, anm = None, parent = None):
        super(anmPainter, self).__init__(parent)
        
        self.anm = anm
        
        if not (isinstance(self.anm, ANM) or self.anm is None):
            raise ValueError('Unrecgonized ANM type')
            
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)        
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
    def populateAnm(self, anm):
        self.anm = anm
        
    @waitingEffects    
    def plotFreqAndMSF(self):
        if self.anm is None:
            return
        self.figure.clf()
        self.ax1 = self.figure.add_subplot(211)
        self.ax2 = self.figure.add_subplot(212)
        self.ax1.bar(np.arange(50), self.anm.e[:50], 1, color = 'white',
                     edgecolor = 'black')
        self.ax1.set_xlabel('Mode Index')
        self.ax1.set_ylabel('Frequencies')
        self.ax1.set_ylim([0, self.anm.e[50]*1.1])
        self.ax1.set_title('Mode Frequencies')
        self.ax2.plot(range(len(self.anm)), np.transpose(self.anm.getMSF()), color = 'black',\
                      lw = 1.5)
        self.ax2.set_xlabel('Residue Index')
        self.ax2.set_ylabel('Mean Square Fluctuation')
        self.ax2.set_xlim([0,len(self.anm)])
        self.ax2.set_title('MSF')
        self.canvas.draw()
    
    @waitingEffects    
    def plotCX(self):
        if self.anm is None:
            return
        self.figure.clf()
        self.ax3 = self.figure.add_subplot(111)
        self.ax3.set_xlabel('Residue Index')
        self.ax3.set_ylabel('Residue Index')
        self.ax3.set_xlim([0, len(self.anm.getCX())])
        self.ax3.set_ylim([0, len(self.anm.getCX())])
        self.ax3.pcolor(self.anm.getCX(), cmap = plt.cm.Blues)
        self.canvas.draw()
     
    @waitingEffects 
    def plotInternalD(self):
        if self.anm is None:
            return
        self.figure.clf()
        self.ax4 = self.figure.add_subplot(111)
        self.ax4.set_xlabel('Residue Index')
        self.ax4.set_ylabel('Residue Index')
        self.ax4.set_xlim([0, len(self.anm.getInternalDis())])
        self.ax4.set_ylim([0, len(self.anm.getInternalDis())])
        self.ax4.set_title('Internal Distance Matrix')
        self.ax4.pcolor(self.anm.getInternalDis(), cmap = plt.cm.Blues)
        self.canvas.draw()
        
    def plotCluster(self):
        if self.anm is None:
            return
            
        self.figure.clf()
        self.ax5 = self.figure.add_subplot(111)
        self.ax5.imshow('cluster.png')
        self.canvas.draw()
       
        
       
if __name__ == '__main__':
    import sys
    from PdbParser import *    
    app = QApplication(sys.argv)
    gln = pdbParser('1t3r.pdb')
    anm = ANM(gln)
    anm.calcModes()
    main = anmPainter()
    main.show()

    sys.exit(app.exec_())
        
        
        