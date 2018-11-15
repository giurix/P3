class SceneManager:
    def __init__(self, game):
        self.game = game
        self.scenes = {}

        # Our current scene, this is what we call each frame for updating, etc
        self.current_scene = None

    def add_scene(self, scene_name, scene_obj):
        self.scenes[scene_name] = scene_obj(self)

    def change_scene(self, new_scene, data = None):
        #new_scene should be a string that is the key in the scenes dict
        if new_scene in self.scenes.keys():
            #if we have a current scene, we want to tell it that its
            #no longer going to be the current scene
            if self.current_scene:
                self.current_scene.deactivate()

            #set the current_scene to the scene passed
            self.current_scene = self.scenes[new_scene]
            #give the new scene any data that the old scene might have sent it
            self.current_scene.activate(data)
        else:
            print("Unable to switch to scene " + new_scene)
            return False

    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self, canvas):
        if self.current_scene:
            self.current_scene.draw(canvas)