# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 15:38:56 2015

@author: Yuan
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class anmDlg(QDialog):
    def __init__(self, parent = None):
        super(anmDlg, self).__init__(parent)
        
        self.cutoffCheckbox = QCheckBox('Cutoff Model')
        self.cutoffCheckbox.checkStateSet()
        self.cutoffCheckbox.setChecked(True)
        cutoffLabel = QLabel('Cutoff Value:')
        self.cutoffSpinBox = QDoubleSpinBox()
        self.cutoffSpinBox.setSuffix('A')
        self.cutoffSpinBox.setValue(12.0)
        self.cutoffSpinBox.setRange(6.0, 18.0)
        self.cutoffSpinBox.setSingleStep(0.5)
        cutoffLabel.setBuddy(self.cutoffSpinBox)
        self.pfCheckBox = QCheckBox('Parameter Free Model')
        pfLabel = QLabel('Power:')
        self.pfSpinBox = QDoubleSpinBox()
        self.pfSpinBox.setValue(5.0)
        self.pfSpinBox.setRange(2.0, 10.0)
        self.pfSpinBox.setSingleStep(0.5)
        
        self.includeHetCheckBox = QCheckBox('Include HETATM')
        self.caCheckBox = QCheckBox('Alpha Carbon Only')
        self.caCheckBox.setChecked(True)
        
        self.buildButton = QPushButton('Build ANM')
        
        grid = QGridLayout()
        grid.addWidget(self.cutoffCheckbox, 0, 0, 2, 0)
        grid.addWidget(cutoffLabel, 1, 0)
        grid.addWidget(self.cutoffSpinBox, 1, 1)
        grid.addWidget(self.pfCheckBox, 2, 0, 2, 0)
        grid.addWidget(pfLabel, 3, 0)
        grid.addWidget(self.pfSpinBox, 3, 1)
        grid.addWidget(self.includeHetCheckBox, 4, 0, 2, 0)
        grid.addWidget(self.caCheckBox, 5, 0, 2, 0)
        grid.addWidget(self.buildButton, 6, 2)
        self.setLayout(grid)
        self.setWindowTitle('Anm Parameters:')
        
        self.connect(self.cutoffCheckbox, SIGNAL('stateChanged(int)'),
                     self.cutoffBoxChanged)
        self.connect(self.pfCheckBox, SIGNAL('stateChanged(int)'),
                     self.pfBoxChanged)
                     
        self.setMaximumSize(300, 300)
                     
    def cutoffBoxChanged(self, value):
        self.cutoffCheckbox.setCheckState(value)
        if self.pfCheckBox.isChecked():
            self.pfCheckBox.setChecked(False)
        else:
            self.pfCheckBox.setChecked(True)
            
    def pfBoxChanged(self, value):
        self.pfCheckBox.setCheckState(value)
        if self.cutoffCheckbox.isChecked():
            self.cutoffCheckbox.setChecked(False)
        else:
            self.cutoffCheckbox.setChecked(True)
        
if __name__ == '__main__':
    import sys    
    app = QApplication(sys.argv)
    form = anmDlg()
    form.show()
    sys.exit(app.exec_())
        