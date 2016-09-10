import pygame
import esper
import components

class RenderProcessor(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

    def process(self, filtered_events, pressed_keys, dt, screen):
        screen.fill((0, 0, 0))
        for ent, (i, p, s) in self.world.get_components(components.Image, components.Position, components.Size):
            if s.scale is 1:
                screen.blit(i.image, (p.x - s.width // 2, p.y - s.height // 2))
            else:
                image = pygame.transform.scale(i.image, (int(s.width * s.scale), int(s.height * s.scale)))
                screen.blit(image, (p.x - s.width * s.scale // 2, p.y - s.height * s.scale // 2))
        for ent, (c, p) in self.world.get_components(components.Circle, components.Position):
            pygame.draw.circle(screen, c.color, (int(p.x), int(p.y)), c.radius, c.width)
        for ent, (r, p) in self.world.get_components(components.Rect, components.Position):
            pygame.draw.rect(screen, c.color, r.rect)

class ClickProcessor(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

    def process(self, filtered_events, pressed_keys, dt, screen):
        for event in filtered_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for ent, (s, p, c) in self.world.get_components(components.Size, components.Position, components.Click):
                    if p.x - s.width // 2 <= x and p.x + s.width // 2 >= x and p.y - s.height // 2 <= y and p.y + s.height // 2 >= y:
                        c.run()

class OverProcessor(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

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

class PositionAnimator(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

    def process(self, filtered_events, pressed_keys, dt, screen):
        for ent, (p, c) in self.world.get_components(components.Position, components.ChangePosition):
            if c.current is None:
                c.current = dt
                c.original = (p.x, p.y)
            else:
                c.current += dt

            if c.current >= c.time:
                x,y = c.target
                self.world.remove_component(ent, components.ChangePosition)
                c.chain(*c.args)
            else:
                x,y = c.target
                ox, oy = c.original
                x = x * c.interp.apply(c.current / c.time) + ox * (1 - c.interp.apply(c.current / c.time))
                y = y * c.interp.apply(c.current / c.time) + oy * (1 - c.interp.apply(c.current / c.time))

            p.x = x
            p.y = y

class SizeAnimator(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

    def process(self, filtered_events, pressed_keys, dt, screen):
        for ent, (s, c) in self.world.get_components(components.Size, components.ChangeSize):
            if not c.current:
                c.current = dt
                c.original = s.scale
            else:
                c.current += dt

            if c.current >= c.time:
                scale = c.target
                self.world.remove_component(ent, components.ChangeSize)
                if c.chain:
                    c.chain(*c.args)
            else:
                scale = c.target * c.interp.apply(c.current / c.time) + c.original * (1 - c.interp.apply(c.current / c.time))

            s.scale = scale
