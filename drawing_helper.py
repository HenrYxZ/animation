'''
Functions to help drawing in OpenGL.
It can draw an axis and a rectangle.

Created on December 25 2013
@author: Hernaldo Henriquez
'''

from OpenGL.GL import *
from geom import Vector3
from geom import sumOfVectors

def drawRect(u, v, p):

	glBegin(GL_LINE_STRIP)
	glColor3f(0, 0, 1)
	glVertex3f(p.x, p.y, p.z)

	pu = sumOfVectors(p, u)
	glVertex3f(pu.x, pu.y, pu.z)

	puv = sumOfVectors(pu, v)
	glVertex3f(puv.x, puv.y, puv.z)

	pv = sumOfVectors(p, v)
	glVertex3f(pv.x, pv.y, pv.z)

	glVertex3f(p.x, p.y, p.z)
	glEnd()


def drawAxis():

    glLineWidth(2.0)
    line_length = 100
    
    glBegin(GL_LINES)

    glColor3f(1, 0, 0)
    glVertex3i(0, 0, 0)
    glVertex3i(line_length, 0, 0)

    glColor3f(0, 1, 0)
    glVertex3i(0, 0, 0)
    glVertex3i(0, line_length, 0)

    glColor3f(0, 0, 1)
    glVertex3i(0, 0, 0)
    glVertex3i(0, 0, line_length)

    glEnd()
