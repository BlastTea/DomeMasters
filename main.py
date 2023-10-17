import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
from text_drawer import *

from build_context import *
from objects.dome import *
from objects.enemy import *

context = BuildContext()

def draw():
    context.dome.draw()
    for enemy in context.current_enemies:
        enemy.draw()

def iterate():
    glViewport(0, 0, context.w, context.h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(-context.w, context.w, -context.h, context.h, 0.0, 1.0),
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(context.camera_position[0], context.camera_position[1], context.camera_position[2])

def showScreen():
    start_time = time.time()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    context.draw_background()
    draw()
    for enemy in context.current_enemies:
        enemy.move_towards_dome()

    left_closes_enemy = sorted(filter(lambda e: e.x <= 0, context.current_enemies), key=lambda e: e.distance())
    right_closes_enemy = sorted(filter(lambda e: e.x >= 0, context.current_enemies), key=lambda e: e.distance())

    if len(left_closes_enemy) > 0:
        context.dome.weapon.is_shooting_enemy(left_closes_enemy[0])
    if len(right_closes_enemy) > 0:
        context.dome.weapon.is_shooting_enemy(right_closes_enemy[0])
    if context.current_state is context.GAMEPLAY:
        context.show_hud()

    update_movement()

    context.start_next_wave()

    glutSwapBuffers()

    frame_time = time.time() - start_time
    sleep_time = 1.0 / context.fps - frame_time
    if sleep_time > 0:
        time.sleep(sleep_time)

def reshape(new_w, new_h):
    context.w = new_w
    context.h = new_h

def keyboard(key, x, y):
    if key in (b'a', b'A', b'd', b'D'):
        context.movement_keys.add(key)
    
    if key == b' ':
        context.dome.weapon.shoot()

def keyboard_up(key, x, y):
    if key == b' ':
        context.dome.weapon.stop_shooting()

    if key in (b'a', b'A', b'd', b'D'):
        context.movement_keys.remove(key)

def special_keyboard(key, x, y):
    if key in (GLUT_KEY_LEFT, GLUT_KEY_RIGHT):
        context.movement_keys.add(key)

def update_movement():
    for key in context.movement_keys:
        if key == b'a' or key == b'A':
            context.dome.weapon.move_left()
        elif key == b'd' or key == b'D':
            context.dome.weapon.move_right()
        elif key == GLUT_KEY_LEFT:
            context.dome.weapon.move_left()
        elif key == GLUT_KEY_RIGHT:
            context.dome.weapon.move_right()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(context.w, context.h)
glutInitWindowPosition(0, 0)
glutCreateWindow('Dome Masters')
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutKeyboardUpFunc(keyboard_up)
glutSpecialFunc(special_keyboard)
glutMainLoop()
