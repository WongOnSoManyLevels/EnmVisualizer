# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 13:51:16 2015

@author: yuanwang
"""

#!/usr/bin/python
"""
PyMol Widget

Usage:
    main.py [input_files]

Options:
    -h, --help: print this screen
"""

from pymolwidget import PyMolWidget
from PyQt4 import QtGui, QtCore
import sys, getopt
 
 
class Usage(Exception):
    """
    """
    def __init__(self, msg):
        self.msg = msg
 
 
if __name__ == '__main__':
    argv = sys.argv
    app = QtGui.QApplication(argv)
    kinect_enabled = True
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
 
        # process options
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                sys.exit(0)
    
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        sys.exit(2)
 
    # process args
    input_files = []
    if len(args):
        input_files = args[:]
  
    window = PyMolWidget()
    window.show()
    for f in input_files:
        window.loadMolFile(f)
    window.playMovie()
 
    sys.exit(app.exec_())