# -*- coding: utf-8 -*-
"""
Created on Mon Mar 02 09:58:15 2015

@author: yuanwang
"""
import numpy as np
import urllib2
from urllib2 import HTTPError


class pdbParser:
    def __init__(self, filename, includeHET = False, onlineFetch = True):
        '''
        A pdb parser for formal pdb format
        
        filename:   the pdb file to be parsed
        includeHET: if HETATM in pdb should be included, default is false (do not include)
        '''
        try:        
            pdbfile = open(filename,'r')
            self._getMethod = 'local'
        except IOError:
            if onlineFetch:
                pdbURL = 'http://www.pdb.org/pdb/files/' + filename.upper() \
                         + '.pdb'
                try:
                    resp = urllib2.urlopen(pdbURL)
                    context = resp.read()
                    if context[0:9] == '<!DOCTYPE':
                        raise ValueError('Initialization failed -- Wrong directory or PDB ID')
                    f = open('temp.pdb', 'w')
                    f.write(context)
                    f.close()
                    pdbfile = open('temp.pdb', 'r')
                    self._getMethod = 'online'
                except HTTPError:
                    raise ValueError('Initialization failed -- Wrong directory or PDB ID')
        
        self._filename = filename
        self._fragment = list()
        self._modelCount = 0
        self._currentModelNumber = 0
        self._modelList = list()            
        
        for line in pdbfile:
            if line.startswith('MODEL') and self._fragment:
                self._addModel(self._fragment)
                self._fragment = list()
            elif includeHET and (line.startswith('ATOM') or line.startswith('HETATM')):
                self._fragment.append(line)
            elif not includeHET and line.startswith('ATOM'):
                self._fragment.append(line)
                
        if self._fragment:
            self._addModel(self._fragment)
        
        pdbfile.close()
        
    def _addModel(self, fragment):
        model = pdbModel(fragment)
        cmd = 'self.model' + str(self._modelCount) + '=model'
        self._modelList.append('model' + str(self._modelCount))
        self._modelCount += 1
        exec(cmd)
        
        
    def __len__(self):
        return self._modelCount
        
    def __str__(self):
        if self._getMethod == 'local':
            return self._filename.split('.')[0] + ':' + str(self._modelCount) + 'model'
        elif self._getMethod == 'online':
            return self._filename + ':' + str(self._modelCount) + 'model'
            
    def nextModel(self):
        if self._currentModelNumber < self._modelCount:
            self._currentModelNumber += 1
            exec('tempModel = self.model' + str(self._currentModelNumber - 1))
            return tempModel
        else:
            self._currentModelNumber = 0            
            return 0
            
    def getModel(self, modelIndex = 0):
        if modelIndex >= self._modelCount:
            raise ValueError('model index out of range')
        cmd = 'tempModel = self.model' + str(modelIndex)
        exec(cmd)
        
        return tempModel
        
    def deleteByIndexes(self, indexes, models = 'all'):
        if models == 'all':
            models = range(self._modelCount)
            
        for model in models:
            cmd = 'self.model' + str(model) + '.deleteByIndexes(indexes)'
            exec(cmd)
            
    def removeModels(self, modelIndexes):
        for model in modelIndexes:
            modelName = 'model' + str(model)
            delattr(self, modelName)
            self._modelList.remove(modelName)
            self._modelCount -= 1
            
    def toCA(self):
        for modelName in self._modelList:
            model = 'self.' + modelName
            exec(model + '=' + model + '.toCA()')
            
        return self
            
    def isCA(self):
        tempNumber = self._currentModelNumber
        tempModel = self.nextModel()
        while tempModel:
            if not tempModel.isCA():
                self._currentModelNumber = tempNumber
                return False
            tempModel = self.nextModel()
        self._currentModelNumber = tempNumber
        return True
        
    def writePDB(self, outname = 'outfile.pdb'):
        '''
        write structure back to pdb format
        
        outname: output filename
        '''
        outfile = open(outname,'w')
        
        if self._modelCount == 1:
            model = self.model0
            for i in range(model.length):
               outfile.write('%-6s%5d  %-4s%3s %1s%4d    %8.3f%8.3f%8.3f%6.2f%6.2f           %-4s\n' \
                             %(model.line_type[i], model.atom_number[i], model.atom_name[i], model.residue_name[i],\
                             model.chain_id[i], model.residue_number[i], model.cor[i,0], model.cor[i,1], model.cor[i,2],\
                             model.occupancy[i], model.b_factor[i], model.element[i]))
        else:
            for index, modelName in enumerate(self._modelList):
                model = 'self.' + modelName
                exec('model = ' + model)
                outfile.write('MODEL     ' + str(index+1) + '\n')
                for i in range(model.length):
                    outfile.write('%-6s%5d  %-4s%3s %1s%4d    %8.3f%8.3f%8.3f%6.2f%6.2f           %-4s\n' \
                             %(model.line_type[i], model.atom_number[i], model.atom_name[i], model.residue_name[i],\
                             model.chain_id[i], model.residue_number[i], model.cor[i,0], model.cor[i,1], model.cor[i,2],\
                             model.occupancy[i], model.b_factor[i], model.element[i]))
                outfile.write('ENDMDL\n')
       
        outfile.close()
        
class pdbModel:
    def __init__(self, fragment):
        self.line_type = list()
        self.atom_number = list()
        self.atom_name = list()
        self.residue_name = list()
        self.chain_id = list()
        self.residue_number = list()
        self.cor = list()
        self.occupancy = list()       
        self.b_factor = list()
        self.element = list()
        
        if fragment != 'empty':
            for line in fragment:
                self.line_type.append(line[0:6].strip())                
                self.atom_number.append(int(line[7:11].strip()))
                self.atom_name.append(line[12:16].strip())
                self.residue_name.append(line[17:21].strip())
                self.chain_id.append(line[21])
                self.residue_number.append(int(line[22:26].strip()))
                cor = list()
                cor.append(float(line[30:38].strip()))
                cor.append(float(line[38:46].strip()))
                cor.append(float(line[46:54].strip()))
                self.cor.append(cor)
                self.occupancy.append(float(line[54:60].strip()))
                self.b_factor.append(float(line[60:66].strip()))
                self.element.append(line[77:80].strip())
                
            self.length = len(self.atom_number)
            self.cor = np.array(self.cor)
            
    def toCA(self):
        if self.isCA():
            return self
        
        tempModel = pdbModel('empty')        
        
        caIndex = list()
        
        for i in range(self.length):
            if self.atom_name[i] == 'CA':
                caIndex.append(i)
                
        caIndex.reverse()
        while caIndex:
            temp = caIndex.pop()
            tempModel.line_type.append(self.line_type[temp])            
            tempModel.atom_number.append(self.atom_number[temp])
            tempModel.atom_name.append(self.atom_name[temp])
            tempModel.residue_name.append(self.residue_name[temp])
            tempModel.chain_id.append(self.chain_id[temp])
            tempModel.residue_number.append(self.residue_number[temp])
            tempModel.occupancy.append(self.occupancy[temp])
            tempModel.b_factor.append(self.b_factor[temp])
            tempModel.element.append(self.element[temp])
            tempModel.cor.append(self.cor[temp,:].tolist())
        tempModel.cor = np.array(tempModel.cor)
        tempModel.length = len(tempModel.atom_number)
        
        return tempModel
        
    def isCA(self):
        for atomName in self.atom_name:
            if atomName != 'CA':
                return False
                
        return True
        
    def deleteByIndex(self, index):
        if not (isinstance(index, int) and index >= 0):
            raise ValueError('index needs to be a positive integer')
            
        del self.line_type[index]
        del self.atom_number[index]
        del self.atom_name[index]
        del self.residue_name[index]
        del self.chain_id[index]
        del self.residue_number[index]
        del self.occupancy[index]
        del self.b_factor[index]
        del self.element[index]
        self.cor = np.delete(self.cor, index, 0)
        
        self.length -= 1
        
    def deleteByIndexes(self, index = -1):
        if index == -1:
            return
        else:
            index.sort(reverse = True)
            for item in index:
                self.deleteByIndex(index = item)
                
        
    def __len__(self):
        return self.length
        
    def __eq__(self, other):
        try:        
            if self.cor is not None and np.array_equal(self.cor, other.cor):
                return True
        except:
            return False
            
        
    def fasta(self):
        transD = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
                  'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
                  'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
                  'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
        seq = {}
        tempModel = self.toCA()
        tempSeq = ''
        chainIndex = 0        
        uniqChainIDs = list()
     
        for i in range(tempModel.length):
            if tempModel.chain_id[i] not in uniqChainIDs:
                uniqChainIDs.append(tempModel.chain_id[i])
                if tempSeq:
                    seq[uniqChainIDs[chainIndex]] = tempSeq
                    tempSeq = ''
                    chainIndex += 1
            try:
                tempSeq += transD[tempModel.residue_name[i].upper()]
            except KeyError:
                tempSeq += '*'
        seq[uniqChainIDs[-1]] = tempSeq        
        return seq
                
            
            
            
            
        
'''       
if __name__ == '__main__':
    import sys
    parserTest = pdbParser(sys.argv[1])
'''       