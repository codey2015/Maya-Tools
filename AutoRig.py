import maya.cmds as mc
"""
This tool will aid in the creation of a humanoid rig.
It takes all the neccessary steps to set up a basic humanoid rig
"""
winID = "AutoRig"
if mc.window(winID, exists=True):
    mc.deleteUI(winID)
    
myWindow = mc.window(winID, title = "AutoRig", menuBar = True, nde = True, s = True, tlc = (300,1000))
mc.frameLayout(l = "Skeleton SetUp", mw = 4, mh = 4, bgc = [0.15, 0.25, 0.3])
mc.rowColumnLayout(nc = 2)

mc.text(l = "Place Joints: ")
placeJointsBtn = mc.button(l = "Place", w = 175, h = 30 ,c = "placeJoints()")

mc.text(l = "Make Controls: ")
placeControlsBtn = mc.button(l = "Make", w = 175, h = 30 ,c = "controlsSetUp()")


mc.text(l = "AutoRig: ")
autorigbtn = mc.button(l = "Create", w = 150, h = 30, c = "finishAutoRig()")

mc.setParent('..')
mc.frameLayout(l = "Skin SetUp", mw = 4, mh = 4, bgc = [0.15, 0.25, 0.3])

mc.rowColumnLayout(nc = 2)


mc.text(l = "Bind selected mesh: ")
bindMeshBtn = mc.button(l = "Bind", w = 150, h = 30, c = "selectMesh()")

mc.text(l = "Add Flexor: ")
addFlexorBtn = mc.button(l = "Add", w = 150, h = 30, c = "addFlexor()")

#mc.text(l = "Unbind selected mesh: ")#Make a checkbox for this later
#unBindBtn = mc.button(l = "Unbind", w = 150, h = 30, c = "unBind()")

mc.text(l = "Quit: ")
mc.button(l = "Exit", w = 150, h = 30, c = "quitBtn()", bgc = (.45,0,0))

mc.menu( label='Help', tearOff=True )

mc.menuItem( divider=True )
aboutMenu = mc.menuItem( 'Application..."', label='About', itl = True , c = "helpMenu()")

mc.showWindow(myWindow)

mc.disable(placeControlsBtn, v=True)
mc.disable(autorigbtn, v=True)

spineJoints = []#positioning
armJointsL = []#positioning
armJointsR = []#positioning
legJointsL = []#positioning
legJointsR = []#positioning
reverseFootL = []#Reverse foot positioning
reverseFootR = []#Reverse foot positioning
SJ = [] #spine joints
RFL = []#RF joint
RFR = []#RF joint
AJL = []#arm joint
AJR = []#arm joint
LJL = []#leg joint
LJR = []#leg joint
clusters = []

def helpMenu():
    mc.confirmDialog( title='About',icn = "information", message='This tool will aid in the creation of a humanoid rig.\n\nStep 1: Place the joint locations (type sorted by color).\nStep 2: Hit the AutoRig button and it will complete the skeleton setup for you.\nStep 3: Select the mesh you want to bind and hit "Bind"\nStep 4 (Optional): Add additional flexors to smooth out any rough areas.', button=['Back'], defaultButton='Yes', cancelButton='No', dismissString='No' )

def quitBtn():
    mc.deleteUI(myWindow)
    
def placeJoints():
    placespineJoints()
    placeArmJoints()
    placeLegJoints()
    placeReverseFoot()
    #protect the user from themself
    mc.disable(placeJointsBtn, v=True)
    mc.disable(placeControlsBtn, v=False)

    
def finishAutoRig(): 
    createspineJoints()
    createArmJoints()
    createLegJoints()
    createReverseFoot()
    createAndPlaceControls()
    connectJoints()
    
    deleteLocators()
    mc.select(clear= True)
    #selectMesh()
    #protect the user from themself
    mc.disable(autorigbtn, v=True)
    

def selectMesh():
    global characterMesh
    characterMesh = mc.ls(sl=True)
    meshChildren = mc.ls(mc.listRelatives(characterMesh, ad = True, type = "transform"), dag = True, lf = True, ni = True)
    print meshChildren
    #influences = []
    #for i in SJ:
        #influences.append(i)
    #c = []
    #c = mc.ls(mc.listRelatives(characterMesh, ad = True, type = "transform"), dag = True, lf = True, ni = True)
    #print c
    #for i in c:
        #print i
        #mc.skinCluster(influences,i, toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1)
    
    #WILL SMOOTH BIND INDIVIDUALLY. MAKE OPTION FOR UNNBIND
    #OR TELL THEM TO BIND SKIN THEN ENHANCE IT
    ###mc.skinCluster(characterMesh,mc.ls(sl=True), toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1, useGeometry = True)
    #mc.skinCluster(characterMesh,mc.ls(sl=True),smoothWeights = .1, bindMethod=0, skinMethod=0, normalizeWeights=1, weightDistribution = 0, dropoffRate = 1.0)
    
    tempSJ = []
    tempSJ = LJR[:] + LJL[:] + AJR[:] + AJL[:] + SJ[1:] + RFL[:] + RFR[:]
    print "tempSJ: " + str(tempSJ)
    mc.bindSkin(characterMesh, tempSJ, tsb = True, cj = True )
    #cmds.select( ['pPlane1.vtx[5]', 'pPlane1.vtx[11]', 'pPlane1.vtx[17]', 'pPlane1.vtx[23]'])
    #cmds.percent( 'testCluster', v=0.5 )
    #t =  SJ[2:]
    #mc.flexor(t, type = "jointLattice", aj = True)
    mc.flexor(LJL[0], type = "jointCluster", aj = True)
    mc.flexor(LJR[0], type = "jointCluster", aj = True)

    mc.disable(bindMeshBtn, v=True)

def addFlexor():
    t = (mc.ls(sl = True))
    #mc.flexor(t, type = "jointCluster", aj = True)
    mc.flexor(t, type = "jointLattice", aj = True)

def unBind():
    unBindMesh = mc.ls(sl=True)
    mc.skinCluster(unBindMesh, e = True ,unbind = True)



def placespineJoints():
    mc.select(clear= True)
#Create locators where spineJoints will be then create spineJoints
    root = mc.spaceLocator( p=(0, 27, 0) , n = "root1")
    mc.xform(cp = True)
    mc.color(rgb = (1,0,0))
    spineJoints.append(root)
    pelvis = mc.spaceLocator( p=(0, 30, -1.3), n = "pelvis1" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,0))
    spineJoints.append(pelvis)
    abs = mc.spaceLocator( p=(0, 32, -0.4), n = "abs1" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,0))
    spineJoints.append(abs)
    baseRibCage = mc.spaceLocator( p=(0, 34, -0.63), n = "baseRibCage1" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,0))
    spineJoints.append(baseRibCage)
    chest = mc.spaceLocator( p=(0, 37.5, -1.35), n = "chest1" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,0))
    spineJoints.append(chest)
    topRibCage = mc.spaceLocator( p=(0, 41.7, -1.35), n = "topRibCage1" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,0))
    spineJoints.append(topRibCage)
    neck = mc.spaceLocator( p=(0, 42.2, -1.25), n = "neck1" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,0))
    spineJoints.append(neck)
    skullBase = mc.spaceLocator( p=(0, 46.3, -0.75), n = "skullBase1" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,0))
    spineJoints.append(skullBase)
    headNub = mc.spaceLocator( p=(0, 50.6, -0.35), n = "headNub1" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,0))
    spineJoints.append(headNub)

    print spineJoints
    
def placeArmJoints():
    shoulderL = mc.spaceLocator( p=(4, 40.675, -1.0), n = "shoulderL" )
    mc.xform(cp = True)
    mc.color(rgb = (1,.65,0))
    armJointsL.append(shoulderL)
    elbowL = mc.spaceLocator( p=(10.8, 40.675, -2.15), n = "elbowL" )
    mc.xform(cp = True)
    mc.color(rgb = (1,.65,0))
    armJointsL.append(elbowL)
    wristL = mc.spaceLocator( p=(18.5, 40.675, -1.55), n = "wristL" )
    mc.xform(cp = True)
    mc.color(rgb = (1,.65,0))
    armJointsL.append(wristL)
    shoulderR = mc.spaceLocator( p=(-4, 40.675, -1.0), n = "shoulderR" )
    mc.xform(cp = True)
    mc.color(rgb = (1,.65,0))
    armJointsR.append(shoulderR)
    elbowR = mc.spaceLocator( p=(-10.8, 40.675, -2.15), n = "elbowR" )
    mc.xform(cp = True)
    mc.color(rgb = (1,.65,0))
    armJointsR.append(elbowR)
    wristR = mc.spaceLocator( p=(-18.5, 40.675, -1.55), n = "wristR" )
    mc.xform(cp = True)
    mc.color(rgb = (1,.65,0))
    armJointsR.append(wristR)
    
    
    
    
def placeLegJoints():
    hipL = mc.spaceLocator( p=(2.5, 28.1, -1.85), n = "hipL" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,1))
    legJointsL.append(hipL)
    kneeL = mc.spaceLocator( p=(2.5, 15.39, -0.5), n = "kneeL" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,1))
    legJointsL.append(kneeL)
    ankleL = mc.spaceLocator( p=(2.5, 3.183, -1.911), n = "ankleL" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,1))
    legJointsL.append(ankleL)
    archL = mc.spaceLocator( p=(2.5, 0.3, -0.6), n = "archL" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,1))
    legJointsL.append(archL)
    toeL = mc.spaceLocator( p=(2.5, 0.3, 2.64), n = "toeL" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,1))
    legJointsL.append(toeL)
    hipR = mc.spaceLocator( p=(-2.5, 28.1, -1.85), n = "hipR" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,1))
    legJointsR.append(hipR)   
    kneeR = mc.spaceLocator( p=(-2.5, 15.39, -0.5), n = "kneeR" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,1))
    legJointsR.append(kneeR)
    ankleR = mc.spaceLocator( p=(-2.5, 3.183, -1.911), n = "ankleR" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,1))
    legJointsR.append(ankleR)
    archR = mc.spaceLocator( p=(-2.5, 0.3, -0.6), n = "archR" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,1))
    legJointsR.append(archR)
    toeR = mc.spaceLocator( p=(-2.5, 0.3, 2.64), n = "toeR" )
    mc.xform(cp = True)
    mc.color(rgb = (1,0,1))
    legJointsR.append(toeR)   
    
    
    
def placeReverseFoot():
    pos = mc.pointPosition(legJointsL[4])
    RFHeelL = mc.spaceLocator( p=(pos[0], pos[1], pos[2] - 5.75), n = "RFHeelL" )    
    mc.xform(cp = True)
    mc.color(rgb = (1,1,1))
    reverseFootL.append(RFHeelL)
    RFToeL = mc.spaceLocator( p = mc.pointPosition(legJointsL[4]), n = "RFToeL")
    mc.xform(cp = True)
    mc.color(rgb = (1,1,1))
    reverseFootL.append(RFToeL)
    RFArchL = mc.spaceLocator( p = mc.pointPosition(legJointsL[3]), n = "RFArchL")
    mc.xform(cp = True)
    mc.color(rgb = (1,1,1))
    reverseFootL.append(RFArchL)
    RFAnkleL = mc.spaceLocator( p = mc.pointPosition(legJointsL[2]), n = "RFAnkleL")
    mc.xform(cp = True)
    mc.color(rgb = (1,1,1))
    reverseFootL.append(RFAnkleL)
    
    
    pos = mc.pointPosition(legJointsR[4])
    RFHeelR = mc.spaceLocator( p=(pos[0], pos[1], pos[2] - 5.75), n = "RFHeelR" )
    print pos[2]
    mc.xform(cp = True)
    mc.color(rgb = (1,1,1))
    reverseFootR.append(RFHeelR)
    RFToeR= mc.spaceLocator( p = mc.pointPosition(legJointsR[4]), n = "RFToeR")
    mc.xform(cp = True)
    mc.color(rgb = (1,1,1))
    reverseFootR.append(RFToeR)
    RFArchR = mc.spaceLocator( p = mc.pointPosition(legJointsR[3]), n = "RFArchR")
    mc.xform(cp = True)
    mc.color(rgb = (1,1,1))
    reverseFootR.append(RFArchR)
    RFAnkleR = mc.spaceLocator( p = mc.pointPosition(legJointsR[2]), n = "RFAnkleR")
    mc.xform(cp = True)
    mc.color(rgb = (1,1,1))
    reverseFootR.append(RFAnkleR)

    
def createspineJoints():
    spine = []
    global ikneck
    global ikSpineSpline
    global spline
    mc.select(clear= True)
#get pos of locators and add spineJoints to them
    for i in spineJoints:
        print i
        pos = mc.pointPosition(i)
        print pos
        spine.append(mc.joint(p = pos, n = str(i)))
        mc.color(ud = 5)
        #mc.hide(i)
        #mc.delete(i)
    #orient spineJoints and then nub
    mc.joint(spine[0], e = True, oj = "xyz", sao = "yup", ch = True, zso = True)
    mc.joint(spine[8], e = True, o = [0,0,0])
    ikneck = mc.ikHandle( sj = spine[6], ee=spine[7], solver = "ikRPsolver" )
    mc.color(ikneck, rgb = (1,.65,0))
    
    ikSpineSpline = mc.ikHandle( sj = spine[1], ee=spine[5],solver = "ikSplineSolver" )
    mc.color(ikSpineSpline, rgb = (1,.55,0))
    mc.select(ikSpineSpline[2])
    spline = mc.rename("ikSpineSpline")
    mc.parent(w = True)
    
    mc.select(clear = True)
    pos = mc.pointPosition(spineJoints[3])
    for i in range(0, 4):
       vtxName = "ikSpineSpline"+".cv[%d]"%i
       print vtxName
       pos2 = mc.pointPosition(spineJoints[2+i])
       mc.select(vtxName)
       clust = mc.cluster()
       clusters.append(clust[1])
       mc.setAttr(clust[1]+ ".originZ", pos[2] -5)
       if i > 0:
           mc.xform(clust[1], piv = (pos2[0],pos2[1],pos2[2]))
       #mc.move(0,0,-5, cs = True)
       #mc.cluster(e=1, bs=1)
    print clusters
       
    SJ[:] = spine[:]
    mc.select(clear= True)
    #spineJoints[:] = []
    print "spineJoints: " + str(spineJoints)
  
  
def createArmJoints():
    joints = []
    global ikarmL #make global for later constraints
    global ikarmR #make global for later constraints
    mc.select(clear= True)
#get pos of locators and add Joints to them
    for i in armJointsL:
        print i
        pos = mc.pointPosition(i)
        print pos
        joints.append(mc.joint(p = pos, n = str(i)))
        mc.color(ud = 5)
    #orient spineJoints and then nub
    mc.joint(joints[0], e = True, oj = "xyz", sao = "yup", ch = True, zso = True)
    mc.joint(joints[2], e = True, o = [0,0,0])
    ikarmL = mc.ikHandle( sj = joints[0], ee=joints[2], solver = "ikRPsolver" )
    mc.color(ikarmL, rgb = (1,.55,0))
    AJL[:] = joints[:]
    #print ikarmL

    joints[:] = []
    mc.select(clear= True)
    for i in armJointsR:
        print i
        pos = mc.pointPosition(i)
        print pos
        joints.append(mc.joint(p = pos, n = str(i)))
        mc.color(ud = 5)

    #orient spineJoints and then nub
    mc.joint(joints[0], e = True, oj = "xyz", sao = "yup", ch = True, zso = True)
    mc.joint(joints[2], e = True, o = [0,0,0])
    ikarmR = mc.ikHandle( sj = joints[0], ee=joints[2], solver = "ikRPsolver" )
    mc.color(ikarmR, rgb = (1,.55,0))
    AJR[:] = joints[:]

    mc.select(clear= True)

    
    print "armJointsL: " + str(armJointsL)
    print "armJointsR: " + str(armJointsR)
    





def createLegJoints():
    joints = []
    global iklegL #make global for later constraints
    global iklegR #make global for later constraints
    global ikankleL #make global for later parenting
    global ikankleR #make global for later parenting
    global iktoeL #make global for later parenting
    global iktoeR #make global for later parenting
    mc.select(clear= True)
#get pos of locators and add Joints to them
    for i in legJointsL:
        print i
        pos = mc.pointPosition(i)
        print pos
        joints.append(mc.joint(p = pos, n = str(i)))
        mc.color(ud = 5)
        #mc.hide(i)
        #mc.delete(i)
    #orient spineJoints and then nub
    mc.joint(joints[0], e = True, oj = "xyz", sao = "yup", ch = True, zso = True)
    mc.joint(joints[4], e = True, o = [0,0,0])
    
    iklegL = mc.ikHandle( sj = joints[0], ee=joints[2], solver = "ikRPsolver" )
    mc.color(iklegL, rgb = (1,.55,0))
    ikankleL = mc.ikHandle( sj = joints[2], ee=joints[3], solver = "ikSCsolver" )
    mc.color(ikankleL, rgb = (1,.55,0))
    iktoeL = mc.ikHandle( sj = joints[3], ee=joints[4], solver = "ikSCsolver" )
    mc.color(iktoeL, rgb = (1,.55,0))
    LJL[:] = joints[:]

    joints[:] = []
    mc.select(clear= True)
    for i in legJointsR:
        print i
        pos = mc.pointPosition(i)
        print pos
        joints.append(mc.joint(p = pos, n = str(i)))
        mc.color(ud = 5)
    #orient spineJoints and then nub
    mc.joint(joints[0], e = True, oj = "xyz", sao = "yup", ch = True, zso = True)
    mc.joint(joints[4], e = True, o = [0,0,0])
    
    iklegR = mc.ikHandle( sj = joints[0], ee=joints[2], solver = "ikRPsolver" )
    mc.color(iklegR, rgb = (1,.55,0))
    ikankleR = mc.ikHandle( sj = joints[2], ee=joints[3], solver = "ikSCsolver" )
    mc.color(ikankleR, rgb = (1,.55,0))
    iktoeR = mc.ikHandle( sj = joints[3], ee=joints[4], solver = "ikSCsolver" )
    mc.color(iktoeR, rgb = (1,.55,0))
    LJR[:] = joints[:]
    
    mc.select(clear= True)

    print "legJointsL: " + str(legJointsL)
    print "legJointsR: " + str(legJointsR)


def createReverseFoot():
    joints = []
    mc.select(clear= True)
#get pos of locators and add Joints to them
    for i in reverseFootL:
        print i
        pos = mc.pointPosition(i)
        print pos
        joints.append(mc.joint(p = pos, n = str(i), radius = 0.75))
        mc.color(rgb = (1,1,1))
             
    RFL[:] = joints[:]

    #mc.parent(iklegL,RFL[3])
    joints[:] = []
    mc.select(clear= True)
    
    for i in reverseFootR:
        print i
        pos = mc.pointPosition(i)
        print pos
        joints.append(mc.joint(p = pos, n = str(i), radius = 0.75))
        mc.color(rgb = (1,1,1))
        
        
    RFR[:] = joints[:]
    #mc.parent(iklegR, joints[3])
    mc.select(clear= True)



def controlsSetUp():
    mc.select(clear= True)
    ##Make left arm Controls
    global shoulderLControl
    shoulderLControl = mc.circle(c = (0,0,0), r = 3, nr = (1, 0, 0), n = "shoulderLControl")
    mc.color(ud = 2)
    global shoulderLControlGRP
    shoulderLControlGRP = mc.group(shoulderLControl, n = "shoulderLControlGRP")
    global elbowLControl
    elbowLControl = mc.circle(c = (0,0,0), r = 2, nr = (1, 0, 0), n = "elbowLControl")
    mc.color(ud = 2)
    global elbowLControlGRP
    elbowLControlGRP = mc.group(elbowLControl, n = "elbowLControlGRP")
    global wristLControl
    wristLControl = mc.circle(c = (0,0,0), r = 1, nr = (1, 0, 0), n = "wristLControl")
    mc.color(ud = 2)
    global wristLControlGRP
    wristLControlGRP = mc.group(wristLControl, n = "wristLControlGRP")
    global armControlL
    armControlL = mc.curve(d = 1, n = "armControlL", p =( (-0.5, 0.5 ,-0.5 ),( -0.5 ,-0.5, -0.5 ),( -0.5 ,-0.5, 0.5 ),( 0.5, -0.5 ,0.5 ),( 0.5, 0.5, 0.5 ),( 0.5, 0.5, -0.5 ),( 0.5, -0.5, -0.5 ),( 0.5, -0.5, 0.5 ),( 0.5, 0.5, 0.5 ),( -0.5, 0.5, 0.5 ),( -0.5, -0.5, 0.5 ),( -0.5, 0.5, 0.5 ),( -0.5, 0.5 ,-0.5 ),( 0.5, 0.5 ,-0.5 ),( 0.5, -0.5 ,-0.5 ),( -0.5 ,-0.5, -0.5 )))
    mc.color(ud = 2)
    global armControlLGRP
    armControlLGRP = mc.group(armControlL, n = "armControlRGRP")
    
    ##Position left arm Controls / Constrain Orientation/rotation
    #Note: Doesn't "work" if IK already exists(constraint that is)
    pos = mc.pointPosition(armJointsL[0])
    mc.move(pos[0],pos[1],pos[2], shoulderLControlGRP)
    pos = mc.pointPosition(armJointsL[1])
    mc.move(pos[0],pos[1],pos[2], elbowLControlGRP)
    #parent elbow group to shoulder so it doesn't bend weirdly
    pos = mc.pointPosition(armJointsL[2])
    mc.move(pos[0],pos[1],pos[2], wristLControlGRP)
    pos = mc.pointPosition(armJointsL[2])
    mc.move(pos[0],pos[1],pos[2], armControlLGRP)
    
    ##Make right arm Controls
    global shoulderRControl
    shoulderRControl = mc.circle(c = (0,0,0), r = 3, nr = (1, 0, 0), n = "shoulderRControl")
    mc.color(ud = 2)
    global shoulderRControlGRP
    shoulderRControlGRP = mc.group(shoulderRControl, n = "shoulderRControlGRP")
    global elbowRControl
    elbowRControl = mc.circle(c = (0,0,0), r = 2, nr = (1, 0, 0), n = "elbowRControl")
    mc.color(ud = 2)
    global elbowRControlGRP
    elbowRControlGRP = mc.group(elbowRControl, n = "elbowRControlGRP")
    global wristRControl
    wristRControl = mc.circle(c = (0,0,0), r = 1, nr = (1, 0, 0), n = "wristRControl")
    mc.color(ud = 2)
    global wristRControlGRP
    wristRControlGRP = mc.group(wristRControl, n = "wristRControlGRP")
    global armControlR
    armControlR = mc.curve(d = 1, n = "armControlR", p =( (-0.5, 0.5 ,-0.5 ),( -0.5 ,-0.5, -0.5 ),( -0.5 ,-0.5, 0.5 ),( 0.5, -0.5 ,0.5 ),( 0.5, 0.5, 0.5 ),( 0.5, 0.5, -0.5 ),( 0.5, -0.5, -0.5 ),( 0.5, -0.5, 0.5 ),( 0.5, 0.5, 0.5 ),( -0.5, 0.5, 0.5 ),( -0.5, -0.5, 0.5 ),( -0.5, 0.5, 0.5 ),( -0.5, 0.5 ,-0.5 ),( 0.5, 0.5 ,-0.5 ),( 0.5, -0.5 ,-0.5 ),( -0.5 ,-0.5, -0.5 )))
    mc.color(ud = 2)
    global armControlRGRP
    armControlRGRP = mc.group(armControlR, n = "armControlRGRP")
    
    ##Position right arm Controls / Constrain Orientation/rotation
    pos = mc.pointPosition(armJointsR[0])
    mc.move(pos[0],pos[1],pos[2], shoulderRControlGRP)
    pos = mc.pointPosition(armJointsR[1])
    mc.move(pos[0],pos[1],pos[2], elbowRControlGRP)
    #parent elbow group to shoulder so it doesn't bend weirdly
    
    pos = mc.pointPosition(armJointsR[2])
    mc.move(pos[0],pos[1],pos[2], wristRControlGRP)
    pos = mc.pointPosition(armJointsR[2])
    mc.move(pos[0],pos[1],pos[2], armControlRGRP)    
    
    #Make and position poleVectorarm/GRP control Left
    global PoleVectorControlElbowL
    PoleVectorControlElbowL = mc.circle(c = (0,0,0), r = 2, nr = (0,0, 1), n = "PoleVectorControlElbowL")
    mc.color(ud = 2)
    numSections = int(mc.circle(PoleVectorControlElbowL, q = True, s = True))
    mc.select(clear = True)
    for i in range(0, numSections, 2):
       vtxName = PoleVectorControlElbowL[0]+".cv[%d]"%i
       print vtxName
       mc.select(vtxName)
       mc.scale(.25,.25,.25)
    pos = mc.pointPosition(armJointsL[1])
    global PoleVectorControlElbowLGRP
    PoleVectorControlElbowLGRP = mc.group(PoleVectorControlElbowL, n = "PoleVectorControlElbowLGRP")
    mc.move(pos[0],pos[1],pos[2] - 7, PoleVectorControlElbowLGRP)
    #print ikarmL   
    #creates constraint but make sure to use all functions
    
    #Make and position poleVectorarm/GRP control Right
    global PoleVectorControlElbowR
    PoleVectorControlElbowR = mc.circle(c = (0,0,0), r = 2, nr = (0,0, 1), n = "PoleVectorControlElbowR")
    mc.color(ud = 2)
    numSections = int(mc.circle(PoleVectorControlElbowR, q = True, s = True))
    mc.select(clear = True)
    for i in range(0, numSections, 2):
       vtxName = PoleVectorControlElbowR[0]+".cv[%d]"%i
       print vtxName
       mc.select(vtxName)
       mc.scale(.25,.25,.25)
    pos = mc.pointPosition(armJointsR[1])
    global PoleVectorControlElbowRGRP
    PoleVectorControlElbowRGRP = mc.group(PoleVectorControlElbowR, n = "PoleVectorControlElbowRGRP")
    mc.move(pos[0],pos[1],pos[2] - 7, PoleVectorControlElbowRGRP) 
    #creates constraint 
    
    
    #Make and position poleVectorleg/GRP control Left
    global PoleVectorControlKneeL
    PoleVectorControlKneeL = mc.circle(c = (0,0,0), r = 2, nr = (0,0, 1), n = "PoleVectorControlKneeL")
    mc.color(ud = 2)
    numSections = int(mc.circle(PoleVectorControlKneeL, q = True, s = True))
    mc.select(clear = True)
    for i in range(0, numSections, 2):
       vtxName = PoleVectorControlKneeL[0]+".cv[%d]"%i
       print vtxName
       mc.select(vtxName)
       mc.scale(.25,.25,.25)
    pos = mc.pointPosition(legJointsL[1])
    global PoleVectorControlKneeLGRP
    PoleVectorControlKneeLGRP = mc.group(PoleVectorControlKneeL, n = "PoleVectorControlKneeLRP")
    mc.move(pos[0],pos[1],pos[2] + 7, PoleVectorControlKneeLGRP)   
    #creates constraint 
    
    #Make and position poleVectorleg/GRP control Right
    global PoleVectorControlKneeR
    PoleVectorControlKneeR = mc.circle(c = (0,0,0), r = 2, nr = (0,0, 1), n = "PoleVectorControlKneeR")
    mc.color(ud = 2)
    numSections = int(mc.circle(PoleVectorControlKneeR, q = True, s = True))
    mc.select(clear = True)
    for i in range(0, numSections, 2):
       vtxName = PoleVectorControlKneeR[0]+".cv[%d]"%i
       print vtxName
       mc.select(vtxName)
       mc.scale(.25,.25,.25)
    pos = mc.pointPosition(legJointsR[1])
    global PoleVectorControlKneeRGRP
    PoleVectorControlKneeRGRP = mc.group(PoleVectorControlKneeR, n = "PoleVectorControlKneeRGRP")
    mc.move(pos[0],pos[1],pos[2] + 7, PoleVectorControlKneeRGRP) 
    #creates constraint
    
    
    global footControlL 
    footControlL = cmds.curve(d = 3,n = "footControlL", p=(( -1.943975, 0, 0.0455116 ),( -1.793015, 0, 0.908818 ),( -1.823946, 0, 1.548806 ),( -2.057076, 0, 2.392609 ),( -2.460573, 0, 2.723015 ),( -3.024632, 0, 2.692013 ),( -3.700054, 0, 2.114125 ),( -3.994695, 0, 0.148922 ),( -3.454195, 0 ,-0.489267 ),( -3.478549, 0, -1.560035 ),( -3.48116 ,0 ,-2.460689 ),( -2.992802 ,0 ,-3.098902 ),( -2.240181, 0, -2.859905 ),( -1.947866, 0, -2.029168 ),( -2.022896, 0 ,-0.986165 ),( -2.162509, 0, -0.255072 ),( -1.943975, 0, 0.0455116)))
    mc.move(2.899,0,0,footControlL)
    mc.xform(cp = True)
    mc.makeIdentity( footControlL, apply=True )
    mc.color(rgb = (1,1,1))
    global footControlLGRP
    footControlLGRP = mc.group(footControlL, n = "footControlLGRP")
    mc.scale(-1,1,1, footControlLGRP)
    mc.makeIdentity( footControlLGRP, apply=True )
    pos = mc.pointPosition(reverseFootL[2])
    mc.move(pos[0],0,0,footControlLGRP)
    pivLoc = mc.pointPosition(reverseFootL[0])
    mc.xform(footControlL, piv = (pivLoc[0], pivLoc[1] , pivLoc[2]), ws = True)
    
    
    global footControlR
    footControlR = cmds.curve(d = 3,n = "footControlR", p=(( -1.943975, 0, 0.0455116 ),( -1.793015, 0, 0.908818 ),( -1.823946, 0, 1.548806 ),( -2.057076, 0, 2.392609 ),( -2.460573, 0, 2.723015 ),( -3.024632, 0, 2.692013 ),( -3.700054, 0, 2.114125 ),( -3.994695, 0, 0.148922 ),( -3.454195, 0 ,-0.489267 ),( -3.478549, 0, -1.560035 ),( -3.48116 ,0 ,-2.460689 ),( -2.992802 ,0 ,-3.098902 ),( -2.240181, 0, -2.859905 ),( -1.947866, 0, -2.029168 ),( -2.022896, 0 ,-0.986165 ),( -2.162509, 0, -0.255072 ),( -1.943975, 0, 0.0455116)))
    mc.move(2.899,0,0,footControlR)
    mc.xform(cp = True)
    mc.makeIdentity( footControlR, apply=True )
    mc.color(rgb = (1,1,1))
    global footControlRGRP
    footControlRGRP = mc.group(footControlR, n = "footControlRGRP")
    pos = mc.pointPosition(reverseFootR[2])
    mc.move(pos[0],0,0,footControlRGRP)
    pivLoc = mc.pointPosition(reverseFootR[0])
    mc.xform(footControlR, piv = (pivLoc[0], pivLoc[1] , pivLoc[2]), ws = True)
        
     
         ##Head Control
    global headControl
    headControl = mc.circle(c = (0,0,0), r = 4.25, nr = (0, 1, 1), n = "headControl1")
    mc.color(ud = 2)
    global headControlGRP
    headControlGRP = mc.group(headControl, n = "headControlGRP1")
    pos = mc.pointPosition(spineJoints[7])
    mc.move(pos[0],pos[1],pos[2] + 1, headControlGRP)
    mc.rotate(-20,0,0,headControlGRP)
    mc.makeIdentity(headControlGRP, apply = True)
    
          
        
        #back Control
    global backControl
    backControl = mc.curve(d=1, n = "backControl1", p=[(-0.5, 0, 0),(-0.5, 0, 2),(-2, 0, 2),(0, 0, 4),(2, 0, 2),(0.5, 0, 2),(0.5, 0, 0),(0.5, 0, -2),(2, 0, -2),(0, 0, -4),(-2, 0, -2),(-0.5, 0, -2),(-0.5, 0, 0)]);
    mc.color(ud = 2)
    mc.rotate(0,0,90, backControl)
    mc.scale(1.5,1.5,1.5, backControl)
    mc.makeIdentity(backControl, apply = True)
    global backControlGRP
    backControlGRP = mc.group(backControl, n = "backControl1GRP")
    pos = mc.pointPosition(spineJoints[5])
    mc.move(pos[0],pos[1],pos[2] - 10, backControlGRP)
        
        
        #hip sway
    global hipSwayControl
    hipSwayControl = mc.curve(d=1, n = "hipSwayControl1", p=[(-0.5, 0, 0),(-0.5, 0, 2),(-2, 0, 2),(0, 0, 4),(2, 0, 2),(0.5, 0, 2),(0.5, 0, 0),(0.5, 0, -2),(2, 0, -2),(0, 0, -4),(-2, 0, -2),(-0.5, 0, -2),(-0.5, 0, 0)]);
    mc.color(ud = 2)
    mc.rotate(0,90,0, hipSwayControl)
    mc.scale(1.5,1.5,1.5, hipSwayControl)
    mc.makeIdentity(hipSwayControl, apply = True)
    global hipSwayControlGRP
    hipSwayControlGRP = mc.group(hipSwayControl, n = "hipSwayControl1GRP")
    pos = mc.pointPosition(spineJoints[0])
    mc.move(pos[0],pos[1] + 2 ,pos[2] - 1 , hipSwayControlGRP)
    
       
       #abs
    global abscontrol
    abscontrol = mc.curve(d = 3, n = "abscontrol1", p = (( -0.800913, 0, 7.056141 ),( -0.265406, 0, 7.325259 ),( 0.31672, 0, 7.381502 ),( 0.764173, 0, 7.27759 ),( 1.183554, 0, 7.139143 ),( 1.516483, 0, 6.925935 ),( 1.76147, 0, 6.690399 ),( 2.254724, 0, 6.334697 ),( 2.57931 ,0, 5.947814 ),( 3.076661, 0, 5.483984 ),( 3.227577, 0, 4.977719 ),( 3.300189, 0, 4.332524 ),( 3.156193, 0, 4.004192 ),( 2.940126, 0, 3.544301 ),( 2.459935, 0, 2.906238 ),( 1.896194, 0, 2.722403, ),( 1.173682, 0, 2.752672 ),( 0.684217, 0 ,2.91142 ),( 0.359928, 0, 3.021365 ),( -0.212499, 0, 2.901779 ),( -0.970966 ,0, 2.743327 ),( -1.336932, 0, 2.71509 ),( -2.105246, 0, 2.809993 ),( -2.53423 ,0, 3.129236 ),( -2.848996, 0, 3.602111 ),( -3.083789, 0,4.152694 ),( -3.072619 ,0 ,4.767065 ),( -2.864968, 0, 5.335299 ),( -2.460608 ,0, 5.822106 ),( -2.017293, 0, 6.187691 ),( -1.388328 ,0, 6.681923 ),( -0.803558, 0, 7.068739)))
    mc.color(ud = 2)
    mc.move(0,0,-5,abscontrol)
    mc.xform(abscontrol, cp = True)
    mc.makeIdentity(abscontrol, apply = True)
    global abscontrolGRP
    abscontrolGRP = mc.group(abscontrol, n = "abscontrol1GRP") 
    pos = mc.pointPosition(spineJoints[1])
    mc.move(pos[0],pos[1] + 2 ,pos[2] , abscontrolGRP)
        
    
        #chest control
    global chestControl
    chestControl = mc.curve(d = 1, n = "chestControl1", p = ((1.308362, 42.005806,-0.0656287 ),( 4.160191 ,39.377197, 0.987189 ),( 3.880039, 39.364937 ,-4.688682 ),( 1.153233, 42.340385 ,-3.206603 ),( 1.308362 ,42.005806 ,-0.0656287 ),( -1.146977 ,41.999775, 0.132541 ),( -3.87119, 39.357468, 1.6354 ),( 4.160191 ,39.377197, 0.987189 ),( 1.308362, 42.005806, -0.0656287 ),( -1.146977 ,41.999775, 0.132541 ),( -1.302106 ,42.334351, -3.008433 ),( 1.153233, 42.340385, -3.206603 ),( 3.880039 ,39.364937 ,-4.688682 ),( -4.151342, 39.345207, -4.040471 ),( -1.302106, 42.334351, -3.008433 ),( -1.146977, 41.999775, 0.132541 ),( -3.87119 ,39.357468, 1.6354 ),( -4.151342, 39.345207, -4.040471 ),( 3.880039 ,39.364937, -4.688682 ),( 4.160191, 39.377197, 0.987189 ),( -3.87119, 39.357468 ,1.6354 ),( -1.363567, 33.493797, 0.483978 ),( 1.562515, 33.500984 ,0.247815 ),( 4.160191, 39.377197, 0.987189 ),( 3.880039, 39.364937 ,-4.688682 ),( 1.377832, 33.492905, -3.49385 ),( 1.562515 ,33.500984 ,0.247815 ),( -1.363567, 33.493797 ,0.483978 ),( -3.87119, 39.357468, 1.6354 ),( -4.151342, 39.345207 ,-4.040471 ),( -1.54825, 33.485714 ,-3.257687 ),( -1.363567 ,33.493797, 0.483978 ),( 1.562515, 33.500984 ,0.247815 ),( 1.377832 ,33.492905 ,-3.49385 ),( -1.54825, 33.485714, -3.257687 ),( -4.151342, 39.345207, -4.040471 ),( 3.880039, 39.364937, -4.688682 ),( 1.377832, 33.492905, -3.49385)))
    mc.color(ud = 2)
    mc.move(0,-40,0,chestControl)
    mc.xform(chestControl, cp = True)
    mc.makeIdentity(chestControl, apply = True)
    global chestControlGRP
    chestControlGRP = mc.group(chestControl, n = "chestControl1GRP")
    pos = mc.pointPosition(spineJoints[4])
    mc.move(pos[0],pos[1] + 3 ,pos[2] + 2 , chestControlGRP)
    
    
    #pelvis control
    global pelvisControl
    pelvisControl = mc.curve(d = 1, n = "pelvisControl1", p = (( 1.687394, 31.104399, 0.844462 ),( -2.107084, 31.088993, 1.042498 ),( -2.305122, 31.088993 ,-2.752012 ),( 1.489357, 31.104399, -2.950047 ),( 1.687394, 31.104399, 0.844462 ),( 4.509414, 28.431793, 0.772943 ),( 4.248509, 28.431793, -3.001678 ),( 1.489357, 31.104399, -2.950047 ),( -2.305122, 31.088993, -2.752012 ),( -5.098434, 28.391262, -2.68199 ),( -4.837529, 28.391262, 1.09263 ),( -2.107084, 31.088993, 1.042498 ),( -2.305122, 31.088993, -2.752012 ),( -5.098434, 28.391262 ,-2.68199 ),( 4.248509, 28.431793, -3.001678 ),( 4.509414, 28.431793, 0.772943 ),( -4.837529, 28.391262, 1.09263 ),( -2.081861, 26.484615, 1.041182 ),( 1.712618, 26.500021, 0.843146 ),( 4.509414, 28.431793, 0.772943 ),( 4.248509, 28.431793, -3.001678 ),( 1.51458, 26.500021 ,-2.951364 ),( -2.279898, 26.484615, -2.753328 ),( -5.098434 ,28.391262 ,-2.68199 ),( -4.837529, 28.391262 ,1.09263 ),( -2.081861 ,26.484615, 1.041182 ),( -2.279898, 26.484615, -2.753328 ),( 1.51458, 26.500021, -2.951364 ),( 1.712618 ,26.500021 ,0.843146 ),( -2.081861, 26.484615 ,1.041182)))
    mc.color(ud = 2)
    mc.move(0,-30,0,pelvisControl)
    mc.xform(pelvisControl, cp = True)
    mc.makeIdentity(pelvisControl, apply = True)
    global pelvisControlGRP
    pelvisControlGRP = mc.group(pelvisControl, n = "pelvisControl1GRP")
    pos = mc.pointPosition(spineJoints[1])
    mc.move(pos[0],pos[1] ,pos[2] + 1, pelvisControlGRP)
    
    
    mc.disable(placeControlsBtn, v=True)
    mc.disable(autorigbtn, v=False)


    
    
        
        
        
        

def createAndPlaceControls():
    mc.select(clear= True)
    mc.orientConstraint(shoulderLControl, AJL[0])
    mc.pointConstraint(AJL[0], shoulderLControl)

    mc.orientConstraint(elbowLControl, AJL[1])
    mc.pointConstraint(AJL[1], elbowLControl)
    #parent elbow group to shoulder so it doesn't bend weirdly
    mc.parent(elbowLControlGRP,shoulderLControl)

    mc.orientConstraint(wristLControl, AJL[2])
    mc.pointConstraint(AJL[2], wristLControl)
    mc.parentConstraint(elbowLControl,wristLControlGRP)
    mc.pointConstraint(armControlL, ikarmL[0])

   
    ##Position right arm Controls / Constrain Orientation/rotation

    mc.orientConstraint(shoulderRControl, AJR[0])
    mc.pointConstraint(AJR[0], shoulderRControl)

    mc.orientConstraint(elbowRControl, AJR[1])
    mc.pointConstraint(AJR[1], elbowRControl)
    #parent elbow group to shoulder so it doesn't bend weirdly
    mc.parent(elbowRControlGRP,shoulderRControl)

    mc.orientConstraint(wristRControl, AJR[2])
    mc.pointConstraint(AJR[2], wristRControl)
    mc.parentConstraint(elbowRControl,wristRControlGRP)

    mc.pointConstraint(armControlR, ikarmR[0])
    

    mc.select(clear = True)
    mc.poleVectorConstraint(PoleVectorControlElbowL, ikarmL[0])
    mc.poleVectorConstraint(PoleVectorControlElbowR, ikarmR[0])
    mc.poleVectorConstraint(PoleVectorControlKneeL, iklegL[0])
    mc.poleVectorConstraint(PoleVectorControlKneeR, iklegR[0])
    
    #Reverse Foot
    mc.parent(iklegL[0],RFL[3])
    mc.parent(iklegR[0],RFR[3])
    mc.parent(ikankleL[0],RFL[2])
    mc.parent(ikankleR[0],RFR[2])
    mc.parent(iktoeL[0],RFL[1])   
    mc.parent(iktoeR[0],RFR[1]) 
      
    
    mc.parentConstraint(footControlL, RFL[0])
    mc.parentConstraint(footControlR, RFR[0])
 

    mc.pointConstraint( headControl, ikneck[0], maintainOffset= True)
    mc.orientConstraint( headControl, SJ[7], maintainOffset= True)
      

    #Make and position global control
    globalControl = mc.circle(c = (0,0,0), r = 20, s = 16, nr = (0, 1, 0), n = "globalControl")
    mc.color(ud = 2)
    numSections = int(mc.circle(globalControl, q = True, s = True))
    mc.select(clear = True)
    for i in range(0, numSections, 2):
       vtxName = globalControl[0]+".cv[%d]"%i
       print vtxName
       mc.select(vtxName)
       mc.scale(.25,.25,.25)


    #mainpulate controls
    mc.pointConstraint(backControl, clusters[3], maintainOffset = True)
    mc.pointConstraint(chestControl, clusters[2], maintainOffset = True)
    mc.pointConstraint(abscontrol, clusters[1], maintainOffset = True)
    mc.pointConstraint(hipSwayControl, clusters[0], maintainOffset = True)
    
    mc.select(clear = True)
    grpNames = []
    for i in clusters:
        x = mc.group(i)
        mc.parent(x, SJ[0])
        grpNames.append(x)
    mc.rename(grpNames[3], "BackClusterGRP")
    mc.rename(grpNames[2], "ChestClusterGRP")
    mc.rename(grpNames[1], "AbsClusterGRP")
    mc.rename(grpNames[0], "HipSwayClusterGRP")

    #parent control groups to pelvis control/ setting up rest of spine
    mc.select(clear = True)
    mc.select(backControlGRP, add = True)
    mc.select(chestControlGRP, add = True)
    mc.select(abscontrolGRP, add = True)
    mc.select(hipSwayControlGRP, add = True)
    mc.parent(mc.ls(sl = True), pelvisControl)
    mc.parentConstraint(SJ[0], pelvisControlGRP, maintainOffset = True)

    mc.parent(headControlGRP,backControl)

    #group top layer ik's
    mc.select(clear = True)
    mc.select(ikneck[0], add = True)
    mc.select(ikSpineSpline[0], add = True)
    mc.select(ikarmL[0], add = True)
    mc.select(ikarmR[0], add = True)
    ikgrp = mc.group(mc.ls(sl=True), n = "IKGRP")

    #group controls
    mc.select(clear = True)
    mc.select(pelvisControlGRP, add = True)
    mc.select(shoulderLControlGRP, add = True)
    mc.select(shoulderRControlGRP, add = True)
    mc.select(wristLControlGRP, add = True)
    mc.select(wristRControlGRP, add = True)
    mc.select(armControlLGRP, add = True)
    mc.select(armControlRGRP, add = True)
    mc.select(PoleVectorControlElbowLGRP, add = True)
    mc.select(PoleVectorControlElbowRGRP, add = True)
    mc.select(PoleVectorControlKneeLGRP, add = True)
    mc.select(PoleVectorControlKneeRGRP, add = True)
    mc.select(footControlLGRP, add = True)
    mc.select(footControlRGRP, add = True)
    mc.select(RFL[0], add = True)
    mc.select(RFR[0], add = True)
    
    cntrlsgrp = mc.group(mc.ls(sl=True), n = "CONTROLSGRP")
    rootgrp = mc.group(SJ[0], n = "ROOTGRP")
    
    mc.parentConstraint(globalControl, rootgrp, maintainOffset = True)
    mc.scaleConstraint(globalControl, rootgrp, maintainOffset = True)
    mc.parentConstraint(globalControl, cntrlsgrp, maintainOffset = True)
    mc.scaleConstraint(globalControl, cntrlsgrp, maintainOffset = True)
    mc.parentConstraint(globalControl, ikgrp, maintainOffset = True)
    mc.scaleConstraint(globalControl, ikgrp, maintainOffset = True)
    
    mc.select(clear = True)
    mc.select(spline, add = True)
    mc.select(globalControl, add = True)
    mc.select(ikgrp, add = True)
    mc.select(cntrlsgrp, add = True)
    mc.select(rootgrp, add = True)
    mc.group(mc.ls(sl=True),n = "Character")
    

    
def connectJoints():
    mc.select(clear = True)
    mc.select(AJL[0], add = True)
    mc.select(AJR[0], add = True)
    mc.parent(mc.ls(sl=True),SJ[5])
    
    mc.select(clear = True)
    mc.select(LJL[0], add = True)
    mc.select(LJR[0], add = True)
    mc.parent(mc.ls(sl=True),SJ[1])
    
    


def deleteLocators():
    for i in spineJoints:
        mc.delete(i)
    for i in armJointsL:
        mc.delete(i)
    for i in armJointsR:
        mc.delete(i)    
    for i in legJointsL:
        mc.delete(i)
    for i in legJointsR:
        mc.delete(i)
    for i in reverseFootL:
        mc.delete(i)
    for i in reverseFootR:
        mc.delete(i)

