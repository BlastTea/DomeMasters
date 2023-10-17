import OpenGL.GLUT as glut
from OpenGL.GLUT import *
from OpenGL.GL import *
from math import *

def drawText(text, x, y, text_color=(255, 255, 255)):
    glPushMatrix()
    font_style = glut.GLUT_BITMAP_HELVETICA_18
    glColor3ub(text_color[0], text_color[1], text_color[2])
    line = 0
    glRasterPos2f(x, y)
    for i in text:
        if i == '\n':
            glRasterPos2f(x, y*line)
        else:
            glut.glutBitmapCharacter(font_style, ord(i))
    glPopMatrix()

def draw_letter_D(x, y, color=(255, 255, 255), scale=1.0, thickness=50):
    glPushMatrix()
    glColor3ub(color[0], color[1], color[2])
    glTranslatef(x, y, 0)
    glScale(scale, scale, 0)
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(270, 451, 5):
        angle = i * (pi / 180.0)
        glVertex2f(200 * cos(angle), 200 * sin(angle))
        angle = i * (pi / 180.0)
        glVertex2f((200 + thickness) * cos(angle),
                   (200 + thickness) * sin(angle))
    glEnd()

    glBegin(GL_POLYGON)
    glVertex2f(-thickness / 2, -200 - thickness)
    glVertex2f(thickness / 2, -200 - thickness)
    glVertex2f(thickness / 2, 200 + thickness)
    glVertex2f(-thickness / 2, 200 + thickness)
    glEnd()
    glPopMatrix()

def draw_letter_O(x, y, color=(255, 255, 255), scale=1.0, thickness=50):
    glPushMatrix()
    glColor3ub(color[0], color[1], color[2])
    glTranslatef(x, y, 0)
    glScale(scale, scale, 0)
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(0, 361, 5):
        angle = i * (pi / 180.0)
        glVertex2f(130 * cos(angle), 200 * sin(angle))
        angle = i * (pi / 180.0)
        glVertex2f((130 + thickness) * cos(angle),
                   (200 + thickness) * sin(angle))
    glEnd()
    glPopMatrix()

def draw_letter_M(x, y, color=(255, 255, 255), scale=1.0, thickness=50):
    glPushMatrix()
    glColor3ub(color[0], color[1], color[2])
    glTranslatef(x, y, 0)
    glScale(scale, scale, 0)
    glBegin(GL_QUADS)
    glVertex2f()
    glEnd()
    glPopMatrix()

def draw_letter_E(x, y, color=(255, 255, 255), scale=1.0, thickness=50):
    pass

def draw_letter_A(x, y, color=(255,255,255), scale=1.0, thickness=50):
    pass

def draw_letter_S(x, y, color=(255, 255, 255), scale=1.0, thickness=50):
    pass

def draw_letter_T(x, y, color=(255, 255, 255), scale=1.0, thickness=50):
    pass

def draw_letter_R(x, y, color=(255, 255, 255), scale=1.0, thickness=50):
    pass