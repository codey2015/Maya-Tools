import maya.app.renderSetup.model.override as override
import maya.app.renderSetup.model.selector as selector
import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup
import maya.cmds as cmds
import json
import os


path = cmds.fileDialog2(dialogStyle=2,  fileFilter = "directory", fileMode = 3)
print path[0]
os.chdir( path[0] )

def importFile(filename):
    with open(filename, "r+") as file:
        renderSetup.instance().decode(json.load(file), renderSetup.DECODE_AND_OVERWRITE, None)

def exportFile(filename):
    with open(filename, "w+") as file:
        json.dump(renderSetup.instance().encode(None), fp=file, indent=2, sort_keys=True)


rs = renderSetup.instance()    
allLayers  = rs.getRenderLayers()

sceneName = cmds.file(q = True, sn = True)
cmds.file((path[0] + "/" + str(0)), type='mayaAscii',de = True, ea = True, f = True)

exportFile('originalRenderLayers.json')
importFile('originalRenderLayers.json')

tempLayer = []
tempLayer = allLayers[1]

print "--------------------------------------------------------------------------"
tempCount = 1
for layer in range(len(allLayers)): 
    print "Layer number: " + str(tempCount)
    if(layer == 0):
        
        for l in allLayers:
            print l.name() + " allLayers"
        print "\n"
        
        curLay = allLayers[layer].name()
        keepFirst = 0
        print curLay + " is the layer we should keep\n"
        for i in allLayers:
            if(keepFirst > 0):
                print " Deleting " + i.name()
                cmds.delete(i.name())
            else:
                print "Keeping " + i.name()
            keepFirst+=1
        print "Saving....."
        testNewLayers = rs.getRenderLayers()
        print "\n"
        for l in testNewLayers:
            print l.name() + " is remaning!"
        print "\n"
        
        cmds.file((path[0] + "/" + allLayers[layer].name()), type='mayaAscii',de = True, ea = True, f = True)
        importFile('originalRenderLayers.json')  
   
    if(layer > 0):
        testNewLayers = rs.getRenderLayers()
        curLay = allLayers[layer].name()
        #cmds.setAttr("rs_"+ curLay +".displayOrder", 0)
      

        for l in allLayers:
            print l.name() + " allLayers"
        print "\n"

        print curLay + " is the layer we should keep\n"
        rs.attachRenderLayer(0, testNewLayers[layer])
        
        for x in testNewLayers:
           if(x.name() not in curLay):
                print " Deleting " + x.name()
                cmds.delete(x.name())
           else:
                print "Keeping " + x.name()
                
        testNewLayers = rs.getRenderLayers()        
        print "\n"        
        for l in testNewLayers:
            print l.name() + " is remaning!"
        print "\n"
        
        print "Saving....."
        cmds.file((path[0] + "/" + allLayers[layer].name()), type='mayaAscii',de = True, ea = True, f = True)
        importFile('originalRenderLayers.json')
    print "**************************************"
    importFile('originalRenderLayers.json')
    tempCount+=1
print "--------------------------------------------------------------------------"
