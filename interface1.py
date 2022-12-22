from  tkinter import *
import cv2
import imutils
from PIL import Image
from PIL import ImageTk
import numpy as np
import speech_recognition as sr

root = Tk()
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


def visualizar():
    global  cap
    if cap is not None:
        ret,frame = cap.read()
        if ret== True:
            frame = imutils.resize(frame,width=640)
            frame = cv2.flip(frame, 1)
            frameAux = frame.copy()
            cv2.rectangle(frame, (50, 40), (270, 310), color_contorno, 4)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image =img
            lblVideo.after(10,visualizar)#Esto hace el ciclo para que se siga visualizando, es como recursivo
        else:
            lblVideo.image=""
            cap.release()

def iniciar():
    global cap
    cap = cv2.VideoCapture(0)
    visualizar()
def terminar():
    global cap
    global root
    cap.release()
    lblVideo.configure(image=imagenDedos)
    lblVideo.image=imagenDedos

    print('termino terminar')

cap = None


btnComenzar = Button(root,text="Comenzar a Jugar", command=iniciar)
btnComenzar.grid(column=0,row=0,padx=10,pady=10)

btnFinalizar = Button(root,text="Finalizar",command=terminar)
btnFinalizar.grid(column=1,row=0,padx=10,pady=10)

imagenDedos = PhotoImage(file='iconoJego.png')
lblVideo = Label(root,image=imagenDedos)
lblVideo.grid(column=0,row=1,columnspan=2)

root.mainloop()


