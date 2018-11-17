from maya.app import renderSetup
import maya.app.renderSetup.model.selector as selector
import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.override as override
#import mtoa.core as core
import string
import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds
renderSetup.model.renderSetup.initialize()
rs = renderSetup.model.renderSetup.instance()

standardAIIter = cmds.ls(type = 'aiStandardSurface')
mainCollList = []
standardSurfaceList = []
#from see import see

 ###To make opacity shader### 
 #1. Create an “aiStandardSurface”
 #2. Set Base.weight to 0 and Specular.weight to 0
 #3. Increase emission weight to 1
 #4. Plug the "outColor" of the master ambient occlusion shader into the “Emission Color” of the newly created shader
 #5. Take the opacity map from the original object’s shader, and plug it into the new shader’s opacity
 
 #We also need to make a standardSurface shader for each shader
 # ---------------->
 
 
winID = "CreateRenderLayers"
if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)

myWindow = cmds.window(winID, title = "CreateRenderLayers", menuBar = True, nde = True, s = True, wh =( 50, 100))
cmds.rowColumnLayout(nc = 1)
 
makeOpacityBtn = cmds.button( label='Create Ambient/Opacity Render Layer', w = 250, h = 30, backgroundColor = [0.588, 0.972, 0.815], command= "makeOpacityLayer()" )

#cmds.setParent( '..' )
cmds.rowColumnLayout(nc = 2)

makeLayersFromSelectedObjectsBtn = cmds.button( label='Create PV Layer From Selected Objects', w = 250, h = 30, backgroundColor = [0.670, 0.384, 0.956], command= "makeLayerFromSelectedObject()" )
makeLayersFromSelectedGroupsBtn = cmds.button( label='Create PV Layer From Selected Groups', w = 250, h = 30, backgroundColor = [0.670, 0.584, 0.956], command= "makeLayerFromSelectedGRP()" )

makeMatteLayersFromSelectedObjectsBtn = cmds.button( label='Create Matte Layer From Selected Objects', w = 250, h = 30, backgroundColor = [0.443, 0.384, 0.956], command= "makeMatteLayerFromSelectedObject()" )
makeMatteLayersFromSelectedGroupsBtn = cmds.button( label='Create Matte Layer From Selected Groups', w = 250, h = 30, backgroundColor = [0.443, 0.584, 0.956],command= "makeMatteLayerFromSelectedGRP()" )

makeVisibilityLayerBtn = cmds.button( label='Make Visibilty Layer From Selected Objects', w = 250, h = 30, backgroundColor = [0.384, 0.662, 0.956],command= "setVisibilityInSceneObject()" )
makeVisibilityLayerGRPBtn = cmds.button( label='Make Visibilty Layer From Selected Groups', w = 250, h = 30, backgroundColor = [0.384, 0.862, 0.956],command= "setVisibilityInSceneGRP()" )

cmds.setParent( '..' )
closeBtn = cmds.button( label='Close', w = 150, h = 30, backgroundColor = [0.909, 0.007, 0.286],command= "quitBtn()" )

cmds.setParent( '..' )
cmds.showWindow( myWindow )


def quitBtn():
    cmds.deleteUI(myWindow)

 
def makeOpacityLayer():  
    global opacToCollList
    global allOtherList
    global aiAmbient
    global standardSurface
    
    
    opacToCollList = []
    allOtherList = []
    tempCount = 0

    for shader in standardAIIter:
        try:
            #get the list of connections to the current aiStandardSurface shader      
            shaderCon = cmds.listConnections(shader)
            tempCon = " ".join(shaderCon)
            if "opacity" in tempCon.lower():
                print "Opacity located in " + shader
                opacToCollList.append(shader)
                tempCount+=1
            else:
                allOtherList.append(shader)
            
        except:
            pass
    opacToCollList = list(set(opacToCollList))
    print opacToCollList



    aiAmbient = cmds.shadingNode("aiAmbientOcclusion",asShader=True)
    standardSurface = cmds.shadingNode("aiStandardSurface", asShader=True) 
    rsLayer = rs.createRenderLayer('RenderLayers') 
     
    
    cmds.setAttr(standardSurface + ".base", 0)
    cmds.setAttr(standardSurface + ".specular", 0)
    cmds.setAttr(standardSurface + ".emission", 1)
    
    for i in range(tempCount):
        standardSurfaceList.append(cmds.duplicate(standardSurface))
    
    setPatternListAndAddNewCollections(rsLayer)
    connectFileToOpacity()
    lightingOverride(rsLayer)
    cmds.delete(standardSurface)
    cmds.button(makeOpacityBtn, e = True, enable = False)


def setPatternListAndAddNewCollections(rsLayer):
    ambientOcculsionColl = rsLayer.createCollection("Ambient Occusion")

    totalItems = []
    
    try:
        for shader in allOtherList:
            cmds.hyperShade(objects = shader)
            objectList = cmds.ls(selection = True)
            totalItems += objectList
            
        myList = ';'.join(totalItems)
        ambientOcculsionColl.getSelector().setPattern("*")
        over_objAmbient = ambientOcculsionColl.createOverride('AmbientLayer', OpenMaya.MTypeId(0x58000386)) 
        over_objAmbient.setShader(aiAmbient)

    except:
        pass
    try:
        rsColl = rsLayer.createCollection('OpacityCollections')
        l2 = []
        index = 0
        for shader in opacToCollList:
            cmds.hyperShade(objects = shader)
            objectList = cmds.ls(selection = True, geometry = True, dagObjects = True, planes = True)
            objectList2 = cmds.listRelatives(objectList ,type='transform' ,p=True)
            
            print objectList
            print objectList2
            myString = ','.join(objectList)
            #myList = remove_all("Shape", myString)
            myList = myString.split(",")
            print myList

            
            #for i in myList:
                
                
            newColl = rsColl.createCollection(str(shader))
            newColl.getSelector().staticSelection.set(myList[:])
            newColl.getSelector().setFilterType(2)
            over_obj = newColl.createOverride('OpacityLayer', OpenMaya.MTypeId(0x58000386)) 

            mainCollList.append(myList)
            l2.append(myList)
            myShader = standardSurfaceList[index]
            print myShader
            over_obj.setShader(myShader[0])
            index+=1
        rsColl.getSelector().setPattern("*")

    except Exception as e:
        print e
    


def remove_all(substr, str):
    index = 0
    length = len(substr)
    while string.find(str, substr) != -1:
        index = string.find(str, substr)
        str = str[0:index] + str[index+length:]
    return str
    
def remove_all_In_List(substr, myList):
    index = 0
    length = len(substr)
    for i in myList:
        index = string.find(i, substr)
        i = str[0:index] + str[index+length:]
    return str

def connectFileToOpacity():
    allFileNodes = cmds.ls(et="file")
    try:
        for currentFile in allFileNodes:
            index = 0
            if "opacity" in currentFile.lower():
                myShader = standardSurfaceList[index] 
                cmds.connectAttr(currentFile + ".outColor", myShader[0] + ".opacity")
                cmds.connectAttr(aiAmbient + ".outColor", myShader[0] + ".emissionColor")  
                index+=1 
    except:
        pass                 
        
        
def lightingOverride(rsLayer):
    try:
        lightColl = rsLayer.createCollection('Lighting') 
        allLights = cmds.ls(type = cmds.listNodeTypes("light"))
        myList = '*;*'.join(allLights)
        lightColl.getSelector().setPattern("*")
        lightingOverride = lightColl.createOverride("LightingOverride", OpenMaya.MTypeId(0x58000378))
        lightColl.getSelector().setFilterType(4)
          
        plug = '%s.intensity' % allLights[0]
        lightingOverride.setAttributeName(plug)
        lightingOverride.finalize(plug)
        lightingOverride.setAttrValue(0)
        print allLights[0]
    except:
        pass
    
    
    
    
def makeLayerFromSelectedGRP():
    selected = cmds.ls(sl = True)
    selectedTransforms = cmds.listRelatives(selected, allDescendents = True, type = "transform")
    selectedShapes = cmds.listRelatives(selected, allDescendents = True, type = "shape")
    makeLayer = rs.createRenderLayer(selected[0] + ' PV Layers')
     
    makeCollection = makeLayer.createCollection(selected[0] + 'PV Collection') 
    makeCollection.getSelector().setPattern("*")
    makeCollection.getSelector().setFilterType(2)
    visibilityCollectionOverride = makeCollection.createOverride(selected[0] + "Override", OpenMaya.MTypeId(0x58000378))

    
    visibilityCollection = makeLayer.createCollection(selected[0] + ' PV Collection') 
    visibilityCollection.getSelector().staticSelection.set(selectedShapes)
    visibilityCollection.getSelector().setFilterType(2)
    visibilityCollectionOverride2 = visibilityCollection.createOverride(selected[0] + " PV Override", OpenMaya.MTypeId(0x58000378))
    
    plug = '%s.primaryVisibility' % selectedShapes[0]
    
    visibilityCollectionOverride.setAttributeName(plug)
    visibilityCollectionOverride.finalize(plug)
    visibilityCollectionOverride.setAttrValue(0)
    
    visibilityCollectionOverride2.setAttributeName(plug)
    visibilityCollectionOverride2.finalize(plug)
    visibilityCollectionOverride2.setAttrValue(1)
    


def makeLayerFromSelectedObject():
    selected = cmds.ls(sl = True, type = "transform")
    selectedShapes = cmds.listRelatives(selected, allDescendents = True, type = "shape")
    makeLayer = rs.createRenderLayer(' PV Layers') 
    
    makeCollection = makeLayer.createCollection(' PV Collection') 
    makeCollection.getSelector().setPattern("*")
    makeCollection.getSelector().setFilterType(2)
    visibilityCollectionOverride = makeCollection.createOverride(" PV Override", OpenMaya.MTypeId(0x58000378))

    visibilityCollection = makeLayer.createCollection(' PV Collection') 
    visibilityCollection.getSelector().staticSelection.set(selectedShapes)
    visibilityCollection.getSelector().setFilterType(2)
    visibilityCollectionOverride2 = visibilityCollection.createOverride(" PV Override", OpenMaya.MTypeId(0x58000378))
    
    plug = '%s.primaryVisibility' % selectedShapes[0]
    
    visibilityCollectionOverride.setAttributeName(plug)
    visibilityCollectionOverride.finalize(plug)
    visibilityCollectionOverride.setAttrValue(0)
    
    visibilityCollectionOverride2.setAttributeName(plug)
    visibilityCollectionOverride2.finalize(plug)
    visibilityCollectionOverride2.setAttrValue(1)
    
    
def makeMatteLayerFromSelectedGRP():
    selected = cmds.ls(sl = True)
    selectedTransforms = cmds.listRelatives(selected, allDescendents = True, type = "transform")
    selectedShapes = cmds.listRelatives(selected, allDescendents = True, type = "shape")
    makeLayer = rs.createRenderLayer(selected[0] + ' Matte Layers')
     
    makeCollection = makeLayer.createCollection(selected[0] + 'Matte Collection ON') 
    makeCollection.getSelector().setPattern("*")
    makeCollection.getSelector().setFilterType(2)
    matteCollectionOverride = makeCollection.createOverride(selected[0] + " Matte Override", OpenMaya.MTypeId(0x58000378))

    
    matteCollection = makeLayer.createCollection(selected[0] + ' Matte Collection OFF') 
    matteCollection.getSelector().staticSelection.set(selectedShapes)
    matteCollection.getSelector().setFilterType(2)
    matteCollectionOverride2 = matteCollection.createOverride(selected[0] + " Matte Override", OpenMaya.MTypeId(0x58000378))
    
    plug = '%s.aiMatte' % selectedShapes[0]
    
    matteCollectionOverride.setAttributeName(plug)
    matteCollectionOverride.finalize(plug)
    matteCollectionOverride.setAttrValue(1)
    
    matteCollectionOverride2.setAttributeName(plug)
    matteCollectionOverride2.finalize(plug)
    matteCollectionOverride2.setAttrValue(0)
    


def makeMatteLayerFromSelectedObject():
    selected = cmds.ls(sl = True, type = "transform")
    selectedShapes = cmds.listRelatives(selected, allDescendents = True, type = "shape")
    makeLayer = rs.createRenderLayer(' Matte Layers') 
    
    makeCollection = makeLayer.createCollection(' Matte Collection ON') 
    makeCollection.getSelector().setPattern("*")
    makeCollection.getSelector().setFilterType(2)
    matteCollectionOverride = makeCollection.createOverride(" Matte Override", OpenMaya.MTypeId(0x58000378))

    matteCollection = makeLayer.createCollection(' Matte Collection OFF') 
    matteCollection.getSelector().staticSelection.set(selectedShapes)
    matteCollection.getSelector().setFilterType(2)
    matteCollectionOverride2 = matteCollection.createOverride(" Matte Override", OpenMaya.MTypeId(0x58000378))
    
    plug = '%s.aiMatte' % selectedShapes[0]
    
    matteCollectionOverride.setAttributeName(plug)
    matteCollectionOverride.finalize(plug)
    matteCollectionOverride.setAttrValue(1)
    
    matteCollectionOverride2.setAttributeName(plug)
    matteCollectionOverride2.finalize(plug)
    matteCollectionOverride2.setAttrValue(0)

    
def setVisibilityInSceneGRP():
    #create a collection for all the scene and create a collection for things we don't want visible
    #This works for groups
    #For visibility of objects/groups to be set invisible by default, must do in specific order
    selected = cmds.ls(sl = True)  
    selectedTransforms = cmds.listRelatives(selected, allDescendents = True, type = "transform")
    makeLayer = rs.createRenderLayer('VisibilityLayers')
    
    visibleCollection = makeLayer.createCollection('VisibleCollection') 
    visibleCollection.getSelector().setPattern("*")
    visibileCollectionOverride = visibleCollection.createOverride("VisibleOverride", OpenMaya.MTypeId(0x58000378))

    invisibleCollection = makeLayer.createCollection('InvisibleCollection') 
    invisibleCollection.getSelector().staticSelection.set(selectedTransforms)
    invisibileCollectionOverride = invisibleCollection.createOverride("InvisibleOverride", OpenMaya.MTypeId(0x58000378))
 
    plug = '%s.visibility' % selectedTransforms[0]
    
    visibileCollectionOverride.setAttributeName(plug)
    visibileCollectionOverride.finalize(plug)
    visibileCollectionOverride.setAttrValue(1)
    
    invisibileCollectionOverride.setAttributeName(plug)
    invisibileCollectionOverride.finalize(plug)
    invisibileCollectionOverride.setAttrValue(0)
    
def setVisibilityInSceneObject():
    #create a collection for all the scene and create a collection for things we don't want visible
    selected = cmds.ls(sl = True, type = "transform")  
    makeLayer = rs.createRenderLayer('VisibilityLayers')
    
    visibleCollection = makeLayer.createCollection('VisibleCollection') 
    visibleCollection.getSelector().setPattern("*")
    visibileCollectionOverride = visibleCollection.createOverride("VisibleOverride", OpenMaya.MTypeId(0x58000378))

    invisibleCollection = makeLayer.createCollection('InvisibleCollection') 
    invisibleCollection.getSelector().staticSelection.set(selected)
    invisibileCollectionOverride = invisibleCollection.createOverride("InvisibleOverride", OpenMaya.MTypeId(0x58000378))
 
    plug = '%s.visibility' % selected[0]

    visibileCollectionOverride.setAttributeName(plug)
    visibileCollectionOverride.finalize(plug)
    visibileCollectionOverride.setAttrValue(1)
    
    invisibileCollectionOverride.setAttributeName(plug)
    invisibileCollectionOverride.finalize(plug)
    invisibileCollectionOverride.setAttrValue(0)
    

        
    
    
    
    
        
