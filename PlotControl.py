# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 09:29:54 2015

@author: yuanwang
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class plotControl(QDialog):
    def __init__(self, parent = None):
        super(plotControl, self).__init__(parent)
        
        label = QLabel('Please choose what to plot:')
        self.msfButton = QPushButton('MSF and Frequencies')
        self.cxButton = QPushButton('Contact Matrix')
        self.internalDButton = QPushButton('Internal Distance Matrix')
        self.clusterButton = QPushButton('Internal Distance Clustering')
        self.msfButton.setEnabled(False)
        self.cxButton.setEnabled(False)
        self.internalDButton.setEnabled(False)
        self.clusterButton.setEnabled(False)
        
        grid = QGridLayout()
        grid.addWidget(label, 0, 0)
        grid.addWidget(self.msfButton, 1, 0)
        grid.addWidget(self.cxButton, 1, 1)
        grid.addWidget(self.internalDButton, 2, 0)
        grid.addWidget(self.clusterButton, 2, 1)
        self.setLayout(grid)
        self.setMaximumHeight(100)
        
        self.setWindowTitle('Plot Control Panel')
        
if __name__ == '__main__':
    import sys    
    app = QApplication(sys.argv)
    form = plotControl()
    form.show()
    sys.exit(app.exec_())