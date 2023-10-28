import random

from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

from build_context import *
from objects.enemy import *

class Weapon:
    def __init__(self, context: BuildContext):
        self.context = context
        self.damage = 20
        self.max_speed = 30
        self.speed = self.max_speed
        self.orientation_degrees = 90.0
        self.update_position()
        self.is_shooting = False
        self.shooting_enemy = None

    def update_position(self):
        self.weapon_orientation_radians = self.orientation_degrees * (pi / 180.0)
        self.x = self.context.dome_radius * cos(self.weapon_orientation_radians)
        self.y = self.context.dome_radius * sin(self.weapon_orientation_radians)

    def draw(self):
        'draw the weapon'
        glPushMatrix()

        if self.is_shooting:
            self.draw_laser()

        glTranslatef(self.x, self.y, 0.0)    
        glRotatef(self.orientation_degrees - 90, 0, 0, 1)
        glScale(0.4, 0.4, 0.0)

        glColor3ub(252, 178, 115)
        glBegin(GL_QUADS)
        glVertex2f(-50, -20)
        glVertex2f(50, -20)
        glVertex2f(10, 60)
        glVertex2f(-10, 60)
        glEnd()

        glColor3ub(13, 9, 23)
        glBegin(GL_QUADS)
        glVertex2f(-60, -20)
        glVertex2f(60, -20)
        glVertex2f(22, 35)
        glVertex2f(-22, 35)
        glEnd()
        
        glColor3ub(252, 178, 115)
        glBegin(GL_QUADS)
        glVertex2f(-60, -20)
        glVertex2f(60, -20)
        glVertex2f(35, 30)
        glVertex2f(-35, 30)
        glEnd()

        glColor3ub(13, 9, 23)
        glBegin(GL_QUADS)
        glVertex2f(-60, -20)
        glVertex2f(60, -20)
        glVertex2f(50, 15)
        glVertex2f(-50, 15)
        glEnd()

        glColor3ub(252, 178, 115)
        glBegin(GL_QUADS)
        glVertex2f(-60, -20)
        glVertex2f(60, -20)
        glVertex2f(50, 10)
        glVertex2f(-50, 10)
        glEnd()

        glPopMatrix()
    
    def draw_laser(self):
        'draw the laser originating from the weapon and shooting outwards'
        glColor3ub(252, 253, 235)
        glLineWidth(self.damage / 10)
        
        glBegin(GL_LINES)

        laser_start_x = self.context.dome_radius * cos(self.weapon_orientation_radians)
        laser_start_y = self.context.dome_radius * sin(self.weapon_orientation_radians)

        laser_end_x, laser_end_y = 0, 0
        if self.shooting_enemy is not None:
            laser_end_x = self.shooting_enemy.distance() * cos(self.orientation_degrees * (pi / 180.0))
            laser_end_y = self.shooting_enemy.distance() * sin(self.orientation_degrees * (pi / 180.0))
        else:
            laser_end_x = (self.context.dome_radius + 4000) * cos(self.weapon_orientation_radians)
            laser_end_y = (self.context.dome_radius + 4000) * sin(self.weapon_orientation_radians)
        
        glVertex2f(laser_start_x, laser_start_y)
        glVertex2f(laser_end_x, laser_end_y)

        glEnd()

        glLineWidth(1.0)

    def move_left(self):
        'move the weapon to the left'
        self.orientation_degrees += self.speed / self.context.frame_per_second
        
        if self.orientation_degrees >= 181:
            self.orientation_degrees = 181
         
        self.update_position()

    def move_right(self):
        'move the weapon to the right'
        self.orientation_degrees -= self.speed / self.context.frame_per_second

        if self.orientation_degrees <= -1:
            self.orientation_degrees = -1

        self.update_position()

    def shoot(self):
        'shoot'
        self.is_shooting = True
        self.speed = self.max_speed * 0.4

    def stop_shooting(self):
        'stop the weapon from shooting'
        self.is_shooting = False
        self.speed = self.max_speed
    
    def is_shooting_enemy(self, enemy: Enemy):
        if self.is_shooting is False or (self.shooting_enemy is not None and self.shooting_enemy.id is not enemy.id):
        # if self.is_shooting is False or self.shooting_enemy is not None:      
            return

        laser_x = enemy.distance() * cos(self.orientation_degrees * (pi / 180.0))
        laser_y = enemy.distance() * sin(self.orientation_degrees * (pi / 180.0))

        # Well, if you wanna see where the pointer is, uncomment below code :)
        # glPushMatrix()
        # glColor3f(0, 1, 1)
        # glPointSize(5.0)
        # glBegin(GL_POINTS)
        # glVertex2f(laser_x, laser_y)
        # glEnd()
        # glPopMatrix()

        if laser_x <= enemy.x + enemy.size.width / 2 * enemy.scale and laser_x >= enemy.x - enemy.size.width / 2 * enemy.scale and laser_y <= enemy.y + enemy.size.height / 2 * enemy.scale and laser_y >= enemy.y - enemy.size.height / 2 * enemy.scale:
            self.shooting_enemy = enemy
            enemy.take_damage(self.damage / self.context.frame_per_second)
            
            if not enemy.is_dead():
                return
            
            self.context.remove_enemy(enemy.id)
        self.shooting_enemy = None