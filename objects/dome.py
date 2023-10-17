from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

from build_context import *
from objects.weapon import *

class Dome:
    def __init__(self, context: BuildContext):
        self.context = context
        self.health = 100
        self.max_health = 100
        self.weapon = Weapon(context)

    def draw(self):
        'draw the dome'
        glPushMatrix()
        glColor3ub(63, 35, 63)

        glBegin(GL_TRIANGLE_FAN)
        for i in range(0, 181, 5):
            angle = i * (pi / 180.0)
            glVertex2f(self.context.dome_radius * cos(angle), self.context.dome_radius * sin(angle))
        glEnd()

        major_radius = self.context.dome_radius
        minor_radius = 50

        glBegin(GL_TRIANGLE_FAN)
        for i in range(180, 361, 5):
            angle = i * (pi / 180.0)
            glVertex2f(major_radius * cos(angle), minor_radius * sin(angle))
        glEnd()

        glPopMatrix()

        self.weapon.draw()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
    
    def is_game_over(self):
        return self.health <= 0
        