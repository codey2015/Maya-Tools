import maya.cmds as cmds

mywinID = "Loading Progress"
if cmds.window(mywinID, exists=True):
    cmds.deleteUI(mywinID)
    
myWindow = cmds.window(title = "Loading Progress")
cmds.columnLayout()
progressControl2 = cmds.progressBar(maxValue=10, width=300, visible = False)
progressControl = cmds.progressBar(maxValue=10, width=300)

shaders = cmds.ls(type = 'aiStandardSurface')
shaders.sort()

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
    
def hasEndNumber(inputString):
    return inputString[-1].isdigit()
       
def checkNumbers(inputString):
    if(":" in inputString):
        tempInput = inputString.split(":")
        newInput = tempInput[0]
        #print (str(tempInput) + " Is our temp")
        print (str(newInput) + " is our new input check node and it returns as " + str(newInput[-1].isdigit()))
        return newInput[-1].isdigit()
    else:
        return inputString[-1].isdigit()
         
       
def flatten(l, nl):
    for sublist in l:
        for item in sublist:
            nl.append(item)
    
    
#def deleteExtra():
    #for i in currentNonUniqueShadersList:
        #cmds.delete(i)
cmds.progressBar(progressControl, edit=True, maxValue = len(shaders))
cmds.showWindow( myWindow )
    
    
uniqueShader = shaders[0]##
currentNonUniqueShadersList = []##
currentObjectsList = []##
flatList = []
objectList = []
for currentShader in shaders:
    #check if it has a number
    if(checkNumbers(currentShader) == True):
        currentNonUniqueShadersList.append(currentShader)
        print currentShader + " has a number"
        shaderCon = cmds.listConnections(currentNonUniqueShadersList)
        objectList = cmds.listRelatives(shaderCon ,type='transform' ,p=True)
        currentObjectsList.append(objectList)
        
        #flatten(currentObjectsList, flatList)
        cmds.progressBar(progressControl, edit=True, step=1)
        #cmds.select(shaderCon)
        cmds.select(shaderCon)
        cmds.hyperShade(a = uniqueShader)

            
    if(checkNumbers(currentShader) == False):
        #if it doesnt have a number
        #set the UNIQUE shader to be used
        uniqueShader = currentShader
        
        cmds.progressBar(progressControl, edit=True, step=1)
        currentObjectsList = []

        
        print "Unique shader: " + uniqueShader
        print "Object List: " + str(objectList)
cmds.progressBar(progressControl, edit = True, visible = False)        
cmds.progressBar(progressControl2, edit = True, visible = True)        
cmds.progressBar(progressControl2, edit=True, maxValue = len(currentNonUniqueShadersList))

for i in currentNonUniqueShadersList:
    cmds.progressBar(progressControl2, edit=True, step=1)
    engine = cmds.listConnections(i, d = True, s = False)
    if('defaultShaderList1' in engine):
        engine.remove('defaultShaderList1')
    cmds.delete(i)
    cmds.delete(engine)

cmds.deleteUI(myWindow)

    
