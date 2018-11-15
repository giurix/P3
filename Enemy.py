import pygame
from Engine.AssetManager import load_image
from Engine.Text import text_surface

class Enemy(object):
    def __init__(self, game, waypoint):
        self.game = game
        self.walking_speed = 0.08
        self.max_hp = 40
        self.current_hp = 40
        self.next_waypoint = self.game.get_next_waypoint(waypoint)
        self.image = load_image("enemy.png")
        self.info_layer = pygame.Surface((self.image.get_rect().width, self.image.get_rect().height), pygame.SRCALPHA)
        self.x = waypoint[0] - (self.image.get_rect().width / 2)
        self.y = waypoint[1] - (self.image.get_rect().height / 2)
        self.active = True
        self.attacked_by = []

    def take_damage(self, damage, tower):
        print("I took some damage: {}".format(damage))
        self.current_hp -= damage
        self.update_image()
        if self.current_hp < 0:
            self.active = False
            tower.target_died()

    def update_image(self):
        self.info_layer.fill((0, 0, 0, 1.0))
        hp_text = text_surface(self.current_hp, font_size=18)
        self.info_layer.blit(hp_text, (0, 0))

    def draw(self, canvas):
        if self.active:
            canvas.blit(self.image, (self.x, self.y))
            canvas.blit(self.info_layer, (self.x, self.y))

    def is_in_range(self, point):
        r = self.get_rect()
        dx = abs(r.centerx - point[0])
        dy = abs(r.centery - point[1])
        if dx < 8 and dy < 8:
            return True
        return False

    def get_rect(self):
        image_rect = self.image.get_rect()
        return pygame.Rect(self.x, self.y, image_rect.width, image_rect.height)

    def update(self, dt):
        if self.active:
            move = [0, 0]
            if self.is_in_range(self.next_waypoint):
                #set new waypoint, not there yet though
                print("Found waypoint {}, getting next one".format(self.next_waypoint))
                self.next_waypoint = self.game.get_next_waypoint(self.next_waypoint)
                if not self.next_waypoint:
                    self.active = False
                print("New Waypoint: {}".format(self.next_waypoint))
            else:
                #move closer to waypoint
                current = self.get_rect().center
                dx = current[0] - self.next_waypoint[0]
                dy = current[1] - self.next_waypoint[1]
                if dx < 0:
                    #move right
                    move[0] = self.walking_speed * dt
                elif dx > 0:
                    #move left
                    move[0] = -(self.walking_speed * dt)
                if dy < 0:
                    #move down
                    move[1] = self.walking_speed * dt
                elif dy > 0:
                    move[1] = -(self.walking_speed * dt)
            self.x += move[0]
            self.y += move[1]

    def handle_event(self, event):
        pass