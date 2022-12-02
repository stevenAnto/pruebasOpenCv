import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#Sacado de StackOverFlow
redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([8,255,255],np.uint8)


redBajo2 = np.array([175,100,20],np.uint8)
redalto2 = np.array([179,255,255],np.uint8)

while True:
    ret, frame = cap.read()
    if ret == True:
        #cambiamos a espacio HSV
        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
        maskRed2 = cv2.inRange(frameHSV,redBajo2,redalto2)
        maskRed =cv2.add(maskRed1,maskRed2)
        #lo muestro en el color que se subad
        maskRedvisua = cv2.bitwise_and(frame,frame,mask=maskRed)
        cv2.imshow('MaskRedVisuali',maskRedvisua)
        cv2.imshow('MaskREd',maskRed)
        cv2.imshow('frame',frameHSV)
        if cv2.waitKey(1) & 0xFF == ord('d'):
            break
cap.release()
cv2.destroyAllWindows()