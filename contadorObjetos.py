import cv2
import numpy as np

amarilloBajo = np.array([15,100,20],np.uint8)
amarilloAlto = np.array([45,255,255],np.uint8)
verdeBajo = np.array([36,100,20],np.uint8)
verdeAlto = np.array([70,255,255],np.uint8)
redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([5,255,255],np.uint8)

redBajo2 = np.array([0,100,20],np.uint8)
redAlto2 = np.array([5,255,255],np.uint8)

image = cv2.imread('Gotass.jpg')

imagenHSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
#Encontrando colores
maskAmarillo = cv2.inRange(imagenHSV, amarilloBajo, amarilloAlto)
maskVerder = cv2.inRange(imagenHSV, verdeBajo, verdeAlto)
maskRed1 = cv2.inRange(imagenHSV, redBajo1, redAlto1)
maskRed2 = cv2.inRange(imagenHSV, redBajo2, redAlto2)
maskRed = cv2.add(maskRed1,maskRed2)
#Encontrar contornos

contornosAmarillo = cv2.findContours(maskAmarillo,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
cv2.drawContours(image,contornosAmarillo,1,(0,255,255),5)

cv2.imshow('maskAmarillo',maskAmarillo)
#cv2.imshow('imagen', imagenHSV)
cv2.imshow('imagen original',image)
cv2.waitKey(0)
cv2.destroyAllWindows()