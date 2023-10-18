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
    # Left leg
    glBegin(GL_QUADS)
    glVertex2f(-200 - thickness / 2, -200 - thickness)
    glVertex2f(-200 + thickness / 2, -200 - thickness)
    glVertex2f(-200 + thickness / 2, 200 + thickness)
    glVertex2f(-200 - thickness / 2, 200 + thickness)
    glEnd()

    # Left
    glBegin(GL_QUADS)
    glVertex2f(-200 + thickness / 2, 200 - thickness)
    glVertex2f(0, -200 - thickness)
    glVertex2f(0, -200 + thickness)
    glVertex2f(-200 + thickness / 2, 200 + thickness)
    glEnd()

    # Right
    glBegin(GL_QUADS)
    glVertex2f(0, -200 - thickness)
    glVertex2f(200 - thickness / 2, 200 - thickness)
    glVertex2f(200 -thickness / 2, 200 + thickness)
    glVertex2f(0, -200 + thickness)
    glEnd()

    # Right leg
    glBegin(GL_QUADS)
    glVertex2f(200 - thickness / 2, -200 - thickness)
    glVertex2f(200 + thickness / 2, -200 - thickness)
    glVertex2f(200 + thickness / 2, 200 + thickness)
    glVertex2f(200 - thickness / 2, 200 + thickness)
    glEnd()
    glPopMatrix()

def draw_letter_E(x, y, color=(255, 255, 255), scale=1.0, thickness=50):
    glPushMatrix()
    glColor3ub(color[0], color[1], color[2])
    glTranslatef(x, y, 0)
    glScale(scale, scale, 0)

    # Vertical Line
    glBegin(GL_QUADS)
    glVertex2f(-200 - thickness / 2, -200 - thickness)
    glVertex2f(-200 + thickness / 2, -200 - thickness)
    glVertex2f(-200 + thickness / 2, 200 + thickness)
    glVertex2f(-200 - thickness / 2, 200 + thickness)
    glEnd()

    # Top Horizontal Line
    glBegin(GL_QUADS)
    glVertex2f(-200, 200)
    glVertex2f(200, 200)
    glVertex2f(200, 200 + thickness)
    glVertex2f(-200, 200 + thickness)
    glEnd()

    # Center Horizontal Line
    glBegin(GL_QUADS)
    glVertex2f(-200, - thickness / 2)
    glVertex2f(200, - thickness / 2)
    glVertex2f(200, thickness / 2)
    glVertex2f(-200, thickness / 2)
    glEnd()

    # Bottom Horizontal Line
    glBegin(GL_QUADS)
    glVertex2f(-200, -200 - thickness)
    glVertex2f(200, -200 - thickness)
    glVertex2f(200, -200)
    glVertex2f(-200, -200)
    glEnd()
    glPopMatrix()

def draw_letter_A(x, y, color=(255,255,255), scale=1.0, thickness=50):
    glPushMatrix()
    glColor3ub(color[0], color[1], color[2])
    glTranslatef(x, y, 0)
    glScale(scale, scale, 0)

    # Left leg
    glBegin(GL_QUADS)
    glVertex2f(-200 - thickness / 2, -200 - thickness)
    glVertex2f(-200 + thickness / 2, -200 - thickness)
    glVertex2f(0, 200 - thickness)
    glVertex2f(0, 200 + thickness)
    glEnd()

    # Right leg
    glBegin(GL_QUADS)
    glVertex2f(0, 200 - thickness)
    glVertex2f(200 - thickness / 2, -200 - thickness)
    glVertex2f(200 + thickness / 2, -200 - thickness)
    glVertex2f(0, 200 + thickness)
    glEnd()

    # Horizontal Line
    glBegin(GL_QUADS)
    glVertex2f(-200 / 2, - thickness / 2)
    glVertex2f(200 / 2, - thickness / 2)
    glVertex2f(200 / 2, thickness / 2)
    glVertex2f(-200 / 2, thickness / 2)
    glEnd()
    glPopMatrix()

def draw_letter_S(x, y, color=(255, 255, 255), scale=1.0, thickness=50):
    glPushMatrix()
    glColor3ub(color[0], color[1], color[2])
    glTranslatef(x, y, 0)
    glRotatef(-25, 0, 0, 1)
    glScale(scale, scale, 0)
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(90, 271, 5):
        angle = i * (pi / 180.0)
        glVertex2f(100 * cos(angle), 100 * sin(angle) + 100)
        angle = i * (pi / 180.0)
        glVertex2f((100 + thickness) * cos(angle), (100 + thickness) * sin(angle) + 100)
    
    for i in range(270, 451, 5):
        angle = i * (pi / 180.0)
        glVertex2f(100 * cos(angle), -100 * sin(angle) - 100 - thickness)
        angle = i * (pi / 180.0)
        glVertex2f((100 + thickness) * cos(angle), (-100 - thickness) * sin(angle) - 100 - thickness)
    glEnd()
    glPopMatrix()

def draw_letter_T(x, y, color=(255, 255, 255), scale=1.0, thickness=50):
    glPushMatrix()
    glColor3ub(color[0], color[1], color[2])
    glTranslatef(x, y, 0)
    glScale(scale, scale, 0)
    # Horizontal Line
    glBegin(GL_QUADS)
    glVertex2f(-200, 200)
    glVertex2f(200, 200)
    glVertex2f(200, 200 + thickness)
    glVertex2f(-200, 200 + thickness)
    glEnd()

    # Vertical Line
    glBegin(GL_QUADS)
    glVertex2f(-thickness / 2, -200 - thickness)
    glVertex2f(thickness / 2, -200 - thickness)
    glVertex2f(thickness / 2, 200 + thickness)
    glVertex2f(-thickness / 2, 200 + thickness)
    glEnd()
    glPopMatrix()

def draw_letter_R(x, y, color=(255, 255, 255), scale=1.0, thickness=50):
    glPushMatrix()
    glColor3ub(color[0], color[1], color[2])
    glTranslatef(x, y, 0)
    glScale(scale, scale, 0)
    # Vertical Line
    glBegin(GL_QUADS)
    glVertex2f(-200 - thickness / 2, -200 - thickness)
    glVertex2f(-200 + thickness / 2, -200 - thickness)
    glVertex2f(-200 + thickness / 2, 200 + thickness)
    glVertex2f(-200 - thickness / 2, 200 + thickness)
    glEnd()

    # Cirlce
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(270, 451, 5):
        angle = i * (pi / 180.0)
        glVertex2f(300 * cos(angle) - 200, 100 * sin(angle) + 200 - thickness * 1.5)
        angle = i * (pi / 180.0)
        glVertex2f((300 + thickness) * cos(angle) - 200, (100 + thickness) * sin(angle) + 200 - thickness * 1.5)
    glEnd()

    # Right leg
    glBegin(GL_QUADS)
    glVertex2f(-100, - thickness / 2)
    glVertex2f(200 - thickness / 2, -200 - thickness)
    glVertex2f(200 + thickness / 2, -200 - thickness)
    glVertex2f(-100, thickness / 2)
    glEnd()
    glPopMatrix()