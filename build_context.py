import random

from OpenGL.GL import *
from math import *

from user_interfaces.text_drawer import *
from size import *

class BuildContext:
    TITLE_SCREEN = 0
    ANIMATING_TO_TITLE_SCREEN = 1
    GAMEPLAY = 2
    ANIMATING_TO_GAMEPLAY = 3
    GAME_OVER = 4

    def __init__(self):
        from objects.dome import Dome
        from user_interfaces.button import Button
        self.w = 800
        self.h = 600
        self.frame_per_second = 60
        self.dome_radius = 200

        self.movement_keys = set()
        self.current_enemies = []

        self.wave_counter = 1
        self.kill_counter = 0

        self.camera_position = [0, -self.h * 2, 0]
        # self.camera_position = [0, 0, 0]

        self.current_state = self.TITLE_SCREEN
        # self.current_state = self.GAMEPLAY

        self.spawn_cooldown = 0.0
        self.spawn_cooldown_elapsed_time = 0.0

        self.total_enemy = 0

        self.dome = Dome(self)

        self.button_play = Button(self, 'Play', Size(40, 40), -100, self.h * 2 - 400)

    def remove_enemy(self, id):
        self.kill_counter += 1
        self.current_enemies = list(filter(lambda e: e.id is not id, self.current_enemies))

    def tick_next_wave(self):
        from objects.enemy import Enemy

        self.spawn_cooldown_elapsed_time += 1 / self.frame_per_second
        
        if self.total_enemy == 0 and len(self.current_enemies) == 0:
            self.wave_counter += 1
            self.total_enemy = self.wave_counter + random.randint(1, self.wave_counter)

        if self.spawn_cooldown_elapsed_time >= self.spawn_cooldown and self.total_enemy > 0:
            self.spawn_cooldown_elapsed_time = 0.0
            self.spawn_cooldown = random.random()
            self.total_enemy -= 1
            self.current_enemies.append(Enemy(self, 0 if len(self.current_enemies) == 0 else len(self.current_enemies) - 1, self.w if random.choice([True, False]) else -self.w - 150.0))


    def draw_background(self):
        
        if self.current_state is self.TITLE_SCREEN or self.current_state is self.ANIMATING_TO_TITLE_SCREEN or self.current_state is self.ANIMATING_TO_GAMEPLAY:
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

            draw_letter_D(-700, self.h * 2 + 200, color, scale, thickness)
            draw_letter_O(-500, self.h * 2 + 200, color, scale, thickness)
            draw_letter_M(-300, self.h * 2 + 200, color, scale, thickness)
            draw_letter_E(-100, self.h * 2 + 200, color, scale, thickness)

            draw_letter_M(-600, self.h * 2 - 100, color, scale, thickness)
            draw_letter_A(-400, self.h * 2 - 100, color, scale, thickness)
            draw_letter_S(-230, self.h * 2 - 100, color, scale, thickness)
            draw_letter_T(-70, self.h * 2 - 100, color, scale, thickness)
            draw_letter_E(130, self.h * 2 - 100, color, scale, thickness)
            draw_letter_R(400, self.h * 2 - 100, color, scale, thickness)
            draw_letter_S(600, self.h * 2 - 100, color, scale, thickness)

            self.button_play.draw()

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

    def draw_hud(self):
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