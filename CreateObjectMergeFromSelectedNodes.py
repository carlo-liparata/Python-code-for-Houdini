import hou

for i in hou.selectedNodes():
    parent = i.parent()
    
    ogPos = i.position()
    offset = hou.Vector2(2, -2)
    finalPos = hou.Vector2(ogPos[0]+offset[0], ogPos[1]+offset[1])
    
    currentNodePath = "/obj/"+str(parent)+"/"+str(i)
    geo = hou.node("/obj/"+str(parent))
    
    i.setSelected(False,clear_all_selected=False)
    
    objMerge = geo.createNode("object_merge")    
    objMerge.move(finalPos)
    
    refObjParm = objMerge.parm("objpath1")
    refObjParm.set(currentNodePath)
    objMerge.setSelected(True, clear_all_selected=False)
    #print(currentNodePath)
