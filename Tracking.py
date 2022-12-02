import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#Sacado de StackOverFlow
azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)


while True:
    ret, frame = cap.read()
    if ret == True:
        #cambiamos a espacio HSV
        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frameHSV,azulBajo,azulAlto)
        contornos,sinUso, = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        for c in contornos:
            area = cv2.contourArea(c)
            if area > 3000:
                #se pone 0 solo para dibujar ciertos contornos
                cv2.drawContours(frame,[c],0,(255,0,0),3)

        #cv2.drawContours(frame,a,-1,(255,0,0),3)# Dibjuamos los contornos en frame con -1 se bijutan todos los contoros, en azul con grosor 3
        #cv2.imshow('maskAzul',mask)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('d'):
            break
cap.release()
cv2.destroyAllWindows()