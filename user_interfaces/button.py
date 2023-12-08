from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

from build_context import *

class Button:
    def __init__(self, context:BuildContext, text:str, size:Size, x, y, text_color = (255, 255, 255)):
        self.context = context
        self.text = text
        self.size = size
        self.x = x
        self.y = y
        self.initial_y = y
        self.text_color = text_color
    
    def draw(self):
        self.y = self.initial_y + (self.context.h * 2 if self.context.current_state is self.context.TITLE_SCREEN else 0)
        drawText(self.text, self.x, self.y, self.text_color)

    def is_on_click(self, x, y):
        actual_y = self.y - (self.context.h * 2 if self.context.current_state is self.context.TITLE_SCREEN else 0)
        return self.context.w + self.x <= x * 2 <= self.context.w + self.x + self.size.width and self.context.h + (actual_y if actual_y >= 0 else abs(actual_y)) - self.size.height <= y * 2 <= self.context.h + (actual_y if actual_y >= 0 else abs(actual_y))