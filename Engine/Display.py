import pygame
from Engine import Config

class Display:
    def __init__(self, engine):
        self.engine = engine
        self.surface = pygame.display.set_mode(Config.get_screensize())
        self.back_buffer = pygame.Surface(Config.get_screensize())
        #self.video_scale = Config.get_video_scale()

    def get_buffer(self):
        return self.back_buffer

    def clear_buffer(self):
        self.back_buffer.fill((0, 0, 0))

    def render(self):
        screen = self.back_buffer
        w, h = self.back_buffer.get_size()
        # if self.video_scale != 1:
        #     if self.video_scale == 2:
        #         screen = pygame.transform.scale2x(screen)
        #     else:
        #         screen = pygame.transform.scale(screen, (int(w * self.video_scale), int(h * self.video_scale)))
        self.surface.blit(screen, (0, 0))