import cv2
import random
import numpy as np
import imutils
import speech_recognition as sr

objetos = {
"0":"Piedra",
        "1":"Uno",
        "2": "Tijera",
        "5":"Papel",
        "3":"tres",
        "4":"Papel",
"5":"Papel",
"6":"Papel",

    }
juego  = np.array([["Empate","no validdo","Ganado Jugador","no valida","Gana Computadora","Gana computadora","gana Computadora"],
                   ["no validdo","Empate","no validdo","no validdo","no validdo","no validdo","no validdo"],
                   ["Gana Comptutadora","no validdo","Empate","no valida","Gana Jugador","Gana Jugador","gana Jugador"],
                   ["no validdo","no validdo","no validdo","no validdo","no validdo","no validdo","no validdo"],
                   ["Gana Jugador","no validdo","Ganado Computadora","no valida","Empate","Empate","Empate"],
                   ["Gana Jugador","no validdo","Ganado Computadora","no valida","Empate","Empate","Empate"],
                   ["Gana Jugador","no validdo","Ganado Computadora","no valida","Empate","Empate","Empate"],])
cap =cv2.VideoCapture(0)

bg = None
foto = None
fingerGlobal = 0
texto = "vacio"

# COLORES PARA VISUALIZACIÓN
color_start = (204, 204, 0)
color_end = (204, 0, 204)
color_far = (255, 0, 0)

color_start_far = (204, 204, 0)
color_far_end = (204, 0, 204)
color_start_end = (0, 255, 255)

color_contorno = (0, 255, 0)
color_ymin = (0, 130, 255)  # Punto más alto del contorno
# color_angulo = (0,255,255)
# color_d = (0,255,255)
color_fingers = (0, 255, 255)

while True:
    ret, frame = cap.read()
    if ret == False: break

    # Redimensionar la imagen para que tenga un ancho de 640
    frame = imutils.resize(frame, width=640)
    frame = cv2.flip(frame, 1)
    frameAux = frame.copy()
    cv2.rectangle(frame, (50,40), (270, 310), color_contorno, 4)
    #cv2.rectangle(frame, (40, 50), (260, 300), color_contorno, 4)

    if bg is not None:

        # Determinar la región de interés
        fragmento = frame[40:310, 50:270]
        cv2.rectangle(frame, (50, 40 ), (270, 310), color_fingers, 4)#coordenadas invertidas
        grayFragmento = cv2.cvtColor(fragmento, cv2.COLOR_BGR2GRAY)

        # Región de interés del fondo de la imagen
        bgFragmento = bg[40:310, 50:270]

        # Determinar la imagen binaria (background vs foreground)
        dif = cv2.absdiff(grayFragmento, bgFragmento)
        th = cv2.threshold(dif, 40, 220, cv2.THRESH_BINARY)[1]
        th = cv2.medianBlur(th, 7)

        # Encontrando los contornos de la imagen binaria
        cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

        for cnt in cnts:

            # Encontrar el centro del contorno
            M = cv2.moments(cnt)
            if M["m00"] == 0: M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            cv2.circle(fragmento, tuple([x, y]), 5, (0, 255, 0), -1)

            # Punto más alto del contorno
            ymin = cnt.min(axis=1)
            cv2.circle(fragmento, tuple(ymin[0]), 5, color_ymin, -1)

            # Contorno encontrado a través de cv2.convexHull
            hull1 = cv2.convexHull(cnt)
            cv2.drawContours(fragmento, [hull1], 0, color_contorno, 2)

            # Defectos convexos
            hull2 = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hull2)

            # Seguimos con la condición si es que existen defectos convexos
            if defects is not None:

                inicio = []  # Contenedor en donde se almacenarán los puntos iniciales de los defectos convexos
                fin = []  # Contenedor en donde se almacenarán los puntos finales de los defectos convexos
                fingers = 0  # Contador para el número de dedos levantados

                for i in range(defects.shape[0]):

                    s, e, f, d = defects[i, 0]
                    start = cnt[s][0]
                    end = cnt[e][0]
                    far = cnt[f][0]

                    # Encontrar el triángulo asociado a cada defecto convexo para determinar ángulo
                    a = np.linalg.norm(far - end)
                    b = np.linalg.norm(far - start)
                    c = np.linalg.norm(start - end)

                    angulo = np.arccos((np.power(a, 2) + np.power(b, 2) - np.power(c, 2)) / (2 * a * b))
                    angulo = np.degrees(angulo)
                    angulo = int(angulo)

                    # Se descartarán los defectos convexos encontrados de acuerdo a la distnacia
                    # entre los puntos inicial, final y más alelago, por el ángulo y d
                    if np.linalg.norm(start - end) > 50 and angulo < 90 and d > 14000:
                        # Almacenamos todos los puntos iniciales y finales que han sido
                        # obtenidos
                        inicio.append(start)
                        fin.append(end)

                        # Visualización de distintos datos obtenidos
                        # cv2.putText(ROI,'{}'.format(angulo),tuple(far), 1, 1.5,color_angulo,2,cv2.LINE_AA)
                        # cv2.putText(ROI,'{}'.format(d),tuple(far), 1, 1.1,color_d,1,cv2.LINE_AA)
                        cv2.circle(fragmento, tuple(start), 5, color_start, 2)
                        cv2.circle(fragmento, tuple(end), 5, color_end, 2)
                        cv2.circle(fragmento, tuple(far), 7, color_far, -1)
                    # cv2.line(ROI,tuple(start),tuple(far),color_start_far,2)
                    # cv2.line(ROI,tuple(far),tuple(end),color_far_end,2)
                    # cv2.line(ROI,tuple(start),tuple(end),color_start_end,2)

                # Si no se han almacenado puntos de inicio (o fin), puede tratarse de
                # 0 dedos levantados o 1 dedo levantado
                if len(inicio) == 0:
                    minY = np.linalg.norm(ymin[0] - [x, y])
                    if minY >= 110:
                        fingers = fingers + 1
                        cv2.putText(fragmento, '{}'.format(fingers), tuple(ymin[0]), 1, 1.7, (color_fingers), 1, cv2.LINE_AA)

                # Si se han almacenado puntos de inicio, se contará el número de dedos levantados
                for i in range(len(inicio)):
                    fingers = fingers + 1
                    cv2.putText(fragmento, '{}'.format(fingers), tuple(inicio[i]), 1, 1.7, (color_fingers), 1, cv2.LINE_AA)
                    if i == len(inicio) - 1:
                        fingers = fingers + 1
                        cv2.putText(fragmento, '{}'.format(fingers), tuple(fin[i]), 1, 1.7, (color_fingers), 1, cv2.LINE_AA)
                fingerGlobal = fingers

                # Se visualiza el número de dedos levantados en el rectángulo izquierdo
                cv2.putText(frame, '{}'.format(fingers), (390, 45), 1, 4, (color_fingers), 2, cv2.LINE_AA)

        cv2.imshow('th', th)
    cv2.imshow('Frame', frame)

    k = cv2.waitKey(10)
    if k == ord('3'):
        print('entro 3')
        bg = cv2.cvtColor(frameAux, cv2.COLOR_BGR2GRAY)
        "intento asincrono"
        """def callback(recognizer, audio):  # this is called from the background thread
            try:
                texto = recognizer.recognize_google(audio, language='es')
                print("You said.... " +texto)
                # received audio data, now need to recognize it
                if 'tijera' in texto:
                    print('encontro a tijera')
                    print('entre al segundo if')
                    numRandom = random.randrange(0, 6, 2)

                    foto = frame[50:300, 380:600]
                    cv2.putText(foto, 'Jugador' + objetos[str(fingerGlobal)], (50, 50), 1, 1, color_contorno, 2)
                    cv2.putText(foto, 'Computadora' + objetos[str(numRandom)], (50, 90), 1, 1, color_contorno, 2)
                    cv2.putText(foto, juego[fingerGlobal, numRandom], (50, 120), 1, 1, color_contorno, 2)
                    cv2.imshow("Resultado", foto)
                    bg = None
            except:
                print("Oops! Didn't catch that")


        r = sr.Recognizer()
        m = sr.Microphone(0)
        r.listen_in_background(m, callback)
        print('salimos de mico')"""

        #tomo foto
    print(texto)
    if 'tijera' in texto:
        print('encontro a tijera')
        k='4'
    if k == ord('4'):
        numRandom = random.randrange(0,6,2)

        foto = frame[50:300, 380:600]
        cv2.putText(foto, 'Jugador'+objetos[str(fingerGlobal)], (50, 50), 1, 1, color_contorno, 2)
        cv2.putText(foto, 'Computadora'+objetos[str(numRandom)], (50, 90), 1, 1, color_contorno, 2)
        cv2.putText(foto, juego[fingerGlobal,numRandom], (50, 120), 1, 1, color_contorno, 2)
        cv2.imshow("Resultado", foto)
        bg = None
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()