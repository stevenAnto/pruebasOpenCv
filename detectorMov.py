import cv2
import numpy as np

video = cv2.VideoCapture(0)
i=0
while True:
    ret, frame = video.read()
    if ret == False: break
    #cambiamos a escal de grises
    gray =  cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #En el frame 20 capturamos
    if i == 20:
        #capturamos el background
        bgGray = gray
    if i> 20:
        dif =cv2 .absdiff(gray,bgGray)
        #cambiamos a imagene binaria, mediante umbralizacion
        sinUsar,th = cv2.threshold(dif,40,255,cv2.THRESH_BINARY)
        contornos = cv2.findContours(th, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
        #cv2.drawContours(frame,contornos,-1,(0,0,255),2)
        #cv2.imshow( 'diff',dif)
        cv2.imshow('th', th)
        #dibujamos rectangulos en los contorndos encontrados
        for c in contornos:
            area =cv2.contourArea(c)
            if area >7000:
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('Frame',frame)
    i=i+1
    if cv2.waitKey(1) & 0XFF ==ord('d'):
        break
video.release()