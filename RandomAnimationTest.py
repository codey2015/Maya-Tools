import maya.cmds as cmds
import random


    #at 200 cubes go up
def playCoolStuff():

    xPos = 0
    xPos2 = 0
    zPos = 0
    zPos2 = 0
    yPos = 0
    yPosRot = 0
    yScale = 0
    memeScale = 0
    cmds.polyCube()
    
    cube1 = cmds.polyCube()
    cube2 = cmds.polyCube()
    cube3 = cmds.polyCube()
    cube4 = cmds.polyCube()
    
    cube5 = cmds.polyCube()
    cmds.move(-10,0,0)
    cube6 = cmds.polyCube()
    cmds.move(10,0,0)
    cube7 = cmds.polyCube()
    cmds.move(0,0,-10)
    cube8 = cmds.polyCube()
    cmds.move(0,0,10)

    meme = cmds.textCurves( f='Courier', t='Meme', o = True )
    cmds.move(-13, 0, 0, meme)
    #cmds.scale(1,1,1,meme,scaleXYZ = True)
    cmds.color( meme, rgb = (1,0,0))

    #sphere1 = cmds.polySphere()
    #cmds.hide(sphere1)
        
    startFrame = cmds.playbackOptions(q=True, minTime =True)
    endFrame = cmds.playbackOptions(q=True,maxTime=True)
    currentFrame=startFrame
    cubeList = [cube1, cube2, cube3, cube4, cube5,cube6,cube7,cube8]
    w=0
    curTime = cmds.currentTime(currentFrame)
    cmds.playbackOptions(loop = "continuous", ast = 2, aet = 500, min = 2)
    for x in range(100):
       #cmds.orbit(horizontalAngle = curTime)
       print currentFrame
       cmds.select(ado = True)
       tt=random.randint(-20,20)
       ty=random.randint(-20,20)
       tz=random.randint(-20,20)
       if w <= len(cubeList):
            cmds.polyColorPerVertex(cubeList[w], colorRGB=[tt*.035, ty*.005, tz*.016], colorDisplayOption = True)
            w+=1
       if w >= len(cubeList):
            w = 0
       cmds.setKeyframe(cube1,  attribute="translateX", value=xPos, t=x*10 )
        ##cmds.setKeyframe(cube1,  attribute="rotateY", value=xPos, t=x*2 )
       xPos-=1
       cmds.setKeyframe(cube2,  attribute="translateX", value=xPos2, t=x*10 )
       ## cmds.setKeyframe(cube2,  attribute="rotateY", value=xPos2, t=x*2 )
       xPos2+=1
       cmds.setKeyframe(cube3,  attribute="translateZ", value=zPos, t=x*10 )
       ## cmds.setKeyframe(cube3,  attribute="rotateY", value=zPos, t=x*2 )
       zPos-=1
       cmds.setKeyframe(cube4,  attribute="translateZ", value=zPos2, t=x*10 )
       ## cmds.setKeyframe(cube4,  attribute="rotateY", value=zPos2, t=x*2 )
       zPos2+=1
       cmds.setKeyframe(cube1, cube2, cube3, cube4, cube5, cube6, cube7, cube8,  attribute="rotateY", value=yPosRot, t=x*10 )
       cmds.setKeyframe(cube1, cube2, cube3, cube4, cube5, cube6, cube7, cube8,  attribute="scaleX", value=1, t=x*10 )
       cmds.setKeyframe(cube1, cube2, cube3, cube4, cube5, cube6, cube7, cube8,  attribute="scaleY", value=1, t=x*10 )
       cmds.setKeyframe(cube1, cube2, cube3, cube4, cube5, cube6, cube7, cube8,  attribute="scaleZ", value=1, t=x*10 )
       cmds.setKeyframe(meme,  attribute="scaleX", value=memeScale, t=x*10 )
       cmds.setKeyframe(meme,  attribute="scaleY", value=memeScale, t=x*10 )
       cmds.setKeyframe(meme,  attribute="scaleZ", value=memeScale, t=x*10 )

       currentFrame+=1

       if x in range(10, 20):
          cmds.polyColorPerVertex(cubeList[w], colorRGB=[tt*.005, ty*.035, tz*.026], colorDisplayOption = True)
          xPos+=2
            ##xPos+=xPos2
          xPos2-=2
            ##xPos2-=zPos
          zPos+=2
            ##zPos+=zPos2
          zPos2-=2
            ##zPos2-=x

       if x in range(20, 30):
          cmds.polyColorPerVertex( cubeList[w], colorRGB=[tt*.005, ty*.035, tz*.026], colorDisplayOption = True)
          xPos-=3
          xPos2+=3
          zPos-=3
          zPos2+=3

          cmds.setKeyframe(cube5, cube6, cube7, cube8,  attribute="translateY", value=yPos, t=x*10 )
          yPos+=2
          yPosRot+=15
          cmds.setKeyframe(cube5, cube6, cube7, cube8,  attribute="rotateY", value=yPosRot, t=x*10 )

       if x in range(30, 40):
          yPos-=4
          cmds.setKeyframe(cube5, cube6, cube7, cube8,  attribute="translateY", value=yPos, t=x*10 )
       if x in range(30, 40):
          yPosRot+=15
          cmds.setKeyframe(cube5, cube6, cube7, cube8,  attribute="translateY", value=yPos, t=x*10 )
       if x in range(40, 50):   
          yPos+=6
          yScale+=.65
          yPosRot+=15
          memeScale += 1
          cmds.setKeyframe(cube5, cube6, cube7, cube8,  attribute="translateY", value=yPos, t=x*10 )
          cmds.setKeyframe(cube1, cube2, cube3, cube4, cube5, cube6, cube7, cube8,  attribute="scaleX", value=yScale, t=x*10 )
          cmds.setKeyframe(cube1, cube2, cube3, cube4, cube5, cube6, cube7, cube8,  attribute="scaleY", value=yScale, t=x*10 )
          cmds.setKeyframe(cube1, cube2, cube3, cube4, cube5, cube6, cube7, cube8,  attribute="scaleZ", value=yScale, t=x*10 )
          cmds.setKeyframe(meme,  attribute="scaleX", value=memeScale, t=x*10 )
          cmds.setKeyframe(meme,  attribute="scaleY", value=memeScale, t=x*10 )
          cmds.setKeyframe(meme,  attribute="scaleZ", value=memeScale, t=x*10 )

    return




def waves():  
    cmds.playbackOptions(loop = "continuous", ast = 2, aet = 800, min = 2)
    g = -0.04
    v0y = 1.0
    v0x = 0.1
    pos0y = 5    
    pos0x = -10 
    temp = 0

    myList = []
    line = 1
    for i in range(100):
       tt=random.randint(-20,20)
       ty=random.randint(-20,20)
       tz=random.randint(-20,20)   
       tm=random.randint(-20,20)    
       x = cmds.polyCube()
       cmds.polyColorPerVertex( colorRGB=[tt*.015, ty*.025, tz*.026], colorDisplayOption = True)
       myList.append(x)

       if i in range(0, 10):
           line+=1
           cmds.setKeyframe( myList[temp], attribute="translateX", value=line, t =i*10 )
           cmds.move(line*2,0,-10, absolute = True)
       if i in range(10, 20):
           line+=1
           cmds.move(line*2,0,-8, absolute = True)
       if i in range(20, 30):           
           line+=1
           cmds.move(line*2,0,-6, absolute = True) 
       if i in range(30, 40):  
           line+=1
           cmds.move(line*2,0,-4, absolute = True)
       if i in range(40, 50):
           line+=1
           cmds.move(line*2,0,-2, absolute = True)       
       if i in range(50, 60):
           line+=1
           cmds.move(line*2,0,0, absolute = True)
       if i in range(60, 70):
           line+=1
           cmds.move(line*2,0,2, absolute = True)
       if i in range(70, 80):           
           line+=1
           cmds.move(line*2,0,4, absolute = True)
       if i in range(80, 90):  
           line+=1
           cmds.move(line*2,0,6, absolute = True)
       if i in range(90, 100):
           line+=1
           cmds.move(line*2,0,8, absolute = True)
          
      # listSize = len(myList)
       #temp+=1
      # if temp >= listSize:
           #temp = 0
           
       if line == 10:
            line = 0

    cmds.select(ado = True)
    cmds.move(-10,0,0, relative = True)   
    
    listSize = len(myList)
    for itr in xrange(0,20):
        for tx in xrange(0,42):
            tm=random.randint(-20,20)
            posy = pos0y + v0y*(tx-1) + g*(tx-1)*(tx-1)/2
            posx = pos0x + v0x*((itr*42) + tx-1)  
            cmds.setKeyframe( myList[temp], attribute="translateY", value=posy, t=(itr*42) + tx )
            #if tx in range(30,42):
                #cmds.setKeyframe(  myList[temp], attribute="translateX", value=posx, t=(itr*42) + tx )
            temp+=1
            if temp >= listSize:
                temp = 0
                
            #if tx in range(30,42):
                #cmds.setKeyframe( myList[temp], attribute="translateX", value=tm, t=tx )

    return
 
 
 
 
homeName = cmds.cameraView(camera='persp')
cmds.cameraView( homeName, e=True, camera='persp', ab=True )


cmds.play()
waves()
playCoolStuff()

cmds.cameraView( homeName, e=True, camera='persp', sc=True )



#just a short example that moves a cube for 120 'seconds'
cmds.polyCube()
cmds.setKeyframe( attribute="translateX", value=0, t = 94 )
for x in xrange(0,60):
    x+=1
    cmds.setKeyframe( attribute="translateX", value=x )
meme = cmds.textCurves( f='Courier', t='Meme', o = True )
cmds.scale(5,5,5,meme,scaleXYZ = True)
cmds.color( meme, rgb = (1,0,0))




