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
        self.size = 100
        self.x = initial_x + self.size
        self.y = initial_y + self.size
        self.jump_duration = 1.0
        self.jump_height = 20.0
        self.jump_elapsed_time = 0.0
        self.initial_y = initial_y + self.size
        self.move_cooldown = 1.5
        self.move_cooldown_elapsed = 0.0
        self.is_moving = True
        self.is_going_back = False

    def draw(self):
        glPushMatrix()

        glTranslatef(self.x, self.y, 0)
        glScale(self.scale, self.scale, 0)

        glColor3ub(201, 214, 98)
        glBegin(GL_QUADS)
        glVertex2f(-self.size, -self.size)
        glVertex2f(self.size, -self.size)
        glVertex2f(self.size, self.size)
        glVertex2f(-self.size, self.size)
        glEnd()

        glColor3ub(12, 0, 15)
        glBegin(GL_QUADS)
        glVertex2f(-self.size + 15, -self.size + 15)
        glVertex2f(self.size - 15, -self.size + 15)
        glVertex2f(self.size - 15, self.size - 15)
        glVertex2f(-self.size + 15, self.size - 15)
        glEnd()

        glBegin(GL_QUADS)
        glColor3ub(148, 131, 75)
        glVertex2f(-self.size + 25, -self.size + 25)
        glColor3ub(148, 131, 75)
        glVertex2f(self.size - 25, -self.size + 25)
        glColor3ub(255, 254, 246)
        glVertex2f(self.size - 25, self.size - 25)
        glColor3ub(255, 254, 246)
        glVertex2f(-self.size + 25, self.size - 25)
        glEnd()

        glPopMatrix()

    def get_size(self):
        return self.size * self.scale

    def move_towards_dome(self):
        if not self.is_moving:
            if self.move_cooldown_elapsed >= self.move_cooldown:
                self.is_moving = True
                self.move_cooldown_elapsed = 0.0
            else:
                self.move_cooldown_elapsed += 1 / self.context.fps
                return

        if self.x + self.get_size() < -self.context.dome_radius or self.x - self.get_size() > self.context.dome_radius:
            jump_progress = self.jump_elapsed_time / self.jump_duration
            if jump_progress >= self.jump_duration:
                self.jump_elapsed_time = 0.0
                self.y = self.initial_y
                self.is_moving = False
            else:
                jump_height = self.jump_height * sin(jump_progress * pi) 
                self.y = self.initial_y + jump_height
                self.jump_elapsed_time += 1 / self.context.fps

        if self.x + self.get_size() <= -self.context.dome_radius + 10.0:
            angle_radians = atan2(self.y - self.get_size(), self.x + self.get_size())
            x_dome_hitbox = self.context.dome_radius * cos(angle_radians)
            y_dome_hitbox = self.context.dome_radius * sin(angle_radians)

            # x_dome_hitbox_end = (self.context.dome_radius + self.distance() - self.context.dome_radius - self.get_size()) * cos(angle_radians)
            # y_dome_hitbox_end = (self.context.dome_radius + self.distance() - self.context.dome_radius - self.get_size()) * sin(angle_radians)

            # glPushMatrix()
            # glColor3f(0, 1, 1)
            # glLineWidth(3.0)
            # glBegin(GL_LINES)
            # glVertex2f(x_dome_hitbox, y_dome_hitbox)
            # glVertex2f(x_dome_hitbox_end, y_dome_hitbox_end)
            # glEnd()
            # glPopMatrix()

            if self.x + self.get_size() >= x_dome_hitbox and self.y - self.get_size() <= y_dome_hitbox:
                self.context.dome.take_damage(self.damage)
                self.is_going_back = True
            
            if self.is_going_back:
                self.x -= self.speed / self.context.fps
                if self.y == self.initial_y:
                    self.is_going_back = False
            else:
                self.x += self.speed / self.context.fps
        elif self.x - self.get_size() >= self.context.dome_radius - 10.0:
            angle_radians = atan2(self.y - self.get_size(), self.x - self.get_size())
            x_dome_hitbox = self.context.dome_radius * cos(angle_radians)
            y_dome_hitbox = self.context.dome_radius * sin(angle_radians)

            if self.x - self.get_size() <= x_dome_hitbox and self.y - self.get_size() <= y_dome_hitbox:
                self.context.dome.take_damage(self.damage)
                self.is_going_back = True
            
            if self.is_going_back:
                self.x += self.speed / self.context.fps
                if self.y == self.initial_y:
                    self.is_going_back = False
            else:
                self.x -= self.speed / self.context.fps

    def distance(self):
        return sqrt(self.x ** 2 + self.y ** 2)
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def is_dead(self): 
        return self.health <= 0