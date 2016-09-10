import esper

class SceneBase:
    world = esper.World()

    def __init__(self):
        self.next = self

    def init(self):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        if next_scene is not None:
            next_scene.init()
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)
