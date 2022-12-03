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
        cv2.imshow( 'diff',dif)
    cv2.imshow('Frame',frame)
    i=i+1
    if cv2.waitKey(1) & 0XFF ==ord('d'):
        break
video.release()