from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

from build_context import *

class Button:
    def __init__(self, context:BuildContext, text:str, size:Size, x, y):
        self.context = context
        self.text = text
        self.size = size
        self.x = x
        self.y = y + (context.h * 2 if context.current_state is context.TITLE_SCREEN else 0)
    
    def draw(self):
        drawText(self.text, self.x, self.y)

    def is_on_click(self, x, y):
        actual_y = self.y - (self.context.h * 2 if self.context.current_state is self.context.TITLE_SCREEN else 0)
        # print(f'isOnClick ({x}, {y}) : {self.context.w + self.x} <= {x * 2} <= {self.context.w + self.x + self.size.width} and {self.context.h + (actual_y if actual_y >= 0 else abs(actual_y) - self.size.height)} <= {y * 2} <= {self.context.h + (actual_y if actual_y >= 0 else abs(actual_y))} : {self.context.h + (actual_y if actual_y >= 0 else abs(actual_y)) - self.size.height <= y * 2 <= self.context.h + (actual_y if actual_y >= 0 else abs(actual_y))}')

        return self.context.w + self.x <= x * 2 <= self.context.w + self.x + self.size.width and self.context.h + (actual_y if actual_y >= 0 else abs(actual_y)) - self.size.height <= y * 2 <= self.context.h + (actual_y if actual_y >= 0 else abs(actual_y))