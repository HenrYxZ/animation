import cv2
import numpy as np
import sys, getopt
from glob import glob

args, img_mask = getopt.getopt(sys.argv[1:], '', ['save=', 'debug=', 'square_size='])
args = dict(args)
try: img_mask = img_mask[0]
except: img_mask = 'frame1/00*.jpg'
img_names = glob(img_mask)

# inicio el stream de video
vc = cv2.VideoCapture(0)
i=0
#for fn in img_names:
while True:

    # leo los frames
    #frame = cv2.imread(fn)
    f, frame = vc.read()

    # los suavizo
    frame = cv2.blur(frame,(3,3))

    # convierto a  hsv y especifico el rango de color
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    t = cv2.inRange(hsv,np.array((0, 150, 0)), np.array((5, 255, 255)))
    t2 = t.copy()

    # encuentro los contornos
    contours,hierarchy = cv2.findContours(t,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # encuentro el contorno con el area mas grande y lo guardo en best_cnt
    max_area = 0
    best_cnt=0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    # encuentro los centroides best_cnt y hago un circulo
    M = cv2.moments(best_cnt)
    if(M['m00']!=0):
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        cv2.circle(frame,(cx,cy),5,255,-1)

    # Lo muestro
    cv2.imshow('frame',frame)
    cv2.imshow('Color',t2)
    cv2.imwrite('seg1/{0:05d}.jpg'.format(i),t2)
    i += 1
    cv2.waitKey(33)== 27
    

# limpio antes de irme
cv2.destroyAllWindows()
