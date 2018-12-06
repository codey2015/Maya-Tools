import maya.cmds as cmds
import os 
import importlib
import imp
import sys

winIDWork = "Script Runner"
if cmds.window(winIDWork, exists=True):
    cmds.deleteUI(winIDWork)

myWorkWindow = cmds.window(winIDWork, title = "Script Runner", menuBar = True, nde = True, s = True, wh =( 50, 100))
cmds.rowColumnLayout(nc = 1)

cmds.button( label='Run Single Script', w = 250, h = 30, backgroundColor = [0.588, 0.972, 0.815], command= "runScript()" ) 
cmds.button( label='Select File', w = 250, h = 30, backgroundColor = [0.588, 0.972, 0.815], command= "selectFile()" ) 
cmds.button( label='Add Script to Selected File', w = 250, h = 30, backgroundColor = [0.588, 0.972, 0.815], command= "addScript()" ) 
cmds.button( label='Run Scripts Selected File (In order)', w = 250, h = 30, backgroundColor = [0.588, 0.972, 0.815], command= "runScriptsFromFile()" ) 

cmds.showWindow( myWorkWindow )

    
def runScript():
    myFile = cmds.fileDialog2(dialogStyle=2, fileFilter = "*.py")
    tempFile = myFile[0].split("/")
    
    changeDir = myFile[0]
    cnge = changeDir.replace(tempFile[-1], "")
    os.chdir( cnge )
    sys.path.insert(0, os.getcwd())
    
    importName = tempFile[-1].split(".")
    myImport = importlib.import_module(importName[0])
    reload(myImport)
    
def selectFile():
    global selectedTextFile
    selectedTextFile = cmds.fileDialog2(dialogStyle=2, fileFilter = "*.txt")
    
def addScript():
    myFile = cmds.fileDialog2(dialogStyle=2, fileFilter = "*.py")
    s = str(selectedTextFile[0])
    with open(s, "a+") as f:
        f.write(myFile[0])
        f.write("\r\n")
    f.close()
    
    
def runScriptsFromFile():
    try:
        myFile = cmds.fileDialog2(dialogStyle=2, fileFilter = "*.txt")
        moduleList = []
        s = str(myFile[0])
        with open(s, "r") as f:
            content = f.readlines()
        for i in content:
            i.strip("\r\n")
            moduleList.append(i)
            
        for i in moduleList:
            tempFile = i.split("/")
            a = i[:-5]
            importName = tempFile[-1].split(".")
                
            for x in reversed(a):  
                if(x == "/"):
                    break
                if(x != "/"):      
                    a = a[:-1]     
                    
            sys.path.insert(0, a)
            os.chdir(a)
            if(importName[0] != myFile[0].split("/")[-1].split(".")[0]):
                myImport = importlib.import_module(importName[0])
                print "Imported: " + importName[0]
                reload(myImport)
    except Exception as e:
        print e
        