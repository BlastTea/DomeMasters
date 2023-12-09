import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *

from build_context import *
from objects.dome import *
from objects.enemy import *

context = BuildContext()

def draw():
    context.dome.draw()
    for enemy in context.current_enemies:
        enemy.draw()

def show_pause():
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1.0, 1.0, 1.0)  # Warna teks putih

    pause_text = "Game Paused"
    resume_text = "Press 'p' to resume"

    # Menentukan posisi teks
    pause_text_x = context.w // 2 - len(pause_text) * 5
    pause_text_y = context.h // 2 + 20

    resume_text_x = context.w // 2 - len(resume_text) * 5
    resume_text_y = context.h // 2 - 20

    # Memanggil fungsi drawText untuk menggambar teks
    drawText(pause_text, pause_text_x, pause_text_y)
    drawText(resume_text, resume_text_x, resume_text_y)

    glPopMatrix()

def iterate():
    glViewport(0, 0, context.w, context.h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(-context.w, context.w, -context.h, context.h, 0.0, 1.0),
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if context.current_state == context.ANIMATING_TO_GAMEPLAY and context.camera_position[1] < 0:
        context.camera_position[1] += 1500 / context.frame_per_second
    elif context.current_state == context.ANIMATING_TO_GAMEPLAY and context.camera_position[1] >= 0:
        context.camera_position[1] = 0
        context.current_state = context.GAMEPLAY

    glTranslatef(context.camera_position[0], context.camera_position[1], context.camera_position[2])

def showScreen():
    if context.current_state is context.GAME_OVER:
        print('Oy mate, it\'s game over, get out from here!')
    
    if context.current_state == context.GAMEPLAY:
        if b'p' in context.movement_keys:
            context.is_paused = not context.is_paused
            time.sleep(0.2)
            if context.is_paused:
                show_pause(context)

    if context.is_paused:
        glutSwapBuffers()
        return
    start_time = time.time()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    context.draw_background()
    draw()
    if context.current_state is context.GAMEPLAY:
        for enemy in context.current_enemies:
            enemy.move_towards_dome()

        left_closes_enemy = sorted(filter(lambda e: e.x <= 0, context.current_enemies), key=lambda e: e.distance())
        is_shooting_enemy = False

        if len(left_closes_enemy) > 0:
            is_shooting_enemy = context.dome.weapon.is_shooting_enemy(left_closes_enemy[0])
        if not is_shooting_enemy:
            right_closes_enemy = sorted(filter(lambda e: e.x >= 0, context.current_enemies), key=lambda e: e.distance())
            if len(right_closes_enemy) > 0:
                context.dome.weapon.is_shooting_enemy(right_closes_enemy[0])
        update_movement()
        context.tick_next_wave()
    
    if context.current_state is context.GAMEPLAY or context.current_state is context.GAME_OVER:
        context.draw_hud()
    
    if context.current_state == context.GAME_OVER:
        context.show_game_over()

    glutSwapBuffers()

    frame_time = time.time() - start_time
    sleep_time = 1.0 / context.frame_per_second - frame_time
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

    if key in (b'p', b'P'):
        context.is_paused = not context.is_paused
        time.sleep(0.2)

def keyboard_up(key, x, y):
    if key == b' ':
        context.dome.weapon.stop_shooting()

    if key in (b'a', b'A', b'd', b'D'):
        context.movement_keys.remove(key)

def special_keyboard(key, x, y):
    if key in (GLUT_KEY_LEFT, GLUT_KEY_RIGHT):
        context.movement_keys.add(key)

def special_keyboar_up(key, x, y):
    if key in (GLUT_KEY_LEFT, GLUT_KEY_RIGHT):
        context.movement_keys.remove(key)

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

def mouse(button, state, x, y):
    if context.button_play.is_on_click(x, y):
        context.current_state = context.ANIMATING_TO_GAMEPLAY
    if context.button_restart.is_on_click(x, y):
        context.restart()

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
glutSpecialUpFunc(special_keyboar_up)
glutMouseFunc(mouse)
glutMainLoop()
