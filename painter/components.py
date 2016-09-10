import interpolation
import pygame

class Position:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class Size:
    scale = 1

    def __init__(self, width=0.0, height=0.0):
        self.width = width
        self.height = height

class Text:
    def __init__(self, text="", font=None, color=(0, 128, 0)):
        self.text = text
        self.font = font
        self.color = color

class Image:
    def __init__(self, image=None):
        self.image = image

class Click:
    def __init__(self, run=None):
        self.run = run

class Over:
    active = False

    def __init__(self, enterf=None, exitf=None):
        self.enterf = enterf
        self.exitf = exitf

class Circle:
    def __init__(self, color=(0,128,0), radius=0.0, width=0):
        self.color = color
        self.radius = radius
        self.width = width

class Rect:
    def __init__(self, color=(0,128,0), rect=pygame.Rect(0, 0, 0, 0), width=0):
        self.color = color
        self.rect = rect
        self.width = width

class ChangePosition:
    current = None

    def __init__(self, target=(0,0), time=0, interp=interpolation.InterpolationBase(), chain=None, *args):
        self.target = target
        self.time = time
        self.interp = interp
        self.chain = chain
        self.args = args

class ChangeSize:
    current = None

    def __init__(self, target=1, time=0, interp=interpolation.InterpolationBase(), chain=None, *args):
        self.target = target
        self.time = time
        self.interp = interp
        self.chain = chain
        self.args = args
