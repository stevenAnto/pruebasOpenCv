import cv2
import numpy as np
#Tienen que estar separados los objetos de colores
amarilloBajo = np.array([15,100,20],np.uint8)
amarilloAlto = np.array([45,255,255],np.uint8)
verdeBajo = np.array([36,100,20],np.uint8)
verdeAlto = np.array([70,255,255],np.uint8)
redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([5,255,255],np.uint8)

redBajo2 = np.array([0,100,20],np.uint8)
redAlto2 = np.array([5,255,255],np.uint8)

image = cv2.imread('lunares.png')

imagenHSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
#Encontrando colores
maskAmarillo = cv2.inRange(imagenHSV, amarilloBajo, amarilloAlto)
maskVerder = cv2.inRange(imagenHSV, verdeBajo, verdeAlto)
maskRed1 = cv2.inRange(imagenHSV, redBajo1, redAlto1)
maskRed2 = cv2.inRange(imagenHSV, redBajo2, redAlto2)
maskRed = cv2.add(maskRed1,maskRed2)
#Encontrar contornos

ContadorGlobal=0
objetos = {
        "1":"Piedra",
        "2": "Tijera",
        "5":"Papel",
        "3":"tres",
        "4":"cuatro"
    }
contadorGlobal=0
def dibujarContorno(contorno, color):

    for (i,c) in enumerate(contorno):
        M = cv2.moments(c)
        if(M["m00"]==0): M["m00"]=1
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        cv2.drawContours(image, [c], 0, color, 5)
        cv2.putText(image,str(i+1),(x+10,y+10),1,2,(0,0,0),2)
        contadorGlobal=str(i+1)
    print(contadorGlobal)
    print(objetos[contadorGlobal])
    #cv2.putText(image,objetos[contadorGlobal],(10,10),1,2,(0,0,0),2)



contornosAmarillo = cv2.findContours(maskAmarillo,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
#print(contornosAmarillo)
#print(type(contornosAmarillo))
contornosVede = cv2.findContours(maskVerder,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
contornosRojo = cv2.findContours(maskRed,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]

dibujarContorno(contornosAmarillo,(0,255,255))
dibujarContorno(contornosVede,(0,255,0))
dibujarContorno(contornosRojo,(0,0,255))


cv2.imshow('maskAmarillo',maskAmarillo)
#cv2.imshow('imagen', imagenHSV)
cv2.imshow('imagen original',image)
cv2.waitKey(0)
cv2.destroyAllWindows()