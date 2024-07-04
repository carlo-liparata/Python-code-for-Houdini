

import os
import subprocess
from PySide2 import QtGui,QtCore,QtWidgets
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPalette
from PySide2.QtWidgets import *

selectedFile = QtWidgets.QFileDialog.getOpenFileName(None, "Select a usd file", "", "USD Files(*.usd *.usda *.usdc *.usdz)")

if selectedFile[0] != "":

    filePath = selectedFile[0].replace("/", "\\")
    hythonEXE = ""
    usdview = ""
    
    if("19.5" in hou.applicationVersionString()):
        hythonEXE = r"C:\Program Files\Side Effects Software\Houdini 19.5.303\bin\hython3.9.exe"
        usdview = r"C:\Program Files\Side Effects Software\Houdini 19.5.303\bin\usdview"
        #CREATE_NO_WINDOW = 0x08000000
        #subprocess.Popen([hythonEXE, usdview, filePath], creationflags=CREATE_NO_WINDOW)
    
    elif("20.0" in hou.applicationVersionString()):
        hythonEXE = r"C:\Program Files\Side Effects Software\Houdini 20.0.547\bin\hython3.9.exe"
        usdview = r"C:\Program Files\Side Effects Software\Houdini 20.0.547\bin\usdview"
    
    subprocess.Popen([hythonEXE, usdview, filePath])

else:
    print("Please select a .usd or .usda file")
