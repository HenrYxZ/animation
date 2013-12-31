'''
GUI for showing the 3D points with OpenGL

Created on December 25 2013
@author: Hernaldo Henriquez
'''
SCREEN_SIZE = (800, 600)

from geom import Vector3
from geom import BoundingBox
from geom import projection
from drawing_helper import drawAxis
from drawing_helper import drawRect
from parser import parse
import sys
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

previous_time = 0
current_frame = 0

beginning_x = 0
beginning_y = 0

zSensitivity = 1
zoom = 0

# float speed for the animation
speed = 1
capture_frame_time = 1 / 30.

# bounding box for the set of points
minP = Vector3(-100., -100., -100.)
maxP = Vector3(100., 100., 100.)
bb = BoundingBox(minP, maxP)

# window parameters
window_width = 800
window_height = 600
window_aspect = window_width/float(window_height);
eye = [-100., 100., 100]
center = [0., 0., 0.]
up = [0., 1., 0.]

frames = []

theta = 0.
phi = 0.
play = True

showAxis = True
showBounds = True

NUMBER_OF_POINTS = 5

def setProjection():

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluPerspective(60.0, window_aspect, 1, 1000)

def computeEyePosition():

    thetaR = math.radians(theta)
    phiR = math.radians(phi)

    cst = math.cos(thetaR)
    csp = math.cos(phiR)
    snt = math.sin(thetaR)
    snp = math.sin(phiR)

    vx = -100
    vy = 100
    vz = 100

    zx = vx / math.sqrt(vx**2 + vz**2)
    zd = vz / math.sqrt(vx**2 + vz**2)

    rotv = Vector3(
    vx*(cst*(zd*zd + xd*xd*csp) + snt*(-1*xd*zd + xd*zd*csp))
     + vy*(xd*cst*snp + zd*snt*snp)
     + vz*(cst*(-1*xd*zd + xd*zd*csp) + snt*(xd*xd + zd*zd*csp)),
                      vx*(-1*xd*snp) + vy*(csp) + vz*(-1*zd*snp),
     vx*(cst*(-1*xd*zd + xd*zd*csp) - snt*(zd*zd + xd*xd*csp))
     + vy*(-1*xd*snt*snp + zd*cst*snp)
     + vz*(cst*(xd*xd + zd*zd*csp)
       - snt*(-1*xd*zd + xd*zd*csp)))

    return rotv


def computeLookAt():

    eyev = computeEyePosition()
    eye = scalarProd(sumOfVectors(eyev, center), zoom)

def resize(width, height):
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, window_aspect, 1, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    
    glEnable(GL_DEPTH_TEST)
    
    glShadeModel(GL_FLAT)
    glClearColor(1.0, 1.0, 1.0, 0.0)

    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)
    glDisable(GL_COLOR_MATERIAL)

def drawPoint(point):

    glPushMatrix()
    glTranslatef(point.x, point.y, point.z)
    glutSolidSphere(0.5, 80, 80)
    glPopMatrix()

def drawFrame():

    for p in frames[current_frame].points:
        drawPoint(p)

def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # draw all the points in the current frame
    setProjection()

    gluLookAt(eye[0],      eye[1],     eye[2],
           center[0],   center[1],  center[2],
               up[0],       up[1],      up[2])

    if (showAxis):
        drawAxis()
    if (showBounds):
        drawBounds()

    drawFrame()

    glFlush()
    glutSwapBuffers()

def updateBounds():

    global bb
    bb = makeBB(frames[current_frame].points)


def idle():

    global previous_time
    global current_frame
    global frames

    if (play == True):
        actual_time = glutGet(GLUT_ELAPSED_TIME)
        # number of milliseconds between two consecutive frames
        frame_time = int(capture_frame_time * 1000 * speed)
        frames_passed = int((actual_time - previous_time)/frame_time)

        if (frames_passed > 0):
            next_frame = current_frame + frames_passed
            
            if (next_frame > len(frames)):
                next_frame = 0

            current_frame = next_frame
            previous_time = actual_time
            updateBounds()
        glutPostRedisplay()

def drawBounds():

    axis = ['xy', 'xz', 'yz']

    for p in axis:
        notp = [axis[i] for i in range(len(axis)) if axis[i]!= p]
        u = projection(bb.maxPoint, bb.minPoint, notp.pop())
        v = projection(bb.maxPoint, bb.minPoint, notp.pop())
        drawRect(u, v, bb.minPoint)

    for p in axis:
        notp = [axis[i] for i in range(len(axis)) if axis[i]!= p]
        u = projection(bb.minPoint, bb.maxPoint, notp.pop())
        v = projection(bb.minPoint, bb.maxPoint, notp.pop())
        drawRect(u, v, bb.maxPoint)

def mouse(button, state, x, y):

    # right button
    if button == 2:
        if state == GLUT_DOWN:
            beginning_x = x
            beginning_y = y
            right_button_down = True
        else:
            right_button_down = False

    # scroll up
    if button == 3:
        if state == GLUT_DOWN:
            zoom -= zSensitivity * 50
            computeLookAt()

    # scroll down
    if button == 4:
        if state == GLUT_DOWN:
            zoom += zSensitivity * 50
            computeLookAt()

def mouse_motion(x, y):

    if(right_button_down):
        theta += (beginning_x - float(x)) / 2.0
        phi += (beginning_y - float(y)) / 2.0
        beginning_x = x
        beginning_y = y
        if (phi < -45):
            phi = -45
        if (phi > 45):
            phi = 45
        computeLookAt()
        glutPostRedisplay()


def keyboard(key):

    if key == 'f':
        # animation 20% faster
        speed *= 1.2
    
    elif key == 's':
        # animation 20% slower
        speed *= 0.8
    
    elif key == ' ':
        if play:
            play = False
        else:
            play = True

    elif key == 'b':
        showBounds != showBounds

    elif key == 'a':
        showAxis != showAxis

    elif key == 27:
        sys.exit(0)

def main():

    global frames
    frames = parse("log.txt", NUMBER_OF_POINTS)

    # Initialize GLUT
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("3D Reconstruction")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    glutMouseFunc(mouse)
    glutMotionFunc(mouse_motion)

    init()

    glutMainLoop()

if __name__ == '__main__':
    main()
	