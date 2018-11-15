import pygame

class Input:
    def __init__(self, engine):
        self.engine = engine
        pygame.key.set_repeat(200, 200)

    def handle_events(self):
        """
        Main event handler
        This will check for quit events (including escape) and shut the game
        down if found.  If its anything but a quit event we send it to the
        handle_event method in the engine object
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.engine.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.engine.running = False
                else:
                    self.engine.handle_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.engine.handle_event(event)
            elif event.type == pygame.KEYUP:
                self.engine.handle_event(event)