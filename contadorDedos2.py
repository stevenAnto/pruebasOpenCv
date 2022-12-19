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
foto = None
fingerGlobal = 0

while(captura.isOpened()):
    #devuelve un booleano y la image

    ret, image = captura.read()

    if ret==True:

        image =imutils.resize(image,width=600)# redimensione las capturas
        image = cv2.flip(image,1) #se invierte par ano tener confusion
        cv2.rectangle(image, (20, 20), (20 + 200, 20 + 300), color_contorno, 4)

        imageAux = image.copy()
        if bg is not None:
            fragmento = image[20:320,20:220]

            cv2.rectangle(image,(20,20),(20+200,20+300),color_fingers,1)
            grayFragmento = cv2.cvtColor(fragmento,cv2.COLOR_BGR2GRAY)

            bgFragmento = bg[20:320,20:220] #tomamos la porcion de la imagen
            #cv2.imshow("fragmento",fragmento)
            #cv2.imshow("grayFragmento", grayFragmento)
            #cv2.imshow("bgFragmento", bgFragmento)
            #aplicando umbralizacion para separar el fondo
            dif = cv2.absdiff(grayFragmento,bgFragmento)
            th =cv2.threshold(dif,30,255,cv2.THRESH_BINARY)[1]
            th = cv2.medianBlur(th, 7)#ajuste para mejor umbralizacion
            contornos = cv2.findContours(th, cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_SIMPLE)[0]
            contornos = sorted(contornos,key=cv2.contourArea,reverse=True)[:1]
            #cv2.drawContours(fragmento, contornos, 0, (0,255,0), 10)

            for cnt in contornos:

                # Encontrar el centro del contorno
                M = cv2.moments(cnt)
                if M["m00"] == 0: M["m00"] = 1
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])
                cv2.circle(fragmento, (x,y), 10, (0, 255, 0), -1)

                # Punto más alto del contorno
                ymin = cnt.min(axis=1)
                cv2.circle(fragmento, tuple(ymin[0]), 10, color_ymin, -1)

                #caso convexo
                hull = cv2.convexHull(cnt)
                cv2.drawContours(fragmento, [hull], 0, color_contorno, 1)

                hull2 = cv2.convexHull(cnt,returnPoints=False)
                defects = cv2.convexityDefects(cnt,hull2)#encuentro los desfectos del cascaron

                if defects is not None:
                    inicio = []
                    fin = []
                    fingers = 0

                    for i in range(defects.shape[0]):
                        s,e,f,d = defects[i,0]
                        start = cnt[s][0]
                        end = cnt[e][0]
                        far = cnt[f][0]

                        #traingulo
                        a= np.linalg.norm(far-end)
                        b = np.linalg.norm(far - start)
                        c = np.linalg.norm(start - end)

                        angulo = np.arccos((np.power(a,2)+np.power(b,2)-np.power(c,2))/(2*a*b))
                        angulo = np.degrees(angulo)
                        angulo =int(angulo)

                        if np.linalg.norm(start-end)>20 and d>10000 and angulo<90:
                            inicio.append(start)
                            fin.append(end)
                            #cv2.putText(fragmento,'{}'.format(d),tuple(far),1,1,color_d,1,cv2.LINE_AA)
                            #cv2.putText(fragmento, '{}'.format(angulo), tuple(far), 1, 1, color_d, 1, cv2.LINE_AA)
                            cv2.circle(fragmento, tuple(start), 2, color_start, 2)
                            cv2.circle(fragmento, tuple(end), 2, color_end, 2)
                            cv2.circle(fragmento, tuple(far), 2, color_far, -1)
                    if len(inicio)==0:
                        minY = np.linalg.norm(ymin[0]-[x,y])
                        cv2.putText(fragmento, '{}'.format(minY), (50,50), 1, 1, color_fingers, 1,cv2.LINE_AA)
                        if minY >= 80:
                            fingers = fingers+1
                            cv2.putText(fragmento, '{}'.format(fingers), tuple(ymin[0]), 1, 1, color_fingers, 1, cv2.LINE_AA)

                    for i in range(len(inicio)):
                        fingers = fingers+1
                        cv2.putText(fragmento, '{}'.format(fingers), tuple(inicio[i]), 1, 1, color_fingers, 1, cv2.LINE_AA)
                fingerGlobal=fingers




            #cv2.imshow("dif",dif)
            cv2.imshow("th",th)
            cv2.imshow("foto", foto)

        cv2.imshow('video', image)

        k = cv2.waitKey(5)
        if k == ord('3'):
            bg = cv2.cvtColor(imageAux,cv2.COLOR_BGR2GRAY)
        if k == ord('4'):
            bg =None
            foto = image[20:320,20:220]
            if fingerGlobal<2:
                cv2.putText(foto, 'piedra', (50, 50), 1, 1, color_contorno, 2)
            elif fingerGlobal==2:
                cv2.putText(foto, 'tijera', (50, 50), 1, 1, color_contorno, 2)
            elif fingerGlobal==3:
                cv2.putText(foto, 'Es un tres, no valid', (50, 50), 4, 2, color_contorno, 2)
            elif fingerGlobal>=4:
                cv2.putText(foto, 'Papel', (50, 50), 1, 1, color_contorno, 2)


        if k & 0xFF==ord('d'):
            break
captura.release()
cv2.destroyAllWindows()