# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 18:47:50 2015

@author: yuanwang
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class pymolControl(QDialog):
    def __init__(self, parent = None):
        super(pymolControl, self).__init__(parent)
        
        cmdLabel = QLabel('Type Command:')
        self.cmdLineEdit = cmdLineEdit()
        self.cmdSubmitButton = QPushButton('Submit')
        
        self.springButton = QPushButton('Show Springs')
        self.springColorButton = QPushButton('Spring Color')
        self.springButton.setEnabled(False)
        self.springColorButton.setEnabled(False)
        
        self.arrowButton = QPushButton('Draw Arrows')
        arrowModeLabel = QLabel('Mode Index:')
        self.arrowModeLineEdit = QLineEdit()
        self.arrowModeLineEdit.setFixedWidth(40)
        self.arrowColorButton = QPushButton('Arrow Color')
        arrowSizeLabel = QLabel('Arrow Size:')
        self.arrowSizeSlider = QSlider(Qt.Horizontal)
        self.arrowButton.setEnabled(False)
        self.arrowColorButton.setEnabled(False)
        self.arrowSizeSlider.setEnabled(False)
        self.arrowSizeSlider.setMinimum(0.1)
        self.arrowSizeSlider.setMaximum(10.1)
        self.arrowSizeSlider.setSliderPosition(5)
        self.arrowSizeSlider.setTracking(False)
        
        self.movieButton = QPushButton('Make Movies')
        movieModeLabel = QLabel('Mode Index:')
        self.movieModeLineEdit = QLineEdit()
        self.movieModeLineEdit.setFixedWidth(40)
        self.movieColorButton = QPushButton('Movie Color')
        movieSizeLabel = QLabel('Movie Scale:')
        self.movieSizeSlider = QSlider(Qt.Horizontal)
        self.movieButton.setEnabled(False)
        self.movieColorButton.setEnabled(False)
        self.movieSizeSlider.setEnabled(False)
        self.movieSizeSlider.setMinimum(0.1)
        self.movieSizeSlider.setMaximum(10.1)
        self.movieSizeSlider.setSliderPosition(5)
        self.movieSizeSlider.setTracking(False)
        
        self.msfButton = QPushButton('Color By MSF')
        self.msfButton.setEnabled(False)
        
        grid = QGridLayout()
        grid.addWidget(cmdLabel, 0, 0)
        grid.addWidget(self.cmdLineEdit, 0, 1, 1, 3)
        grid.addWidget(self.cmdSubmitButton, 0, 4)
        grid.addWidget(self.springButton, 1, 0)
        grid.addWidget(self.springColorButton, 1, 1)
        grid.addWidget(self.msfButton, 1, 5)
        grid.addWidget(self.arrowButton, 2, 0)
        grid.addWidget(self.arrowColorButton, 2, 1)
        grid.addWidget(arrowModeLabel, 2, 2)
        grid.addWidget(self.arrowModeLineEdit, 2, 3)        
        grid.addWidget(arrowSizeLabel, 2, 4)
        grid.addWidget(self.arrowSizeSlider, 2, 5)
        grid.addWidget(self.movieButton, 3, 0)
        grid.addWidget(self.movieColorButton, 3, 1)
        grid.addWidget(movieModeLabel, 3, 2)
        grid.addWidget(self.movieModeLineEdit, 3, 3)
        grid.addWidget(movieSizeLabel, 3, 4)
        grid.addWidget(self.movieSizeSlider, 3, 5)
        
        
        self.setLayout(grid)
        self.setWindowTitle('Pymol Control Panel')
        
class cmdLineEdit(QLineEdit):
    def __init__(self, parent = None):
        super(cmdLineEdit, self).__init__(parent)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.emit(SIGNAL('upPressed()'))
        elif event.key() == Qt.Key_Down:
            self.emit(SIGNAL('downPressed()'))
        else:
            QLineEdit.keyPressEvent(self, event)
        
if __name__ == '__main__':
    import sys    
    app = QApplication(sys.argv)
    form = pymolControl()
    form.show()
    sys.exit(app.exec_())

        
        
        