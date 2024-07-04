
import hou
import _alembic_hom_extensions as abc
from PySide2 import QtGui,QtCore,QtWidgets
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPalette, QBrush, QColor
from PySide2.QtWidgets import *
import os


class autoRestUI(QtWidgets.QMainWindow):
    

    def __init__(self, parent=None):     
        
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setFixedSize(500, 300)
        self.setWindowTitle("Auto Rest Abc")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
           
        self.sourceAbcPath = ""
        self.selNodes = hou.selectedNodes()
        self.tempAutoRestAbc = None
        
        self.AutoRestAbc()
        
        self.chooseMode = QCheckBox("Pick External Alembic File", self)
        self.chooseMode.move(10, 10)
        self.chooseMode.resize(500, 30)        
        self.chooseMode.setStyleSheet("font-size: 14pt")        
        self.chooseMode.stateChanged.connect(self.updateMode)        
        
        self.frameLabel = QLabel("Frame:", self)
        self.frameLabel.resize(100,40)
        self.frameLabel.move(10,80)
        self.frameLabel.setEnabled(True)
        self.frameLabel.setStyleSheet("font-size: 14pt")
        
        self.stepLabel = QLabel("Step:", self)
        self.stepLabel.resize(100,40)
        self.stepLabel.move(10,120)
        self.stepLabel.setEnabled(True)
        self.stepLabel.setStyleSheet("font-size: 14pt")
        
        self.frameChooser = QSpinBox(self)
        self.frameChooser.resize(200, 40)
        self.frameChooser.move(80, 80)
        self.frameChooser.setRange(-10000, 99999)
        self.frameChooser.setValue(1001)
        self.frameChooser.setStyleSheet("font-size: 14pt")
        self.frameChooser.setEnabled(True)
        self.frameChooser.valueChanged.connect(self.updateFrameValue)
        
        self.stepChooser = QDoubleSpinBox(self)
        self.stepChooser.resize(200, 40)
        self.stepChooser.move(80, 120)
        self.stepChooser.setRange(0.1, 1)
        self.stepChooser.setValue(1.0)
        self.stepChooser.setStyleSheet("font-size: 14pt")
        self.stepChooser.setEnabled(True)
        self.stepChooser.valueChanged.connect(self.updateStepValue)
        
        self.pickAbcFile = QPushButton("Pick An Alembic File", self)
        self.pickAbcFile.move(10, 200)
        self.pickAbcFile.resize(250, 40)
        self.pickAbcFile.setStyleSheet("font-size: 14pt")
        self.pickAbcFile.setEnabled(False)
        self.pickAbcFile.clicked.connect(self.openAbcPicker)
        
        self.saveButton = QPushButton("Save Alembic", self)
        self.saveButton.move(280, 200)
        self.saveButton.resize(200, 40)
        self.saveButton.setStyleSheet("font-size: 14pt")
        self.saveButton.clicked.connect(self.saveRestAbc)
        
    
    def saveRestAbc(self):

        saveToDiskButton = self.tempAutoRestAbc.parm("save_output_abc")
        saveToDiskButton.pressButton()
        self.tempAutoRestAbc.destroy()
        if self.selNodes[0].type().name() == "alembicarchive":
            self.selNodes[0].parm("reloadGeometry").pressButton()
            self.selNodes[0].parm("buildHierarchy").pressButton()
        self.close()
       
            
    def openAbcPicker(self):
        abcFile= QtWidgets.QFileDialog.getOpenFileName(self, "Pick reference position Abc", filter=("Alembic File (*.abc)"))
        externalAbcPath = self.tempAutoRestAbc.parm("external_file")
        externalAbcPath.set(abcFile[0])
        print(abcFile[0])
    
        
    def updateMode(self):
        checked = self.chooseMode.isChecked()
        nodeCheckBox = self.tempAutoRestAbc.parm("use_external_file")
        nodeCheckBox.set(checked)
        
        if checked:
            self.frameChooser.setEnabled(False)
            self.frameLabel.setEnabled(False)
            self.pickAbcFile.setEnabled(True)
        else:
            self.frameChooser.setEnabled(True)
            self.frameLabel.setEnabled(True)
            self.pickAbcFile.setEnabled(False)
    
            
    def updateFrameValue(self):
        currentFrameValue = self.frameChooser.value()        
        self.tempAutoRestAbc.parm("sourceFrame").set(currentFrameValue)
        
    def updateStepValue(self):
        currentStepValue = self.stepChooser.value()
        #print(currentStepValue)
        self.tempAutoRestAbc.parm("output_frame_range3").set(currentStepValue)
        
    def getAlembicFrameRange(self, abcPath):
        myFps = hou.fps()
        time = abc.alembicTimeRange(abcPath)
        if time != None:
            firstFrame = time[0]*myFps
            lastFrame = time[1]*myFps
            return [firstFrame, lastFrame, 1]
        else:
            firstFrame = hou.playbar.frameRange()[0]
            return [firstFrame, firstFrame, 1]            
            print( "Alembic file has no time information, frame {} will be used".format(str(firstFrame)) )
            
        
    def restFilePath(self, srcPath):
        restPath = srcPath[:-4]+"_rest.abc"
        return restPath
    
        
    def createAutoRestNode(self, sourcefile):
        obj = hou.node("/obj")
                
        self.tempAutoRestAbc = obj.createNode("auto_rest_abc::1.0", "auto_abc_TEMP")
        self.tempAutoRestAbc.parm("og_filename").set(sourcefile, None, False)
        self.tempAutoRestAbc.parm("output_filepath").set(self.restFilePath(sourcefile), None, False)
        self.tempAutoRestAbc.parm("output_frame_range1").set(self.getAlembicFrameRange(sourcefile)[0], None, False)
        self.tempAutoRestAbc.parm("output_frame_range2").set(self.getAlembicFrameRange(sourcefile)[1], None, False)
        self.tempAutoRestAbc.parm("output_frame_range3").set(self.getAlembicFrameRange(sourcefile)[2], None, False)
        #hou.cd(self.tempAutoRestAbc.path())
    
        
    def AutoRestAbc(self):            
        
        if len(self.selNodes) == 1 and ( self.selNodes[0].type().name() == "arnold::alembic" or self.selNodes[0].type().name() == "alembicarchive" ):           
            
            if self.selNodes[0].type().name() == "arnold::alembic":            
                self.sourceAbcPath = self.selNodes[0].parm("ar_filename").eval()
                
                if len(self.sourceAbcPath) != 0:
                    if self.sourceAbcPath[-9:][:6] == "_rest.":
                        raise Exception("Alembic already has a rest attribute")
                        #print("Alembic already has a rest attribute")
                    
                    else:                                                
                        self.createAutoRestNode(self.sourceAbcPath)
                        self.selNodes[0].parm("ar_filename").set(self.restFilePath(self.sourceAbcPath))
                                
                        
            if self.selNodes[0].type().name() == "alembicarchive":   
                self.sourceAbcPath = self.selNodes[0].parm("fileName").eval()
                
                if len(self.sourceAbcPath) != 0:
                    if self.sourceAbcPath[-9:][:6] == "_rest.":
                        raise Exception("Alembic already has a rest attribute")
                        #print("Alembic already has a rest attribute")
                    
                    else:
                        self.createAutoRestNode(self.sourceAbcPath)                        
                        self.selNodes[0].parm("fileName").set(self.restFilePath(self.sourceAbcPath))
                                            
                        
        elif len(self.selNodes) > 1:
            raise Exception("select only 1 node")
            #print("select only 1 node")
    
            
        elif len(self.selNodes) < 1:
            raise Exception("Select a node")
            #print("Select a node")        
            
            
        elif self.selNodes[0].type().name() != "arnold::alembic" or self.selNodes[0].type().name() != "alembicarchive":       
            raise Exception("Select a valid node")
            #print("Select a valid node")    
            
            
    #self.sourceAbcPath = self.selNodes[0].parm("ar_filename").eval()
    #print(self.getAlembicFrameRange(self.sourceAbcPath))    


mainWin = autoRestUI()
mainWin.show()
