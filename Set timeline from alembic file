import hou

root = hou.selectedNodes()[0]

fRange = __import__("_alembic_hom_extensions").alembicTimeRange(root.hdaModule().GetFileName(root))
myFps = hou.fps()
startFrame = fRange[0]*myFps
endFrame = fRange[1]*myFps

def frameRateCheck():
    checkStartFrame = startFrame%10
    checkStartFrame = str(checkStartFrame)
    if checkStartFrame[-1] == "0":
        hou.ui.displayMessage("Framerate is PROBABLY correct", title="Framerate is PROBABLY correct")
    else:
        hou.ui.displayMessage("Framerate is PROBABLY incorrect", title="Framerate is PROBABLY incorrect")


def setPlaybar(a,b):
    hou.playbar.setFrameRange(a, b)
    hou.playbar.setPlaybackRange(a, b)
    hou.setFrame(a)

frameRateCheck()
    
myUiText = "Current framerate is {framerate} fps, if you want to change it please click cancel".format(framerate = myFps)     
myConfirm = hou.ui.displayConfirmation(myUiText, title = "Confirm Fps")

if myConfirm == False:
    framerateUserInput = hou.ui.readInput("Insert Framerate", title = "Change Fps")
    myFramerate = int(framerateUserInput[1])
    
    if framerateUserInput[0] == 0:    
        myFps = hou.setFps(myFramerate) 
        hou.ui.displayMessage("Framerate changed. Redo the command to edit the playbar")
 
        
if myConfirm == True:
    setPlaybar(startFrame, endFrame)
