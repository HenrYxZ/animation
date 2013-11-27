import cv2
import numpy as np


def find_points(frame):
    # los suavizo
    frame = cv2.blur(frame,(3,3))

    # convierto a  hsv y especifico el rango de color
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # azul
    # np.array((104, 178, 70)), np.array((130, 240, 124))
    # blanco np.array((0, 0, 166)), np.array((180, 53, 255))
    # rojo 
    t = cv2.inRange(hsv,np.array((160, 128, 104)), np.array((179, 255, 255)))
    t2 = t.copy()
    points = []

    # encuentro los contornos
    contours,hierarchy = cv2.findContours(t,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # encuentro el contorno con el area mas grande y lo guardo en best_cnt
    max_area = 0
    best_cnt=0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 40:
            max_area = area
            best_cnt = cnt
          # encuentro los centroides best_cnt y hago un circulo
        M = cv2.moments(best_cnt)
        if(M['m00']!=0):
            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            cv2.circle(frame,(cx,cy),5,255,-1)
            # OJO : quizas sea necesario pasarlo a float
            points.append(np.array((cx, cy)))

    # Lo muestro
    frame_name = 'frame '
    cv2.imshow(frame_name,frame)
    cv2.imshow('Color',t2)
    return points

# inicio el stream de video
cap = cv2.VideoCapture(0)
counter = 1
while(1):

    # leo los frames
    _,frame = cap.read()
    if not _:
        print "NO hay imagen"
        break

    find_points(frame)
    counter += 1

    if cv2.waitKey(33)== 27:
        break

# limpio antes de irme
cv2.destroyAllWindows()
cap.release()
