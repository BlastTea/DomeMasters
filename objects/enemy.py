from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

from build_context import *

class Enemy:
    def __init__(self, context: BuildContext, id: int, initial_x = 0, initial_y = 5):
        self.context = context
        self.id = id
        self.damage = 3
        self.health = 200
        self.speed = 40
        self.size = 40
        self.x = initial_x + self.size
        self.y = initial_y + self.size
        pass

    def draw(self):
        glPushMatrix()

        glTranslatef(self.x, self.y, 0)
        glColor3ub(124, 146, 143)

        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(-self.size, -self.size + 10)
        glVertex2f(self.size, -self.size + 10)
        glVertex2f(27, -15)
        glVertex2f(17, -3)
        glVertex2f(9, 8)
        glVertex2f(0, self.size)
        glVertex2f(-15, 23)
        glVertex2f(-28, -10)
        glEnd()

        major_radius = self.size
        minor_radius = 10

        glTranslatef(0, -self.size + 10, 0)
        glBegin(GL_TRIANGLE_FAN)
        for i in range(180, 361, 5):
            angle = i * (pi / 180.0)
            glVertex2f(major_radius * cos(angle), minor_radius * sin(angle))
        glEnd()

        glPopMatrix()

    def move_towards_dome(self):
        if self.x + self.size < -self.context.dome_radius:
            self.x += self.speed / self.context.fps
        elif self.x - self.size > self.context.dome_radius:
            self.x -= self.speed / self.context.fps
        else:
            self.context.dome.take_damage(self.damage / self.context.fps)

    def distance(self):
        return sqrt(self.x ** 2 + self.y ** 2)
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def is_dead(self): 
        return self.health <= 0