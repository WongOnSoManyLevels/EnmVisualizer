# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 14:21:06 2015

@author: Yuan
"""


from PyQt4.QtCore import *
from PyQt4.QtGui import *

class structureDlg(QDialog):
    def __init__(self, parent = None):
        super(structureDlg, self).__init__(parent)
        
        structureLabel = QLabel('Structure:')
        self.structureLineEdit = QLineEdit()
        self.structureLineEdit.setFixedWidth(100)
        self.browseButton = QPushButton('Browse...')
        self.submitButton = QPushButton('Submit')
        self.submitButton.setEnabled(False)
        self.clearButton = QPushButton('Clear')
        
        grid = QGridLayout()
        grid.addWidget(structureLabel, 0, 0)
        grid.addWidget(self.structureLineEdit, 0, 1)
        grid.addWidget(self.browseButton, 0, 2)
        grid.addWidget(self.submitButton, 1, 1)
        grid.addWidget(self.clearButton, 1, 2)
        self.setLayout(grid)
        self.setWindowTitle('Select Structure:')
        
        self.connect(self.clearButton, SIGNAL('clicked()'), 
                     self.structureLineEdit.clear)
        self.connect(self.browseButton, SIGNAL('clicked()'),
                     self.getFileLocation)
        self.connect(self.structureLineEdit, SIGNAL('textChanged(QString)'),
                     self.submitButtonControl)
                     
        self.setMaximumSize(300, 70)
                     
    def getFileLocation(self):
        fileLocaion = unicode(QFileDialog.getOpenFileName(self, 
                         'Choose PDB File', '.', 
                         '*.pdb'))
                         
        if fileLocaion:
            self.structureLineEdit.setText(fileLocaion)
            
    def submitButtonControl(self, text):
        if bool(text) is False:
            self.submitButton.setEnabled(False)
        else:
            self.submitButton.setEnabled(True)
                     
                     
                     
                     
if __name__ == '__main__':
    import sys    
    app = QApplication(sys.argv)
    form = structureDlg()
    form.show()
    sys.exit(app.exec_())