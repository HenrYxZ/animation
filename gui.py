'''
GUI for showing the 3D points with OpenGL
'''
SCREEN_SIZE = (800, 600)

from math import radians 
from geom import Point3

from OpenGL.GL import *
from OpenGL.GLU import *

previous_time = 0
current_frame = 0

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

def drawAxis():

    glLineWidth(2.0)
    line_length = 100
    
    glBegin(GL_LINES)

    glColor3i(1, 0, 0)
    glVertex3i(0, 0, 0)
    glVertex3i(line_length, 0, 0)

    glColor3i(0, 1, 0)
    glVertex3i(0, 0, 0)
    glVertex3i(0, line_length, 0)

    glColor3i(0, 0, 1)
    glVertex3i(0, 0, 0)
    glVertex3i(0, 0, line_length)

    glEnd()

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
	