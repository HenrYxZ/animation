'''
GUI for showing the 3D points with OpenGL

Created on December 25 2013
@author: Hernaldo Henriquez
'''
SCREEN_SIZE = (800, 600)

from math import radians 
from geom import Point3
from geom import BoundingBox
from geom import projection
import sys

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

# bounding box for the set of points
minP = Point3(-100., -100., -100.)
maxP = Point3(100., 100., 100.)
bb = BoundingBox(minP, maxP)

# window parameters
window_width = 800
window_height = 600
window_aspect = window_width/float(window_height);
eye = []
center = [0., 0., 0.]
up = [0., 1., 0.]

theta = 0.
phi = 0.

def setProjection():

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluPerspective(60.0, window_aspect, 1, 1000)

def computeLookAt():

    

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

def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # draw all the points in the current frame
    setProjection()

def idle():

    if (play == true):
        actual_time = glutGet(GLUT_ELAPSED_TIME)
        # number of milliseconds between two consecutive frames
        frame_time = int(capture_frame_time * 1000 * speed)
        frames_passed = int((actual_time - previous_time)/frame_time)

        if (frames_passed > 0):
            next_frame = current_frame + frames_passed
            
            if (next_frame > number_of_frames):
                next_frame = 0

            current_frame = next_frame
            previous_time = actual_time

        glutPostRedisplay()

def drawBounds():

    axis = ['xy', 'xz', 'yz']

    for p in axis:
        notp = [axis[i] for i in range(len(axis)) if axis[i]!= p]
        u = projection(bb.getMax(), bb.getMin(), notp.pop())
        v = projection(bb.getMax(), bb.getMin(), notp.pop())
        drawRect(u, v, bb.getMin())

    for p in axis:
        notp = [axis[i] for i in range(len(axis)) if axis[i]!= p]
        u = projection(bb.getMin(), bb.getMax(), notp.pop())
        v = projection(bb.getMin(), bb.getMax(), notp.pop())
        drawRect(u, v, bb.getMax())

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


def keyboard(key):

    if key == 'f':
        # animation 20% faster
        speed *= 1.2
    
    elif key == 's':
        # animation 20% slower
        speed *= 0.8
    
    elif key == ' ':
        play = false if play else play = true

    elif key == 'b':
        drawBounds()

    elif key == 27:
        sys.exit(0)

def main():

    # Initialize GLUT
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutWindowPosition(100, 100)
    glutCreateWindow("3D Reconstruction")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    glutMouseFunc(mouse)
    glutMotionFunc(mouseMotion)

if __name__ == '__main__':
    main()
	