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
        self.font = pygame.font.Font("RobotoMono-Regular.ttf", 24)
        self.titlefont = pygame.font.Font("RobotoMono-Regular.ttf", 48)

        def start_game():
            self.SwitchToScene(self)

        def quit_game():
            self.Terminate()

        def highlight(entity):
            t = self.world.component_for_entity(entity, components.Text)
            image = t.font.render("> " + t.text + " <", True, (128, 0, 128))
            self.world.component_for_entity(entity, components.Image).image = image
            size = self.world.component_for_entity(entity, components.Size)
            size.width = image.get_width()
            size.height = image.get_height()

        def lowlight(entity):
            t = self.world.component_for_entity(entity, components.Text)
            image = t.font.render(t.text, True, t.color)
            self.world.component_for_entity(entity, components.Image).image = image
            size = self.world.component_for_entity(entity, components.Size)
            size.width = image.get_width()
            size.height = image.get_height()

        def go_down(circle, idx):
            self.world.add_component(circle, components.ChangePosition((640 - ((idx - 2) * 50), 400), 1, interpolation.Circle(), go_up, circle, idx))

        def go_up(circle, idx):
            self.world.add_component(circle, components.ChangePosition((640 - ((idx - 2) * 50), 320), 1, interpolation.Circle(), go_down, circle, idx))

        start = self.world.create_entity()
        image = self.font.render("start", True, (0, 128, 0))
        self.world.add_component(start, components.Position(640, 480))
        self.world.add_component(start, components.Text("start", self.font))
        self.world.add_component(start, components.Image(image))
        self.world.add_component(start, components.Size(image.get_width(), image.get_height()))
        self.world.add_component(start, components.Click(start_game))
        self.world.add_component(start, components.Over(highlight, lowlight))

        quitbutton = self.world.create_entity()
        image = self.font.render("quit", True, (0, 128, 0))
        self.world.add_component(quitbutton, components.Position(640, 520))
        self.world.add_component(quitbutton, components.Text("quit", self.font))
        self.world.add_component(quitbutton, components.Image(image))
        self.world.add_component(quitbutton, components.Size(image.get_width(), image.get_height()))
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
            self.world.add_component(circle, components.Position(640 - ((idx - 2) * 50), 320))
            self.world.add_component(circle, components.Circle(val, 10))
            self.world.add_component(circle, components.Over(None))
            go_down(circle, idx)

        self.world.add_processor(processors.ClickProcessor())
        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.OverProcessor())
        self.world.add_processor(processors.PositionAnimator())
        self.world.add_processor(processors.SizeAnimator())
