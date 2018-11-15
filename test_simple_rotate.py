import pygame
from Engine.Engine import Engine
from Engine.AssetManager import load_image

class GameObject(object):
    def __init__(self):
        self.test_image = load_image("enemy.png")
        self.degrees = 0
        self.last_move = 0

    def draw(self, canvas):
        canvas.blit(self.test_image, (0, 0))

        rot_image = self.rot_center(self.test_image, self.degrees)
        canvas.blit(rot_image, (200, 200))

    def get_angle(self, origin, target):
        dx = target.x - origin.x
        dy = target.y - origin.y
        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi
        degs = math.degrees(rads)
        return int(degs)

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self, dt):
        self.last_move += dt
        if self.last_move > 100:
            self.degrees += 1
            if self.degrees > 359:
                self.degrees = 0
            self.last_move = 0

    def handle_event(self, event):
        pass


if __name__ == '__main__':
    e = Engine(GameObject)
    e.game_loop()