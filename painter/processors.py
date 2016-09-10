import pygame
import esper
import components

class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, filtered_events, pressed_keys, dt, screen):
        screen.fill((0, 0, 0))
        for ent, (i, p, s) in self.world.get_components(components.Image, components.Position, components.Size):
            screen.blit(i.image, (p.x - s.width // 2, p.y - s.height // 2))

class ClickProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, filtered_events, pressed_keys, dt, screen):
        for event in filtered_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for ent, (s, p, c) in self.world.get_components(components.Size, components.Position, components.Click):
                    if p.x - s.width // 2 <= x and p.x + s.width // 2 >= x and p.y - s.height // 2 <= y and p.y + s.height // 2 >= y:
                        c.run()

class OverProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, filtered_events, pressed_keys, dt, screen):
        for event in filtered_events:
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                for ent, (s, p, o) in self.world.get_components(components.Size, components.Position, components.Over):
                    if p.x - s.width // 2 <= x and p.x + s.width // 2 >= x and p.y - s.height // 2 <= y and p.y + s.height // 2 >= y:
                        if not o.active:
                            o.enterf(ent)
                            o.active = True
                    elif o.active:
                        o.exitf(ent)
                        o.active = False
