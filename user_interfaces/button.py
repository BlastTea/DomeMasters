from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

from build_context import *

class Button:
    def __init__(self, context:BuildContext, text:str, size:Size, initial_x, initial_y):
        self.context = context
        self.text = text
        self.size = size
        self.x = initial_x
        self.y = initial_y
    
    def draw(self):
        drawText(self.text, self.x, self.y)

    def on_click(self, x, y):
        return self.context.w / 2 + self.x + 50 <= x <= self.context.w / 2 + self.x + 50 + self.size.width and self.context.h