class SceneBase:
    def __init__(self):
        self.next = self

    def init(self):
        print("uh-oh, you didn't override this in the child class")

    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self, dt):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        if next_scene is not None:
            next_scene.init()
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)
