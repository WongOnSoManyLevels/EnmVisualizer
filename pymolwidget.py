# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 14:02:01 2015

@author: yuanwang
"""
#import sys
#sys.path.append('/usr/lib64/python2.6/site-packages')
from PyQt4.QtOpenGL import *
from PyQt4 import QtCore
from PyQt4.Qt import Qt
from OpenGL.GL import *
import pymol2
from pymol.cgo import *
 
buttonMap = {
    Qt.LeftButton:0,
    Qt.MidButton:1,
    Qt.RightButton:2,
}
 
class PyMolWidget(QGLWidget):
    def __init__(self, parent=None):
        self._enableUi = True
        f = QGLFormat()
        f.setStencil(True)
        f.setRgba(True)
        f.setDepth(True)
        f.setDoubleBuffer(True)
        super(PyMolWidget, self).__init__(f, parent)
        self._pymol = pymol2.PyMOL()
        self._pymol.start()
        
        
        if self._enableUi:
            self._pymol.cmd.set("internal_gui", 0)
            self._pymol.cmd.set("internal_feedback", 0)
            self._pymol.cmd.button("double_left", "None", "None")
            self._pymol.cmd.button("single_right", "None", "None")
 
        self._pymol.reshape(self.width(), self.height())
        self.resizeGL(self.width(), self.height())
        self._pymolProcess()
        self.playMovie()
 
    def initializeGL(self):
        """ 
        Reimplemented from QGLWidget
        
        Instance PyMOL _only_ when we're sure there's an OGL context up and running
        (i.e. in this method :-)
        
        self._pymol = pymol2.PyMOL()
        self._pymol.start()
        
        if not self._enableUi:
            self._pymol.cmd.set("internal_gui", 0)
            self._pymol.cmd.set("internal_feedback", 0)
            self._pymol.cmd.button("double_left", "None", "None")
            self._pymol.cmd.button("single_right", "None", "None")
 
        self._pymol.reshape(self.width(), self.height())
        self.resizeGL(self.width(), self.height())
        self._pymolProcess()
        """
        
    def paintGL(self):
        glViewport(0, 0, self.width(), self.height())
        self._pymol.idle()
        self._pymol.draw()
 
    def resizeGL(self, w, h):
        self._pymol.reshape(w, h, True)
        self._pymolProcess()
 
    def loadMolFile(self, mol_file):
        self._pymol.cmd.load(str(mol_file))
    
    def playMovie(self):
        self._pymol.cmd.mplay()
        self._pymolProcess()
 
    def _pymolProcess(self):
        self._pymol.idle()
        self.update()
    
    def mouseMoveEvent(self, ev):
        self._pymol.drag(ev.x(), self.height() - ev.y(), 0)
        self._pymolProcess()
 
    def mousePressEvent(self, ev):
        if not self._enableUi:
            self._pymol.cmd.button("double_left", "None", "None")
            self._pymol.cmd.button("single_right", "None", "None")
        self._pymol.button(buttonMap[ev.button()], 0, ev.x(), self.height() - ev.y(), 0)
        self._pymolProcess()
 
    def mouseReleaseEvent(self, ev):
        self._pymol.button(buttonMap[ev.button()], 1, ev.x(), self.height() - ev.y(), 0)
        self._pymolProcess()
 
    def wheelEvent(self, ev):
        button = 3 if ev.delta() > 0 else 4
        self._pymol.button(button, 0, ev.x(), ev.y(), 0)
        self._pymolProcess()
        
    def sizeHint(self):
        return QtCore.QSize(300, 300)
    