# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 20:44:40 2015

@author: Yuan
"""

from __future__ import division
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ANM import *
from PdbParser import *

class freqAndMSFPainter(QDialog):
    FONT = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 18}
    matplotlib.rc('font', **FONT)
            
    def __init__(self, anm, parent = None):
        super(freqAndMSFPainter, self).__init__(parent)
        
        self.anm = anm
        
        if not isinstance(self.anm, ANM):
            raise ValueError('Unrecgonized ANM type')
            
        self.figure, (self.ax1, self.ax2) = plt.subplots(1, 2)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.plot()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)
        
    def plot(self):
        self.ax1.bar(np.arange(50), anm.e[:50], 1, color = 'white',
                     edgecolor = 'black')
        self.ax1.set_xlabel('Mode Index')
        self.ax1.set_ylabel('Frequencies')
        self.ax1.set_ylim([0, anm.e[50]*1.1])
        self.ax1.set_title('Mode Frequencies')
        self.ax2.plot(range(len(anm)), np.transpose(anm.getMSF()), color = 'black',\
                      lw = 1.5)
        self.ax2.set_xlabel('Residue Index')
        self.ax2.set_ylabel('Mean Square Fluctuation')
        self.ax2.set_xlim([0,len(anm)])
        self.ax2.set_title('MSF')
        
        
if __name__ == '__main__':
    import sys    
    app = QApplication(sys.argv)
    gln = pdbParser('1VRE')
    anm = ANM(gln)
    anm.calcModes()
    main = freqAndMSFPainter(anm)
    main.show()

    sys.exit(app.exec_())
        
        
        