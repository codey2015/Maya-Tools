import maya.cmds as cmds


winID = "LightLinker"
if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)

myWindow = cmds.window(winID, title = "Light Linker", menuBar = True, nde = True, s = True, wh =( 50, 100))
cmds.rowColumnLayout(nc = 1)
 
getLightsBtn = cmds.button( label='Select light(s)', w = 250, h = 30, backgroundColor = [0.588, 0.972, 0.815], command= "selectLights()" )
getObjectsBtn = cmds.button( label='Select objects to include', w = 250, h = 30, backgroundColor = [0.7, 0.6, 0.815], command= "selectObjectsToExclude()" )
linkLightsBtn = cmds.button( label='Link lights', w = 250, h = 30, backgroundColor = [0.95, 1.0, 0.4], command= "linkLights()" )

closeBtn = cmds.button( label='Close', w = 150, h = 30, backgroundColor = [0.909, 0.007, 0.286],command= "quitBtn()" )

cmds.showWindow( myWindow )

def quitBtn():
    cmds.deleteUI(myWindow)

def selectLights():
    global selectedLights
    selectedLights = cmds.ls(selection = True) 
    cmds.select(cl = True)

def selectObjectsToExclude():
    global allDeselectedObjects
    global selectedObjects
    selectedObjects = cmds.ls(sl = True)
    cmds.select(all = True)
    cmds.select(selectedObjects, deselect = True)
    cmds.select(selectedLights, deselect = True)
    allDeselectedObjects = cmds.ls(sl = True)
    cmds.select(cl = True)
      
def linkLights():
    cmds.lightlink(b = True, light = selectedLights, object = allDeselectedObjects)
    cmds.lightlink(light = selectedLights, object = selectedObjects)

