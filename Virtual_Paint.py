#Virtual Paint
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10,150)
imgCanvas = np.zeros((480,640,3),np.uint8)

##hmin, smin, vmin hmax, smax, vmax

myColors = [[17,90,0,31,254,255],[76,97,105,96,230,255],[146,92,0,176,255,255]]
myColorValues = [[0,255,255],[28,171,28],[0,0,0]]  #BGR #red,yellow,green,pink
 
myPoints =  []  ## [x , y , colorId ]
 
def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        #...............
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),15,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
        #cv2.imshow(str(color[0]),mask)
    return newPoints
 
def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>800:
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.drawContours(imgResult, cnt, -1, (0, 255, 0), 3)
            img = cv2.rectangle(imgResult,(x,y),(x+y,y+h),(125,10,20),5)
            #epsilon  = 0.1*cv2.arcLength(cnt,True)
            #data = cv2.approxPolyDP(cnt,epsilon,True)


            
            
           # hull = cv2.convexHull(data)           

    return x+w//2,y
 
def drawOnCanvas(myPoints,myColorValues):
    xp= 0
    yp= 0
    if xp == 0 and yp ==0:
        xp,yp = myPoints[0][0], myPoints[0][1]
    for point in myPoints:
        if myColorValues[point[2]] == [0,0,0]:
            print(myColorValues[point[2]])
            #cv2.circle(imgCanvas,(point[0], point[1]),20,myColorValues[point[2]],20)
            cv2.circle(imgCanvas, (point[0], point[1]), 20, myColorValues[point[2]], cv2.FILLED)

        
 
        #cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)
        #cv2.line(imgResult,(xp,yp),(point[0], point[1]),myColorValues[point[2]],5,8,0)
        cv2.line(imgCanvas,(xp,yp),(point[0], point[1]),myColorValues[point[2]],5)
        xp,yp = point[0],point[1]
    
 
 
while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
 
 
    #cv2.imshow("Result", imgResult)
    #cv2.imshow("canvas", imgCanvas)
    imgwait = cv2.addWeighted(imgResult,0.5,imgCanvas,0.5,0)
    imgwait = cv2.flip(imgwait,1)
    cv2.imshow("final", imgwait)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break