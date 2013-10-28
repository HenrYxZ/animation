from cv2 import *
import sys
import numpy as np

namedWindow("preview")
vc = VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    imshow("preview", frame)
    bw = inRange(frame, np.array((0.,0.,80.)), np.array((60.,60.,255.)))
    # np.array((0.,0.,110.)), np.array((53.,53.,255.))
    namedWindow('input')
    imshow('input',bw)
    rval, frame = vc.read()
    key = waitKey(20)
    if key == 27: # exit on ESC
        break