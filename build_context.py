import random

from OpenGL.GL import *
from math import *

from text_drawer import *

class BuildContext:
    TITLE_SCREEN = 0
    ANIMATING_TO_TITLE_SCREEN = 1
    GAMEPLAY = 2
    ANIMATING_TO_GAMEPLAY = 3

    def __init__(self):
        from objects.dome import Dome
        self.w = 800
        self.h = 600
        self.fps = 60
        self.dome_radius = 200

        self.movement_keys = set()
        self.current_enemies = []

        self.wave_counter = 1
        self.kill_counter = 0

        # self.camera_position = [0, -self.h * 2, 0]
        self.camera_position = [0, 0, 0]

        # self.current_state = self.TITLE_SCREEN
        self.current_state = self.GAMEPLAY

        self.dome = Dome(self)

    def remove_enemy(self, id):
        self.kill_counter += 1
        self.current_enemies = list(filter(lambda e: e.id is not id, self.current_enemies))
        if len(self.current_enemies) == 0:
            self.start_next_wave()


    def start_next_wave(self):
        from objects.enemy import Enemy
        
        self.wave_counter += 1
        for i in range(random.randint(1, self.wave_counter)):
            is_positive = random.choice([True, False])

            random_x = self.w + random.randint(1, 200)

            self.current_enemies.append(Enemy(self, i, random_x if is_positive else -random_x))

    def draw_background(self):
        if self.current_state is self.TITLE_SCREEN or self.current_state is self.ANIMATING_TO_TITLE_SCREEN:
            # above the sky
            glPushMatrix()
            glColor3ub(190, 117, 61)
            glBegin(GL_QUADS)
            glVertex2f(-self.w, self.h)
            glVertex2f(self.w, self.h)
            glVertex2f(self.w, self.h * 3)
            glVertex2f(-self.w, self.h * 3)
            glEnd()
            glPopMatrix()

            color = (162, 102, 109)
            thickness = 60
            scale = 0.4

            draw_letter_D(-400, self.h * 2, color, scale, thickness)
            draw_letter_O(-200, self.h * 2, color, scale, thickness)
            # draw_letter_M(0, self.h * 2, color, scale, thickness)

        # Sky
        glPushMatrix()
        glColor3ub(190, 117, 61)
        glBegin(GL_QUADS)
        glVertex2f(-self.w, 0)
        glVertex2f(self.w, 0)
        glVertex2f(self.w, self.h)
        glVertex2f(-self.w, self.h)
        glEnd()

        # Ground
        glColor3ub(34, 23, 14)
        glBegin(GL_QUADS)
        glVertex2f(-self.w, -self.h)
        glVertex2f(self.w, -self.h)
        glVertex2f(self.w, 0)
        glVertex2f(-self.w, 0)
        glEnd()
        glPopMatrix()

    def show_hud(self):
        # kill counter
        drawText(f'{self.kill_counter}', -self.w + 20, -self.h + 60)
        
        # heart icon
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef(35, 35, 0)
        glBegin(GL_POLYGON)
        for t in range(0, 360, 1):
            angle = t * pi / 180.0
            x = -self.w + 16 * (sin(angle) ** 3)
            y = -self.h + 13 * cos(angle) - 5 * cos(2 * angle) - 2 * cos(3 * angle) - cos(4 * angle)
            glVertex2f(x, y)
        glEnd()
        glPopMatrix()

        # health bar
        glPushMatrix()
        glTranslatef(55, 20, 0)

        # outline of the health bar
        glColor3f(1, 1, 1)
        glBegin(GL_LINE_LOOP)
        glVertex2f(-self.w, -self.h + 25)
        glVertex2f(-self.w + 200, -self.h + 25)
        glVertex2f(-self.w + 200, -self.h)
        glVertex2f(-self.w, -self.h)
        glEnd()
        
        # the progress of the health bar
        glColor3f(1, 0, 0)
        glBegin(GL_QUADS)
        glVertex2f(-self.w + 1, -self.h + 25 - 1)
        glVertex2f(-self.w + (200 * self.dome.health / self.dome.max_health) - 1, -self.h + 25 - 1)
        glVertex2f(-self.w + (200 * self.dome.health / self.dome.max_health) - 1, -self.h + 1)
        glVertex2f(-self.w + 1, -self.h + 1)
        glEnd()
        glPopMatrix()