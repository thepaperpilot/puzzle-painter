import scenebase
import math
import pygame
import esper
import components
import processors
import interpolation

class TitleScene(scenebase.SceneBase):
    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        self.font = pygame.font.Font("RobotoMono-Regular.ttf", 42)
        self.titlefont = pygame.font.Font("RobotoMono-Regular.ttf", 72)

        def start_game():
            for ent, c in self.world.get_component(components.CircleAnimation):
                c.loop = False
                c.chain = move_to_bottom
            for ent in [start, quitbutton, title]:
                pos = self.world.component_for_entity(ent, components.Position)
                self.world.add_component(ent, components.ChangePosition((pos.x, pos.y + 100), 1))
                self.world.add_component(ent, components.ChangeAlpha(1, 0, 1))
            def change_scene():
                print("TODO: game screen")
            next_scene = self.world.create_entity()
            self.world.add_component(next_scene, components.Delay(2, change_scene))

        def quit_game():
            self.Terminate()

        def highlight(entity):
            t = self.world.component_for_entity(entity, components.Text)
            image = t.font.render("> " + t.text + " <", False, (128, 0, 128))
            self.world.component_for_entity(entity, components.Image).image = image
            size = self.world.component_for_entity(entity, components.Size)
            size.width = image.get_width()
            size.height = image.get_height()
            self.world.add_component(entity, components.ChangeSize(1, .25, interpolation.Smooth()))

        def lowlight(entity):
            t = self.world.component_for_entity(entity, components.Text)
            image = t.font.render(t.text, False, t.color)
            self.world.component_for_entity(entity, components.Image).image = image
            size = self.world.component_for_entity(entity, components.Size)
            size.width = image.get_width()
            size.height = image.get_height()
            self.world.add_component(entity, components.ChangeSize(.5, .25, interpolation.Smooth()))

        def start_circle(circle, idx):
            self.world.add_component(circle, components.CircleAnimation(400, 1, math.pi * (1.25 + .15 * idx), True, None, circle, idx))

        def move_to_bottom(circle, idx):
            self.world.add_component(circle, components.ChangePosition((16 + 250 * idx, 16), .5))

        start = self.world.create_entity()
        image = self.font.render("start", False, (0, 128, 0))
        self.world.add_component(start, components.Position(640, 480))
        self.world.add_component(start, components.Text("start", self.font))
        self.world.add_component(start, components.Image(image=image))
        self.world.add_component(start, components.Size(image.get_width(), image.get_height(), .5))
        self.world.add_component(start, components.Click(start_game))
        self.world.add_component(start, components.Over(highlight, lowlight))

        quitbutton = self.world.create_entity()
        image = self.font.render("quit", False, (0, 128, 0))
        self.world.add_component(quitbutton, components.Position(640, 540))
        self.world.add_component(quitbutton, components.Text("quit", self.font))
        self.world.add_component(quitbutton, components.Image(image=image))
        self.world.add_component(quitbutton, components.Size(image.get_width(), image.get_height(), .5))
        self.world.add_component(quitbutton, components.Click(quit_game))
        self.world.add_component(quitbutton, components.Over(highlight, lowlight))

        title = self.world.create_entity()
        image = self.titlefont.render("Puzzle Painter", False, (0, 128, 0))
        self.world.add_component(title, components.Position(640, 240))
        self.world.add_component(title, components.Text("Puzzle Painter", self.titlefont))
        self.world.add_component(title, components.Image(image=image))
        self.world.add_component(title, components.Size(image.get_width(), image.get_height()))

        for idx, val in enumerate(["blue", "green", "orange", "purple", "red"]):
            circle = self.world.create_entity()
            self.world.add_component(circle, components.Position(640, 300))
            self.world.add_component(circle, components.Image("pastel" + val + ".png"))
            self.world.add_component(circle, components.Size(16, 16))
            self.world.add_component(circle, components.Velocity())
            self.world.add_component(circle, components.Delay(idx / 5, start_circle, circle, idx))

        self.world.add_processor(processors.ClickProcessor(), priority=10)
        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.OverProcessor(), priority=10)
        self.world.add_processor(processors.VelocityProcessor(), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
