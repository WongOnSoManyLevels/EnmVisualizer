# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:53:24 2015

@author: Yuan
"""

import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from AnmPainter import *
from AnmDlg import *
from StructureDlg import *
from PdbViewer import *
from pymolwidget import *
from PdbParser import *
from ANM import *
from mathFunctions import *
from PlotControl import *
from PymolControl import *

class mainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)
        
        self.painter = anmPainter()
        self.plotContrl = plotControl()
        self.centralSplitter = QSplitter(Qt.Vertical)
        self.centralSplitter.addWidget(self.painter)
        self.centralSplitter.addWidget(self.plotContrl)
        self.setCentralWidget(self.centralSplitter)
        
        self.anmDlg = anmDlg()
        self.anmDlg.buildButton.setEnabled(False)
        self.strDlg = structureDlg()
        self.splitter1 = QSplitter(Qt.Vertical)
        self.splitter1.addWidget(self.strDlg)
        self.splitter1.addWidget(self.anmDlg)
        
        basicDockWidget = QDockWidget('Structure Panel', self)
        basicDockWidget.setObjectName('basicDockWidget')
        basicDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        basicDockWidget.setWidget(self.splitter1)
        self.addDockWidget(Qt.LeftDockWidgetArea, basicDockWidget)
        
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        
        self.pdbViewer = pdbViewer()
        
        viewerDockWidget = QDockWidget('Pdb Viewer', self)
        viewerDockWidget.setObjectName('PdbViewer')
        viewerDockWidget.setAllowedAreas(Qt.TopDockWidgetArea|
                                         Qt.BottomDockWidgetArea)
        viewerDockWidget.setWidget(self.pdbViewer)
        self.addDockWidget(Qt.TopDockWidgetArea, viewerDockWidget)
        self.setWindowTitle('ENM Visualizer')
        
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        
        self.pymolWidget = PyMolWidget()
        self.pymolWidget.setMinimumSize(250, 250)
        self.pymolControl = pymolControl()
        self.pymolSplitter = QSplitter(Qt.Vertical)
        self.pymolSplitter.addWidget(self.pymolWidget)
        self.pymolSplitter.addWidget(self.pymolControl)
        pymolDockWidget = QDockWidget('PyMol', self)
        pymolDockWidget.setObjectName('Pymol')
        pymolDockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
        pymolDockWidget.setWidget(self.pymolSplitter)
        self.addDockWidget(Qt.RightDockWidgetArea, pymolDockWidget)
        
        self.statusBar = self.statusBar()
        self.statusBar.showMessage('Ready')
        self.setWindowIcon(QIcon('/image/AppIcon.png'))
        
        self.connect(self.strDlg.submitButton, SIGNAL('clicked()'),
                     self.submitStructure)
        self.connect(self.anmDlg.buildButton, SIGNAL('clicked()'),
                     self.buildANM)
        self.connect(self.pdbViewer, SIGNAL('itemSelectionChanged()'),
                     self.selectInPymol)
        self.connect(self.plotContrl.msfButton, SIGNAL('clicked()'),
                     self.painter.plotFreqAndMSF)
        self.connect(self.plotContrl.cxButton, SIGNAL('clicked()'),
                     self.painter.plotCX)
        self.connect(self.plotContrl.internalDButton, SIGNAL('clicked()'),
                     self.painter.plotInternalD)
        self.connect(self.plotContrl.clusterButton, SIGNAL('clicked()'),
                     self.painter.plotCluster)
        self.connect(self.pymolControl.cmdLineEdit, SIGNAL('returnPressed()'),
                     self.passCmdToPymol)
        self.connect(self.pymolControl.cmdLineEdit, SIGNAL('upPressed()'),
                     self.previousCmd)
        self.connect(self.pymolControl.cmdLineEdit, SIGNAL('downPressed()'),
                     self.nextCmd)
        self.connect(self.pymolControl.cmdSubmitButton, SIGNAL('clicked()'),
                     self.passCmdToPymol)
        self.connect(self.pymolControl.springButton, SIGNAL('clicked()'),
                     self.buildSprings)
        self.connect(self.pymolControl.springColorButton, SIGNAL('clicked()'),
                     self.changeSpringColor)
        self.connect(self.pymolControl.msfButton, SIGNAL('clicked()'),
                     self.colorByMSF)
        self.connect(self.pymolControl.arrowButton, SIGNAL('clicked()'),
                     self.drawArrows)
        self.connect(self.pymolControl.arrowSizeSlider, SIGNAL('valueChanged(int)'),
                     self.drawArrows)
        self.connect(self.pymolControl.arrowColorButton, SIGNAL('clicked()'),
                     self.changeArrowColor)
        self.connect(self.pymolControl.movieButton, SIGNAL('clicked()'),
                     self.makeMovie)
        
        self.strDlg.structureLineEdit.setFocus()
        self.cmdHistory = []
        self.cmdPointer = -1
        self.arrowColor = None
                     
    @waitingEffects                 
    def submitStructure(self):
        fileName = str(self.strDlg.structureLineEdit.text())
        try:
            self.tempModel = pdbParser(fileName)
            self.pdbViewer.populateTable(self.tempModel.model0)
            tempModel = self.tempModel.toCA().writePDB('tempp.pdb')
            if self.tempModel._getMethod == 'local':            
                self.pymolWidget.loadMolFile(fileName)
            elif self.tempModel._getMethod == 'online':
                self.pymolWidget.loadMolFile('temp.pdb')
            self.anmDlg.buildButton.setEnabled(True)
            self.pymolWidget.setFocus()
        except ValueError:
            QMessageBox.warning(self, 'Initialization Failed', 
                               'Failed to read %s' % fileName,
                                QMessageBox.Ok, QMessageBox.NoButton)
            self.strDlg.structureLineEdit.setFocus()
            self.strDlg.structureLineEdit.selectAll()
            
    @waitingEffects  
    def buildANM(self):
        if self.anmDlg.cutoffCheckbox.isChecked():
            anmMethod = 'cutoff'
        elif self.anmDlg.pfCheckBox.isChecked():
            anmMethod = 'pf'
            
        if self.anmDlg.caCheckBox.isChecked():
            useCA = True
        else:
            useCA = False
            
        cutoff = self.anmDlg.cutoffSpinBox.value()
        power = self.anmDlg.pfSpinBox.value()
        
        try:
            self.anm = ANM(self.tempModel.model0, cutoff, useCA, anmMethod, power)
            self.anm.calcModes()
            self.painter.populateAnm(self.anm)
            self.plotContrl.msfButton.setEnabled(True)
            self.plotContrl.cxButton.setEnabled(True)
            self.plotContrl.internalDButton.setEnabled(True)
            self.plotContrl.clusterButton.setEnabled(True)
            self.pymolControl.springButton.setEnabled(True)
            self.pymolControl.springColorButton.setEnabled(True)
            self.pymolControl.arrowButton.setEnabled(True)
            self.pymolControl.arrowColorButton.setEnabled(True)
            self.pymolControl.arrowSizeSlider.setEnabled(True)
            self.pymolControl.movieButton.setEnabled(True)
            self.pymolControl.movieColorButton.setEnabled(True)
            self.pymolControl.movieSizeSlider.setEnabled(True)
            self.pymolControl.msfButton.setEnabled(True)
        except ValueError or TypeError:
            QMessageBox.warning(self, 'ANM Failed', 
                               'Failed to build an ANM',
                                QMessageBox.Ok, QMessageBox.NoButton)
                                
    def passCmdToPymol(self):
        cmd = str(self.pymolControl.cmdLineEdit.text())
        self.cmdHistory.append(cmd)
        self.cmdPointer = -1
        self.pymolWidget._pymol.cmd.do(cmd)
        self.pymolControl.cmdLineEdit.clear()
        self.pymolWidget.setFocus()
        self.pymolControl.cmdLineEdit.setFocus()
        
    def previousCmd(self):
        try:        
            self.pymolControl.cmdLineEdit.setText(self.cmdHistory[self.cmdPointer])
            self.cmdPointer -= 1
        except IndexError:
            pass
            
    def nextCmd(self):
        if self.cmdPointer == -1:
            self.pymolControl.cmdLineEdit.clear()
        else:
            self.cmdPointer += 1          
            self.pymolControl.cmdLineEdit.setText(self.cmdHistory[self.cmdPointer])
            
    def buildSprings(self):
        springFileName = 'springs_temp.pdb'
        objName = 'springs_temp'
        objList = self.pymolWidget._pymol.cmd.get_names()
        if objName in objList:
            self.pymolWidget._pymol.cmd.delete(objName)
        tempCAModel = self.tempModel.toCA()
        tempCAModel.writePDB(springFileName)
        springFile = open(springFileName, 'a')
        for i in xrange(len(self.anm.contactPair_x)):
            springFile.write('CONECT %4d %4d\n' %
                             (tempCAModel.getModel().atom_number[self.anm.contactPair_x[i]],
                              tempCAModel.getModel().atom_number[self.anm.contactPair_y[i]]))
        springFile.close()
        self.pymolWidget._pymol.cmd.hide('everything')
        self.pymolWidget._pymol.cmd.load(springFileName)
        self.pymolWidget.setFocus()
        self.pymolControl.springColorButton.setFocus()
        os.remove(springFileName)
        
    def changeSpringColor(self):
        color = QColorDialog.getColor(Qt.blue)
        
        if color.isValid():
            rgb = color.getRgbF()
            self.pymolWidget._pymol.cmd.set_color('tempColor', 
                                                  [rgb[0], rgb[1], rgb[2]])
            self.pymolWidget._pymol.cmd.color('tempColor', 'springs_temp')
            
    def changeArrowColor(self):
        color = QColorDialog.getColor(Qt.white)
        
        if color.isValid():
            rgb = color.getRgbF()
            self.arrowColor = [rgb[0], rgb[1], rgb[2]]
            self.drawArrows()
    
    def colorByMSF(self):
        msf = self.anm.getMSF().tolist()[0]
        msfFileName = 'msf_temp.pdb'
        objName = 'msf_temp'
        objList = self.pymolWidget._pymol.cmd.get_names()
        if objName in objList:
            self.pymolWidget._pymol.cmd.delete(objName)
        tempCAModel = self.tempModel.toCA()
        tempCAModel.model0.b_factor = msf
        tempCAModel.writePDB(msfFileName)
        
        self.pymolWidget._pymol.cmd.hide('everything')
        self.pymolWidget._pymol.cmd.load(msfFileName)
        self.pymolWidget._pymol.cmd.set('cartoon_trace', 1)
        self.pymolWidget._pymol.cmd.show('cartoon', objName)
        self.pymolWidget._pymol.cmd.spectrum('b', 'cyan_yellow', objName)
        self.pymolWidget.setFocus()
        self.pymolControl.msfButton.setFocus(True)
    
    def drawArrows(self):
        if self.arrowColor is None:
            self.arrowColor = [1, 1, 1]
            
        objName = 'arrows'
        objList = self.pymolWidget._pymol.cmd.get_names()
        if objName in objList:
            self.pymolWidget._pymol.cmd.delete(objName)
            
        arrowSize = self.pymolControl.arrowSizeSlider.value()
        mode = int(self.pymolControl.arrowModeLineEdit.text())
        
        self.anm.arrowGenerator(mode = mode, color = self.arrowColor, size = arrowSize)
        self.pymolWidget._pymol.cmd.hide('everything')
        self.pymolWidget._pymol.cmd.set('cartoon_trace', 1)
        self.pymolWidget._pymol.cmd.load('tempp.pdb')
        self.pymolWidget._pymol.cmd.do('as cartoon, tempp')
        self.pymolWidget._pymol.cmd.load_cgo(self.anm.arrows, objName)
        self.pymolWidget.setFocus()
        self.pymolControl.arrowButton.setFocus(True)
        
    def makeMovie(self):
        objName = 'movie'
        objList = self.pymolWidget._pymol.cmd.get_names()
        if objName in objList:
            self.pymolWidget._pymol.cmd.delete(objName)
            
        movieSize = self.pymolControl.movieSizeSlider.value()
        mode = int(self.pymolControl.movieModeLineEdit.text())
        
        self.anm.modeAnimator(modes = [mode], scaler = movieSize)
        self.pymolWidget._pymol.cmd.hide('everything')
        self.pymolWidget._pymol.cmd.load('movie.pdb')
        self.pymolWidget.setFocus()
        self.pymolWidget.playMovie()
        #self.pymolControl.movieButton.setFocus()
        
    def selectInPymol(self):
        rowsToSelect = []            
        allSelectedIndexes = self.pdbViewer.selectedIndexes()
        if len(allSelectedIndexes) == 0:
            return
        for item in allSelectedIndexes:
            if item.row() not in rowsToSelect:
                rowsToSelect.append(item.row())
                    
        if len(rowsToSelect) == 1:
            self.pymolWidget._pymol.cmd.do('select aa, resi %d and chain a' %int(rowsToSelect[0]))
            self.pymolWidget._pymolProcess()
    
        
        

        
        
    
        
            
        
        
if __name__ == '__main__':
    import sys    
    app = QApplication(sys.argv)
    form = mainWindow()
    form.show()
    sys.exit(app.exec_())
        
        