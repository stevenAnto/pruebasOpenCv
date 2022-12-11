import cv2
import numpy as np

objetos = {
"0":"Piedra",
        "1":"Uno",
        "2": "Tijera",
        "5":"Papel",
        "3":"tres",
        "4":"Papel",
"5":"Papel",
"6":"seis",
"7":"siete",
"8":"ocho",

    }

def dibujar(mask,color):

    contornos = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)[0]
    contador=0
    #bota muchos contornos porque tambien cuenta a los pequenos, solo nos interesa los que tiene una area prudente
    print("cuantos contornos",len(contornos))
    for (i,c) in enumerate(contornos):

        area = cv2.contourArea(c)

        if area > 3000:
            # Buscamos el centro
            M = cv2.moments(c)
            if (M["m00"] == 0): M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(frame, objetos[str(contador)], (x+10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)

            nuevoContorno = cv2.convexHull(c)

            # se pone 0 solo para dibujar ciertos contornos
            cv2.drawContours(frame, [nuevoContorno], 0, color, 4)
            contador = contador + 1
    #cv2.putText(frame, '{},{},{}'.format(x, y, str(i + 1)), (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
    #cv2.putText(frame, objetos[str(contador)], (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
    font = cv2.FONT_HERSHEY_SIMPLEX

    #cv2.putText(frame, objetos[str(contador)], (100, 100), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)

    print(contador)
    print(objetos[str(contador)])
    return contador



    #print(objetos[contadorGlobal])

cap = cv2.VideoCapture(0)
#Sacado de StackOverFlow
azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)

amarilloBajo = np.array([15,100,20],np.uint8)
amarilloAlto = np.array([45,255,255],np.uint8)

redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([5,255,255],np.uint8)

redBajo2 = np.array([0,100,20],np.uint8)
redAlto2 = np.array([5,255,255],np.uint8)

font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, frame = cap.read()
    if ret == True:
        #cambiamos a espacio HSV
        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        maskAzul = cv2.inRange(frameHSV,azulBajo,azulAlto)
        maskAmarillo = cv2.inRange(frameHSV, amarilloBajo, amarilloAlto)
        maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)
        maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)
        maskRed = cv2.add(maskRed1,maskRed2)

        dibujar(maskAmarillo,(0,255,255))
        dibujar(maskRed,(0,0,255))
        contadorD =dibujar(maskAzul,(255,0,0))
        cv2.putText(frame, objetos[str(contadorD)], (150, 150), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('d'):
            break
cap.release()
cv2.destroyAllWindows()