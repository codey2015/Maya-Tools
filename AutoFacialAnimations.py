import pymel.core as pm
import OptionsWindowBaseClass


"""
This tool will be used for automatic facial animations. The user will give their base facial curves aka
curves parented to a base circle around a face. They will then choose individual curves to place joints on.
Then, they will hit a button and it will duplicate the "animated" faces. Then, maybe, they will
hit a button to attach their facial geometry with blendshapes.


"""
     
class facialAnimations():
    allJoints = []    
    def selectCurves(self, curves):
        curve1 = pm.ls(sl = True)[0]
        curve2 = pm.ls(sl = True)[0]
        if (curves == 'geometry'):
            pm.textField(self.loadCurves, e = True, text = str(curve1))
        if (curves == 'curves'):
            pm.textField(self.loadCurves2, e = True, text = str(curve2))
       
    def duplicateItem(self, *args):
        mesh = pm.textField(self.loadCurves, q = True, text = True)
        #will use when I am NOT testing with a blendshape that's already created
        myBlendShp = pm.blendShape(mesh, n = "Blend Facial Animations")
        
        happy = pm.duplicate(mesh, n = mesh + '_happy')[0]
        happyChdr = pm.listRelatives(happy, ni = True)
        for child in happyChdr[1:]:
            pm.select(child)
            self.selectedCurve = child
            self.happyFace()
            #print child 
        pm.blendShape(myBlendShp, edit = True, t =  (mesh,0,happy,1))
               
        sad = pm.duplicate(mesh, n = mesh + '_sad')[0]
        sadChdr = pm.listRelatives(sad, ni = True)
        for child in sadChdr[1:]:
            pm.select(child)
            self.selectedCurve = child
            self.sadFace()
        pm.blendShape(myBlendShp, edit = True, t =  (mesh,1,sad,1))
    
        mad = pm.duplicate(mesh, n = mesh + '_mad')[0]
        madChdr = pm.listRelatives(mad, ni = True)
        for child in madChdr[1:]:
            pm.select(child)
            self.selectedCurve = child
            self.madFace()
        pm.blendShape(myBlendShp, edit = True, t =  (mesh,2,mad,1))

        
        
        confused = pm.duplicate(mesh, n = mesh + '_confused')[0]
        confusedChdr = pm.listRelatives(confused, ni = True)
        for child in confusedChdr[1:]:
            pm.select(child)
            self.selectedCurve = child
            self.confusedFace()
        pm.blendShape(myBlendShp, edit = True, t =  (mesh,3,confused,1))
        
        bored = pm.duplicate(mesh, n = mesh + '_bored')[0]
        boredChdr = pm.listRelatives(bored, ni = True)
        for child in boredChdr[1:]:
            pm.select(child)
            self.selectedCurve = child
            self.boredFace()
        pm.blendShape(myBlendShp, edit = True, t =  (mesh,4,bored,1))
        
        
        pm.move(happy, [10,0,0], relative = True, objectSpace = True, worldSpaceDistance = True)
        pm.move(sad, [20,0,0], relative = True, objectSpace = True, worldSpaceDistance = True)
        pm.move(mad, [30,0,0], relative = True, objectSpace = True, worldSpaceDistance = True)
        pm.move(confused, [40,0,0], relative = True, objectSpace = True, worldSpaceDistance = True)
        pm.move(bored, [50,0,0], relative = True, objectSpace = True, worldSpaceDistance = True)
        
        
    def moveCurves(self, *args):
        facialCurves = pm.textField(self.loadCurves2, q = True, text = True)
        pm.softSelect(sse = 1)
     
     
     
     
    def happyFace(self, *args):
        self.upperLip = self.selectedCurve
        endPoint = pm.getAttr(self.upperLip + ".spans") + 1
        endVtx = self.upperLip + ".cv[%d]"%endPoint
        startPoint = 0
        startVtx = self.upperLip + ".cv[%d]"%startPoint
        tempVar = 0.5
        ##test 
        #pm.softSelect(sse = 1, ssd = 4.50, ssf = 0, ssc='0,1,2,1,0,2')
        pm.softSelect(sse = 1, ssd = 1)
        #pm.move(thisCurve.cv[0], [0,.5,0], relative = True, objectSpace = True, worldSpaceDistance = True)
        #pm.nurbsCurveToBezier()

        #pm.xform(startVtx, t =[0,0.5,0],relative = True, objectSpace = True)
        #pm.xform(endVtx, t =[0,0.5,0],relative = True, objectSpace = True)
        pm.softSelect(sse = 0)
        #pm.scale(thisCurve + ".cv[%d:%d]"%(endPoint/2 - 1,endPoint), [1,1.25,1], relative = True, objectSpace = True)
        #pm.scale(thisCurve + ".cv[%d:%d]"%(0,endPoint/2), [1,1.25,1], relative = True, objectSpace = True)
        #pm.scale(startVtx, [1,1.5,1], relative = True, objectSpace = True)
        
        for i in range(endPoint):
            vtxName = self.upperLip + ".cv[%d]"%i   
            print vtxName
            print str(tempVar) + " TEMPVAR"
            print endPoint/2
            if i < endPoint/2:
                pm.move(vtxName, [0,tempVar,0], relative = True, objectSpace = True)
                tempVar -= .05 
            if i == endPoint/2:
                pm.move(vtxName, [0,tempVar,0], relative = True, objectSpace = True)
                tempVar += .05 

            if i > endPoint/2:
                pm.move(vtxName, [0,tempVar,0], relative = True, objectSpace = True)
                tempVar += .05 
            if(tempVar >= .5):
                tempVar = .5
                
                
            
    def sadFace(self, *args):
        self.upperLip = self.selectedCurve
        endPoint = pm.getAttr(self.upperLip + ".spans") + 1
        endVtx = self.upperLip + ".cv[%d]"%endPoint
        startPoint = 0
        startVtx = self.upperLip + ".cv[%d]"%startPoint
        tempVar = -0.35

     
        for i in range(endPoint):
            vtxName = self.upperLip + ".cv[%d]"%i   
            print vtxName
            print str(tempVar) + " TEMPVAR"
            print endPoint/2
            if i < endPoint/2:
                pm.move(vtxName, [0.15,tempVar,0], relative = True, objectSpace = True)
                tempVar += .1 
            if i == endPoint/2:
                pm.move(vtxName, [0,tempVar,0], relative = True, objectSpace = True)
                tempVar -= .1 
        
            if i > endPoint/2:
                pm.move(vtxName, [-0.1,tempVar,0], relative = True, objectSpace = True)
                tempVar -= .1 
            if(tempVar >= .5):
                tempVar = .5        
                    
    def madFace(self, *args):
        self.upperLip = self.selectedCurve
        endPoint = pm.getAttr(self.upperLip + ".spans") + 1
        endVtx = self.upperLip + ".cv[%d]"%endPoint
        startPoint = 0
        startVtx = self.upperLip + ".cv[%d]"%startPoint
        tempVar = -0.25

     
        for i in range(endPoint):
            vtxName = self.upperLip + ".cv[%d]"%i   
            print vtxName
            print str(tempVar) + " TEMPVAR"
            print endPoint/2
            if i < endPoint/2:
                pm.move(vtxName, [0,tempVar,0], relative = True, objectSpace = True)
                tempVar += .2 
            if i == endPoint/2:
                pm.move(vtxName, [0,tempVar,0], relative = True, objectSpace = True)
                tempVar -= .2 
        
            if i > endPoint/2:
                pm.move(vtxName, [0,tempVar,0], relative = True, objectSpace = True)
                tempVar -= .2 
            if(tempVar >= .5):
                tempVar = .5  
                
                  
    def confusedFace(self, *args):
        self.upperLip = self.selectedCurve
        endPoint = pm.getAttr(self.upperLip + ".spans") + 1
        endVtx = self.upperLip + ".cv[%d]"%endPoint
        startPoint = 0
        startVtx = self.upperLip + ".cv[%d]"%startPoint
        tempVar = -0.05

     
        for i in range(endPoint):
            vtxName = self.upperLip + ".cv[%d]"%i   
            print vtxName
            print str(tempVar) + " TEMPVAR"
            print endPoint/2
            if i < endPoint/2:
                pm.move(vtxName, [.05,tempVar,0], relative = True, objectSpace = True)
                tempVar += .15 
            if i == endPoint/2:
                pm.move(vtxName, [0,tempVar,0], relative = True, objectSpace = True)
                tempVar -= .15 
        
            if i > endPoint/2:
                pm.move(vtxName, [-.05,tempVar,0], relative = True, objectSpace = True)
                tempVar += .15 
            if(tempVar >= .5):
                tempVar = .5  
                
    def boredFace(self, *args):
        self.upperLip = self.selectedCurve
        endPoint = pm.getAttr(self.upperLip + ".spans") + 1
        endVtx = self.upperLip + ".cv[%d]"%endPoint
        startPoint = 0
        startVtx = self.upperLip + ".cv[%d]"%startPoint
        tempVar = 0.1

     
        for i in range(endPoint):
            vtxName = self.upperLip + ".cv[%d]"%i   
            print vtxName
            print str(tempVar) + " TEMPVAR"
            print endPoint/2
            if i < endPoint/2:
                pm.move(vtxName, [0,tempVar,0], relative = True, objectSpace = True)
                tempVar += .075
            if i == endPoint/2:
                pm.move(vtxName, [0,tempVar,0], relative = True, objectSpace = True)
                tempVar -= .075
        
            if i > endPoint/2:
                pm.move(vtxName, [0,tempVar,0], relative = True, objectSpace = True)
                tempVar -= .075 
            if(tempVar >= .5):
                tempVar = .5         
     
     
     
        
    
    def addJointsToCurve(self, *args):
        self.jointsList = []
        self.jointsListGRP = []
        try:
            numOfJoints = pm.intField(self.loadNumJoints, q = True, v = True)
            self.selectedCurve = pm.ls(sl = True)[0]
            incr = float((numOfJoints - 1))
            incr = 1/incr #calculate incrementation
            print incr
            incrTemp = 0.0
            

            for i in range(numOfJoints):
                pm.select(clear = True)
                j = pm.joint(radius = 0.25, n = self.selectedCurve + "Joint")
                self.jointsList.append(j)
                jGRP = pm.group(j, n = j + "GRP")
                self.jointsListGRP.append(jGRP)
                #attach to motion path
                motionPath = pm.pathAnimation(jGRP, self.selectedCurve, fractionMode = True, follow = True )
                pm.setAttr(motionPath +".u", incrTemp)
                pm.cutKey(motionPath)
                incrTemp += incr
                print incrTemp
                if incrTemp >= 1.0:
                    incrTemp = 1.0
                    
            facialAnimations.allJoints.append(self.jointsList)
            self.curvesGRP = pm.group(self.jointsListGRP, n = self.selectedCurve + "_Face_jointsGRP")
        except:
            pass
            print "Curve not selected"
            
            
    def bindToMesh(self, *args):
        mesh = pm.textField(self.loadCurves2, q = True, text = True)
        jntLst = facialAnimations.allJoints
        print jntLst
        pm.select(pm.ls(sl = True))
        pm.select(jntLst, add = True)
        pm.select(mesh, add = True)
        #pm.bindSkin(mesh, jntLst)
        pm.skinCluster()    
            

face = facialAnimations()

class autoFacialAnimations(OptionsWindowBaseClass.OptionsWindow):
    
    def __init__(self):
        OptionsWindowBaseClass.OptionsWindow.__init__(self)
        self.title = "Facial Blend Shapes"
        self.actionName = "Create"
        self.applyName = "Bind Mesh"
        #self.size = (546,350)
        
    def helpMenuCmd(self, *args): 
        pm.confirmDialog( title='About',icn = "information", message='This tool will aid in the creation of basic facial blend shapes.\n\nStep 1: Load in your base curves. It should be a circular shape with children curves for eyebrows, lips, etc.\nStep 2: Hit the create button and make 5 different faces that can be modified.\nStep 3: Add any number of joints to the curves.\nStep 4 (Optional): Load the mesh you want to bind and hit Bind.', button=['Back'], defaultButton='Yes', cancelButton='No', dismissString='No' )

      
    def displayOptions(self):
        #pm.setParent("|")
        #loadCurves = pm.textFieldButtonGrp(text = " ", editable = False, buttonLabel = "Load Curves", buttonCommand = lambda x: face.selectCurves("curve1") )    
        pm.rowColumnLayout(nc = 4)
        pm.text(l = 'Load Base Shape:')
        pm.separator(width = 50, style = 'none')
        facialAnimations.loadCurves = pm.textField(text = '', editable = False)
        pm.button(l = '<<', width = 30,c = self.curve1Helper) #c = lambda x: face.selectCurves('curve1'))
        
        pm.text(l = 'Load Mesh Geometry:')
        pm.separator(width = 50, style = 'none')
        pm.rowColumnLayout(nr = 2)
        facialAnimations.loadCurves2 = pm.textField(text = '', editable = False)
        pm.setParent("..")
        pm.button(l = '<<', width = 30,c = self.curve2Helper) #c = lambda x: face.selectCurves('curve1'))
        
        pm.text(l = 'Add n Joints to selected Curve:')
        pm.separator(width = 50, style = 'none')
        pm.rowColumnLayout(nr = 2)
        facialAnimations.loadNumJoints = pm.intField( v = 1, editable = True)
        pm.setParent("..")
        pm.button(l = '<<', width = 30,c = self.addJoints)

    def actionCmd(self,*args):
        try:
            self.test()  
        except:
            pass  
            print "Nothing Selected"  
        #finally:
            #face.duplicateItem()
            
    def applyBtnCmd(self,*args):
        #pm.bindSkin(face.jointsList, face.loadCurves2)
        face.bindToMesh()
        

        
    def catchBlank(self, curv, *args):
            try:
                face.selectCurves(face.selectCurves(curv))
            except IndexError:
                pass
                print 'Out of Range' 
                
                
    def curve1Helper(self, *args):
        self.catchBlank("geometry")
                
    def curve2Helper(self, *args):
        self.catchBlank("curves")  
        
        
    def test(self, *args):
        face.duplicateItem()   
        face.moveCurves()
        
        
    def addJoints(self, *args):
        face.addJointsToCurve()  
        
       
        
win = autoFacialAnimations()
win.create()        
