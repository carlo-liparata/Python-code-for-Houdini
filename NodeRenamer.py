
import hou

from PySide2 import QtGui,QtCore,QtWidgets
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPalette
from PySide2.QtWidgets import *


## Save Old Name In Node's Comment ##  
def saveOldNameInComment():
        
    selectedNodes = hou.selectedNodes()
        
    for i in selectedNodes:
        nodeName = i.name()
        i.setComment(nodeName)
            
            

class myUi(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):     
        
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setMinimumSize(920, 270)
        self.setWindowTitle("Name Replacer")
        
        self.force_close = True 
        
        ## Replaced Label ##
        self.replacedLabel = QLabel("Write here the string that will be replaced:", self)
        self.replacedLabel.resize(300, 20)
        self.replacedLabel.move(20, 30)
        
        ## Replaced Input ##
        self.replacedStr = QLineEdit("", self)
        self.replacedStr.resize(400, 50)
        self.replacedStr.move(20, 50)
        
        ## Replacing Label ##
        self.replacingLabel = QLabel("Write here the replacing string:", self)
        self.replacingLabel.resize(300, 20)
        self.replacingLabel.move(20, 100)
        
        ## Replacing Input ##
        self.replacingStr = QLineEdit("", self)
        self.replacingStr.resize(400, 50)
        self.replacingStr.move(20, 120)
       
        ## Replace Button ##
        self.replaceButton = QPushButton("Replace", self)
        self.replaceButton.move(20, 170)
        self.replaceButton.clicked.connect(self.replaceNames)
        
        ## Suffix Label ##
        self.suffixLabel = QLabel("Write the suffix here:", self)
        self.suffixLabel.resize(300, 20)
        self.suffixLabel.move(500, 30)
        
        ## Suffix Input ##
        self.suffixStr = QLineEdit("", self)
        self.suffixStr.resize(400, 50)
        self.suffixStr.move(500, 50)
        
        ## Suffix Button ##
        self.suffixButton = QPushButton("Add Suffix", self)
        self.suffixButton.move(500, 170)
        self.suffixButton.clicked.connect(self.addSuffix)
        
        ## Prefix Label ##
        self.prefixLabel = QLabel("Write the prefix here:", self)
        self.prefixLabel.resize(300, 20)
        self.prefixLabel.move(500, 100)
        
        ## Prefix Input ##
        self.prefixStr = QLineEdit("", self)
        self.prefixStr.resize(400, 50)
        self.prefixStr.move(500, 120)
        
        ## Prefix Button ##
        self.prefixButton = QPushButton("Add Prefix", self)
        self.prefixButton.move(600, 170)
        self.prefixButton.clicked.connect(self.addPrefix)
        
        ## Undo Button ##
        self.undoButton = QPushButton("Undo", self)
        self.undoButton.move(800, 220)
        self.undoButton.clicked.connect(self.undo)
        
        gridLay = QGridLayout()
        gridLay.addWidget(self.replacedLabel, 0, 0)
        gridLay.addWidget(self.replacedStr, 1, 0)        
        gridLay.addWidget(self.replacingLabel, 3, 0)        
        gridLay.addWidget(self.replacingStr, 4, 0)
        gridLay.addWidget(self.replaceButton, 5, 0)
        gridLay.addWidget(self.suffixLabel, 0, 1)
        gridLay.addWidget(self.suffixStr, 1, 1)
        gridLay.addWidget(self.suffixButton, 2, 1)
        gridLay.addWidget(self.prefixLabel, 3, 1)        
        gridLay.addWidget(self.prefixStr, 4, 1)
        gridLay.addWidget(self.prefixButton, 5, 1)
        gridLay.addWidget(self.undoButton, 7, 1)
        
        
        widget = QWidget()
        widget.setLayout(gridLay)
        self.setCentralWidget(widget)
        
            
    ## Delete Comment When Closing Window ##    
    def closeEvent(self,event): 
        
        if self.force_close is True:
            selectedNodes = hou.selectedNodes()
        
            for i in selectedNodes:
                i.setComment("")
                                   
        
    ## Set Comment As Name ##    
    def undo(self):
       
        selectedNodes = hou.selectedNodes()
        
        for i in selectedNodes:
            nodeName = i.name()
            newName = i.comment()
            i.setName(newName)  
        
        
            
    def addSuffix(self):    
        
        saveOldNameInComment()
        selectedNodes = hou.selectedNodes()
        for i in selectedNodes:
            nodeName = i.name()
            newName = nodeName+self.suffixStr.text()
            i.setName(newName)
            
            
            
    def addPrefix(self):    
        
        saveOldNameInComment()
        selectedNodes = hou.selectedNodes()
        
        for i in selectedNodes:
            nodeName = i.name()
            newName = self.prefixStr.text()+nodeName
            i.setName(newName)            
            
               
            
    def replaceNames(self):
        
        saveOldNameInComment()
        
        selectedNodes = hou.selectedNodes()
        stringMatch = self.replacedStr.text()
        stringReplace = self.replacingStr.text()

        
        for i in selectedNodes:
            nodeName = i.name()
            newName = nodeName.replace(stringMatch, stringReplace)
            i.setName(newName)
  
            
            

mainWin = myUi()
mainWin.show()
      
