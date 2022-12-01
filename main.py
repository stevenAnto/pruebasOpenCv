import cv2
captura =cv2.VideoCapture(0)

while(captura.isOpened()):
    #devuelve un booleano y la image
    ret, image = captura.read()
    if ret==True:
        cv2.imshow('video',image)
        if cv2.waitKey(1) & 0xFF==ord('d'):
            break
captura.release()
cv2.destroyAllWindows()




