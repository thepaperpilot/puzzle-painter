import scenebase
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

        def quit_game():
            self.Terminate()

        def highlight(entity):
            t = self.world.component_for_entity(entity, components.Text)
            image = t.font.render("> " + t.text + " <", True, (128, 0, 128))
            self.world.component_for_entity(entity, components.Image).image = image
            size = self.world.component_for_entity(entity, components.Size)
            size.width = image.get_width()
            size.height = image.get_height()
            self.world.add_component(entity, components.ChangeSize(1, .25, interpolation.Smooth()))

        def lowlight(entity):
            t = self.world.component_for_entity(entity, components.Text)
            image = t.font.render(t.text, True, t.color)
            self.world.component_for_entity(entity, components.Image).image = image
            size = self.world.component_for_entity(entity, components.Size)
            size.width = image.get_width()
            size.height = image.get_height()
            self.world.add_component(entity, components.ChangeSize(.5, .25, interpolation.Smooth()))

        def start_circle(circle):
            self.world.add_component(circle, components.CircleAnimation(200, 2, True))

        start = self.world.create_entity()
        image = self.font.render("start", True, (0, 128, 0))
        self.world.add_component(start, components.Position(640, 480))
        self.world.add_component(start, components.Text("start", self.font))
        self.world.add_component(start, components.Image(image))
        self.world.add_component(start, components.Size(image.get_width(), image.get_height(), .5))
        self.world.add_component(start, components.Click(start_game))
        self.world.add_component(start, components.Over(highlight, lowlight))

        quitbutton = self.world.create_entity()
        image = self.font.render("quit", True, (0, 128, 0))
        self.world.add_component(quitbutton, components.Position(640, 540))
        self.world.add_component(quitbutton, components.Text("quit", self.font))
        self.world.add_component(quitbutton, components.Image(image))
        self.world.add_component(quitbutton, components.Size(image.get_width(), image.get_height(), .5))
        self.world.add_component(quitbutton, components.Click(quit_game))
        self.world.add_component(quitbutton, components.Over(highlight, lowlight))

        title = self.world.create_entity()
        image = self.titlefont.render("Puzzle Painter", True, (0, 128, 0))
        self.world.add_component(title, components.Position(640, 240))
        self.world.add_component(title, components.Text("Puzzle Painter", self.titlefont))
        self.world.add_component(title, components.Image(image))
        self.world.add_component(title, components.Size(image.get_width(), image.get_height()))

        for idx, val in enumerate([(119, 190, 119), (119, 158, 203), (255, 179, 71), (150, 111, 214), (255, 105, 97)]):
            circle = self.world.create_entity()
            self.world.add_component(circle, components.Position(640, 300))
            self.world.add_component(circle, components.Circle(val, 10))
            self.world.add_component(circle, components.Over(None))
            self.world.add_component(circle, components.Velocity())
            self.world.add_component(circle, components.Delay(idx * 2/5, start_circle, circle))

        self.world.add_processor(processors.ClickProcessor())
        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.OverProcessor())
        self.world.add_processor(processors.VelocityProcessor())
        self.world.add_processor(processors.AnimationProcessor())
