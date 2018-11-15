import pygame
from Engine.Display import Display
from Engine.Input import Input

class Engine():
    """
    Pygame based game engine
    """
    def __init__(self, game_manager):
        """
        game_manager needs to be a reference to a class that can handle the game
        so it does the actual work when update, draw and handle_events are called
        """
        pygame.init()

        #setting up objects to handle the display and input events
        self.display = Display(self)
        self.input = Input(self)

        #time and speed
        self.clock = pygame.time.Clock()
        self.fps = 60

        #controls if game is quit or not
        self.running = False 

        #this is the object that handles the game itself
        self.game_manager = game_manager()

    def handle_event(self, event):
        """
        If the event wasn't a quit event
        we tell the game manager to handle it
        """
        self.game_manager.handle_event(event)

    def update(self):
        """
        Sends the delta time to the update method of the game manager
        This in turn updates everything that needs it
        """
        self.game_manager.update(self.clock.get_time())

    def draw(self):
        """
        Main draw command send to the game manager
        """
        self.game_manager.draw(self.display.get_buffer())

    def game_loop(self):
        """
        Main game loop
        """
        self.running = True
        while self.running:
            self.display.clear_buffer()
            self.input.handle_events()
            self.update()
            self.draw()
            self.display.render()
            pygame.display.flip()
            self.clock.tick(self.fps)
