import scenebase
import pygame
import util

class TitleScene(scenebase.SceneBase):
    is_blue = True
    x = 610
    y = 330
    radius = 15
    mousex = 0
    mousey = 0
    mode = 'blue'
    points = []

    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        self.font = pygame.font.Font("RobotoMono-Regular.ttf", 24)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_blue = not self.is_blue
                    self.x = 610
                    self.y = 330
                elif event.key == pygame.K_q:
                    self.Terminate()
                elif event.key == pygame.K_r:
                    self.mode = 'red'
                elif event.key == pygame.K_g:
                    self.mode = 'green'
                elif event.key == pygame.K_b:
                    self.mode = 'blue'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click grows radius
                    self.radius = min(200, self.radius + 1)
                elif event.button == 3: # right click shrinks radius
                    self.radius = max(1, self.radius - 1)
            elif event.type == pygame.MOUSEMOTION:
                # if mouse moved, add point to list
                position = event.pos
                self.points = self.points + [position]
                self.points = self.points[-256:]

    def Update(self, dt):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: self.y -= dt
        if pressed[pygame.K_DOWN]: self.y += dt
        if pressed[pygame.K_LEFT]: self.x -= dt
        if pressed[pygame.K_RIGHT]: self.x += dt
        self.dt = dt

    def Render(self, screen):
        screen.fill((0, 0, 0))
        if self.is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, 60, 60))
        text = self.font.render("FPS: " + str(int(1000*1//self.dt)), True, (0, 128, 0))
        screen.blit(text, (10, 10))
        util.render_text(screen, self.font, "press 1,2, or 3 to change framerates", 640, 720 - 90)
        util.render_text(screen, self.font, "press space to change colors and reset position, arrows to move", 640, 720 - 60)
        util.render_text(screen, self.font, "press q to exit", 640, 720 - 30)

        i = 0
        while i < len(self.points) - 1:
            drawLineBetween(screen, i, self.points[i], self.points[i + 1], self.radius, self.mode)
            i += 1

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in xrange(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)
