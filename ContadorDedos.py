import cv2
import numpy as np
import imutils


captura =cv2.VideoCapture(0)

color_start = (204,204,0)
color_end = (204,0,204)
color_far = (255,0,0)

color_start_far = (204,204,0)
color_far_end = (204,0,204)
color_start_end = (0,255,255)

color_contorno = (0,255,0)
color_ymin = (0,130,255) # Punto más alto del contorno
color_angulo = (0,255,255)
color_d = (0,255,255)
color_fingers = (0,255,255)

bg = None

while(captura.isOpened()):
    #devuelve un booleano y la image
    ret, image = captura.read()
    if ret==True:

        image =imutils.resize(image,width=600)# redimensione las capturas
        image = cv2.flip(image,1) #se invierte par ano tener confusion

        imageAux = image.copy()
        if bg is not None:
            fragmento = image[20:320,20:220]

            cv2.rectangle(image,(20,20),(20+200,20+300),color_fingers,4)
            grayFragmento = cv2.cvtColor(fragmento,cv2.COLOR_BGR2GRAY)

            bgFragmento = bg[20:320,20:220] #tomamos la porcion de la imagen
            #cv2.imshow("fragmento",fragmento)
            #cv2.imshow("grayFragmento", grayFragmento)
            #cv2.imshow("bgFragmento", bgFragmento)
            #aplicando umbralizacion para separar el fondo
            dif = cv2.absdiff(grayFragmento,bgFragmento)
            th =cv2.threshold(dif,30,255,cv2.THRESH_BINARY)[1]
            cv2.imshow("dif",dif)
            cv2.imshow("th",th)

        cv2.imshow('video', image)

        k = cv2.waitKey(5)
        if k == ord('i'):
            bg = cv2.cvtColor(imageAux,cv2.COLOR_BGR2GRAY)
        if k & 0xFF==ord('d'):
            break
captura.release()
cv2.destroyAllWindows()