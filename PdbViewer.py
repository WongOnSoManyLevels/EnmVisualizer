# -*- coding: utf-8 -*-
"""
Created on Sun Mar 08 16:41:34 2015

@author: Yuan
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PdbParser import *
import warnings

class pdbViewer(QTableWidget):
    def __init__(self, model = None, parent = None):
        super(pdbViewer, self).__init__(parent)
        
        self.clear()
        self.setSortingEnabled(False)
        self.model = model
        if isinstance(self.model, pdbModel):
            length = self.model.length
            pass
        elif isinstance(self.model, pdbParser):
            if len(model) > 1:
                warnings.warn('Mutiple models found, will use the first model')
            self.model = self.model.getModel()
            length = self.model.length
        elif self.model == None:
            length = 10
            pass
        else:
            raise TypeError('Unrecgonized model type')
            
        self.setColumnCount(12)
        self.setRowCount(length)
        columnLabels = ['Line Type', 'Atom Number', 'Atom Name', 'Residue Name',\
                        'Chain ID', 'Residue Number', 'X', 'Y', 'Z', 'Occupancy', \
                        'B Factor', 'Element']
        self.setHorizontalHeaderLabels(columnLabels)
        if self.model:        
            self.populateTable(self.model)
        
    def isModified(self):
        self.dirty = True
        
    def populateTable(self, model):
        self.model = model
        self.setColumnCount(12)
        self.setRowCount(self.model.length)
        columnLabels = ['Line Type', 'Atom Number', 'Atom Name', 'Residue Name',\
                        'Chain ID', 'Residue Number', 'X', 'Y', 'Z', 'Occupancy', \
                        'B Factor', 'Element']
        self.setHorizontalHeaderLabels(columnLabels)
        
        self.hiddenColumnIndexes = []
        self.rowsToRemove = []
        self.dirty = False
        self.itemChanged.connect(self.isModified)
       
        for i in xrange(self.model.length):
            self.setItem(i, 0, self.lineTypeItem(i))
            self.setItem(i, 1, self.atomNumberItem(i))
            self.setItem(i, 2, self.atomNameItem(i))
            self.setItem(i, 3, self.residueNameItem(i))
            self.setItem(i, 4, self.chainIDItem(i))
            self.setItem(i, 5, self.residueNumberItem(i))
            self.setItem(i, 6, self.corXItem(i))
            self.setItem(i, 7, self.corYItem(i))
            self.setItem(i, 8, self.corZItem(i))
            self.setItem(i, 9, self.occupancyItem(i))
            self.setItem(i, 10, self.bFactorItem(i))
            self.setItem(i, 11, self.elementItem(i))
            
        self.resizeColumnsToContents()
    
    def itemProcess(self, item, row):
        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        if self.model.atom_name[row] == 'CA':
            item.setBackgroundColor(QColor(240, 255, 240))
        return item
    
    
    def lineTypeItem(self, row):
        item = QTableWidgetItem(str(self.model.line_type[row]))
        return self.itemProcess(item, row)
        
    def atomNumberItem(self, row):
        item = QTableWidgetItem(str(self.model.atom_number[row]))
        return self.itemProcess(item, row)
        
    def atomNameItem(self, row):
        item = QTableWidgetItem(str(self.model.atom_name[row]))
        return self.itemProcess(item, row)
        
    def residueNameItem(self, row):
        item = QTableWidgetItem(str(self.model.residue_name[row]))
        return self.itemProcess(item, row)
        
    def chainIDItem(self, row):
        item = QTableWidgetItem(str(self.model.chain_id[row]))
        return self.itemProcess(item, row)
        
    def residueNumberItem(self, row):
        item = QTableWidgetItem(str(self.model.residue_number[row]))
        return self.itemProcess(item, row)
        
    def corXItem(self, row):
        item = QTableWidgetItem(str(self.model.cor[row, 0]))
        return self.itemProcess(item, row)
        
    def corYItem(self, row):
        item = QTableWidgetItem(str(self.model.cor[row, 1]))
        return self.itemProcess(item, row)
        
    def corZItem(self, row):
        item = QTableWidgetItem(str(self.model.cor[row, 2]))
        return self.itemProcess(item, row)
        
    def occupancyItem(self, row):
        item = QTableWidgetItem(str(self.model.occupancy[row]))
        return self.itemProcess(item, row)
        
    def bFactorItem(self, row):
        item = QTableWidgetItem(str(self.model.b_factor[row]))
        return self.itemProcess(item, row)
        
    def elementItem(self, row):
        item = QTableWidgetItem(str(self.model.element[row]))
        return self.itemProcess(item, row)
        
    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_H:
                allSelectedIndexes = self.selectedIndexes() 
                if not len(allSelectedIndexes) == self.rowCount():
                    return
                columnIndex = allSelectedIndexes[0].column()                
                for item in allSelectedIndexes:
                    if not item.column() == columnIndex:
                        return
                self.hideColumn(columnIndex)
                self.hiddenColumnIndexes.append(columnIndex)
            if event.key() == Qt.Key_S:
                try:
                    columnIndex = self.hiddenColumnIndexes.pop()
                    self.setColumnHidden(columnIndex, False)
                except IndexError:
                    return
        elif event.key() == Qt.Key_Delete:
            rowsToRemove = []            
            allSelectedIndexes = self.selectedIndexes()
            if len(allSelectedIndexes) == 0:
                return
            for item in allSelectedIndexes:
                if item.row() not in rowsToRemove:
                    rowsToRemove.append(item.row())
            if QMessageBox.question(self, 'PdbViewer - Delete Rows',\
                '%d rows will be deleted, continue?' % len(rowsToRemove),\
                QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
                for row in rowsToRemove:
                    print row
                    self.hideRow(row)
                self.dirty = True
                self.rowsToRemove.append(rowsToRemove)
        else:
            QTableWidget.keyPressEvent(self, event)
            
            
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    hiv = pdbParser('1WDN')
    table = pdbViewer(hiv)
    table.show()
    sys.exit(app.exec_())
