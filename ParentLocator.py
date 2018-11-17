import pymel.core as pm

winID = "ParentLocator"
if pm.window(winID, exists=True):
    pm.deleteUI(winID)

myWindow = pm.window(winID, title = "ParentLocator", menuBar = True, nde = True, s = True, wh =( 50, 100))
pm.rowColumnLayout(nc = 1)
startPosBtn = pm.button( label='Select Child', w = 150, h = 30, command = "getObjectA()" )
endPosBtn = pm.button( label='Select Parent', w = 150, h = 30, command = "getObjectB()" )
makeBtn = pm.button( label='Create Constraint', w = 150, h = 30, command = "createConstraint()" )
closeBtn = pm.button( label='Close', w = 150, h = 30,command= "quitBtn()" )

pm.setParent( '..' )
pm.showWindow( myWindow )


def quitBtn():
    pm.deleteUI(myWindow)


def getObjectA():
    global objectA
    objectA = pm.ls(sl = True)


    
def getObjectB():
    global objectB
    objectB = pm.ls(sl = True)
    
        
def createConstraint():
    mid = pm.spaceLocator(name = objectA[0] + "_Mover")
    midGRP = pm.group(mid, name = objectA[0] + "_Mover_GRP")
    objAGRP = pm.group(objectA, name = objectA[0] + "_GRP")
    #put locator to object A
    pm.parentConstraint(objAGRP, midGRP)
    pm.parentConstraint(objAGRP, midGRP, e = True, rm = True)
    
    midToA = pm.parentConstraint(mid, objAGRP, maintainOffset = True)
    BToMid = pm.parentConstraint(objectB, midGRP, maintainOffset = True) 
    print midToA
    print BToMid
    constraintSlider = pm.addAttr(objectA, longName = objectA[0] + "TO" + objectB[0], at = "float", min = 0, max = 1, k = True)
    pm.connectAttr(objectA[0] + "." + objectA[0] + "TO" + objectB[0], BToMid+ ".w0")
    pm.setAttr(objectA[0] + "." + objectA[0] + "TO" + objectB[0], 1)
    pm.select(mid)
    
