from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

from build_context import *

class Enemy:
    def __init__(self, context: BuildContext, id: int, initial_x = 0, initial_y = -70, scale = 0.3):
        self.context = context
        self.id = id
        self.damage = 3
        self.health = 200
        self.speed = 40
        self.scale = scale
        self.size = Size(200, 200)
        self.x = initial_x + self.size.width / 2
        self.y = initial_y + self.size.height / 2
        self.jump_duration = 1.0
        self.jump_height = 20.0
        self.jump_elapsed_time = 0.0
        self.initial_y = initial_y + self.size.height / 2
        self.move_cooldown = 1.5
        self.move_cooldown_elapsed_time = 0.0
        self.is_moving = True
        self.is_going_back = False

    def draw(self):
        glPushMatrix()

        glTranslatef(self.x, self.y, 0)
        glScale(self.scale, self.scale, 0)

        glColor3ub(201, 214, 98)
        glBegin(GL_QUADS)
        glVertex2f(-self.size.width / 2, -self.size.height / 2)
        glVertex2f(self.size.width / 2, -self.size.height / 2)
        glVertex2f(self.size.width / 2, self.size.height / 2)
        glVertex2f(-self.size.width / 2, self.size.height / 2)
        glEnd()

        glColor3ub(12, 0, 15)
        glBegin(GL_QUADS)
        glVertex2f(-self.size.width / 2 + 15, -self.size.height / 2 + 15)
        glVertex2f(self.size.width / 2 - 15, -self.size.height / 2 + 15)
        glVertex2f(self.size.width / 2 - 15, self.size.height / 2 - 15)
        glVertex2f(-self.size.width / 2 + 15, self.size.height / 2 - 15)
        glEnd()

        glBegin(GL_QUADS)
        glColor3ub(148, 131, 75)
        glVertex2f(-self.size.width / 2 + 25, -self.size.height / 2 + 25)
        glColor3ub(148, 131, 75)
        glVertex2f(self.size.width / 2 - 25, -self.size.height / 2 + 25)
        glColor3ub(255, 254, 246)
        glVertex2f(self.size.width / 2 - 25, self.size.height / 2 - 25)
        glColor3ub(255, 254, 246)
        glVertex2f(-self.size.width / 2 + 25, self.size.height / 2 - 25)
        glEnd()

        glPopMatrix()

    def move_towards_dome(self):
        if not self.is_moving:
            if self.move_cooldown_elapsed_time >= self.move_cooldown:
                self.is_moving = True
                self.move_cooldown_elapsed_time = 0.0
            else:
                self.move_cooldown_elapsed_time += 1 / self.context.frame_per_second
                return

        if self.x + self.size.width / 2 * self.scale < -self.context.dome_radius or self.x - self.size.width / 2 * self.scale > self.context.dome_radius:
            jump_progress = self.jump_elapsed_time / self.jump_duration
            if jump_progress >= self.jump_duration:
                self.jump_elapsed_time = 0.0
                self.y = self.initial_y
                self.is_moving = False
            else:
                jump_height = self.jump_height * sin(jump_progress * pi) 
                self.y = self.initial_y + jump_height
                self.jump_elapsed_time += 1 / self.context.frame_per_second

        if self.x + self.size.width / 2 * self.scale <= -self.context.dome_radius + 10.0:
            angle_radians = atan2(self.y - self.size.height / 2 * self.scale, self.x + self.size.width / 2 * self.scale)
            x_dome_hitbox = self.context.dome_radius * cos(angle_radians)
            y_dome_hitbox = self.context.dome_radius * sin(angle_radians)

            if self.x + self.size.width / 2 * self.scale >= x_dome_hitbox and self.y - self.size.height / 2 * self.scale <= y_dome_hitbox:
                self.context.dome.take_damage(self.damage)
                self.is_going_back = True
            
            if self.is_going_back:
                self.x -= self.speed / self.context.frame_per_second
                if self.y == self.initial_y:
                    self.is_going_back = False
            else:
                self.x += self.speed / self.context.frame_per_second
        elif self.x - self.size.width / 2 * self.scale >= self.context.dome_radius - 10.0:
            angle_radians = atan2(self.y - self.size.height / 2 * self.scale, self.x - self.size.width / 2 * self.scale)
            x_dome_hitbox = self.context.dome_radius * cos(angle_radians)
            y_dome_hitbox = self.context.dome_radius * sin(angle_radians)

            if self.x - self.size.width / 2 * self.scale <= x_dome_hitbox and self.y - self.size.height / 2 * self.scale <= y_dome_hitbox:
                self.context.dome.take_damage(self.damage)
                self.is_going_back = True
            
            if self.is_going_back:
                self.x += self.speed / self.context.frame_per_second
                if self.y == self.initial_y:
                    self.is_going_back = False
            else:
                self.x -= self.speed / self.context.frame_per_second

    def distance(self):
        return sqrt(self.x ** 2 + self.y ** 2)
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def is_dead(self): 
        return self.health <= 0