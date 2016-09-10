class Position:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class Size:
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
