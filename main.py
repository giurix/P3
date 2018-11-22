import sys
import pygame
import math
from Engine.Engine import Engine
from Engine.AssetManager import load_image
from Engine.Config import set_screensize, get_screenrect
from Engine.Text import text_surface
from Enemy import Enemy
from Tower import BasicTower, TowerSlot
from Tower2 import BasicTower2, TowerSlot
from random import randint


class Game(object):
    def __init__(self):
        self.money= 500
        self.irand= randint(3, 10)
        self.screenrect = get_screenrect()
        self.surface = pygame.Surface((1280, 720))
        self.background_image = load_image("bg.png")
        self.surface.blit(self.background_image, (0, 0))
        self.game_timer = 0
        self.wave_times2 = [[100]]
        self.wave_times = [
            [100, 1000, 1500, 2500, 3000, 6000],
            [100, 500, 1000],
            [100, 500, 1300, 2400]
        ]
        self.wave_time_index = 0
        self.money_index = 500
        self.current_wave = self.wave_times[self.wave_time_index]
        self.current_wave_completed = False
        self.current_wave_index = 0
        self.tower_pos = [
            [150, 50, "down"],
            [150, 120, "down"],

        ]
        self.slots = []
        self.towers = []
        self.waypoint_list = [
            [100, 0],
            [100, 620],
            [400, 620],
            [400, 100],
            [700, 100],
            [700, 620],
            [1000, 620],
            [1000, 100],
            [1280, 100]
        ]
        self.enemies = []
        self.spawned = 0
        self.killed = 0
        self.wave_text = text_surface("Wave: 1", font_size=24)
        self.money_text = text_surface("Danish Dollars: 500", font_size=24)
        self.health_index = 100
        self.health_text = text_surface("Health: 100", font_size=24)
        self.post_init()
        self.lost = text_surface("YOU LOST!", font_size=50)


    def update_health_text(self):
        self.health_text = text_surface("Health: " + str(self.health_index), font_size=24)


    def game_over(self):
        self.surface.fill(0,0,0)
        self.surface.blit(self.lost,(640,360))


    def spawn_enemy(self):
        enemy = Enemy(self, self.waypoint_list[0])
        self.enemies.append(enemy)
        self.spawned += 1

    def get_enemy_list(self):
        return list(self.enemies)

    def post_init(self):
        for spot in self.tower_pos:
            ts = TowerSlot(spot[0], spot[1], spot[2])
            self.slots.append(ts)

    def draw_waypoints(self, canvas):
        for index, point in enumerate(self.waypoint_list):
            if len(self.waypoint_list) > index + 1:
                pygame.draw.line(canvas, (238, 239, 154), self.waypoint_list[index], self.waypoint_list[index + 1])

    def get_next_waypoint(self, waypoint):
        for index, w in enumerate(self.waypoint_list):
            if w[0] == waypoint[0] and w[1] == waypoint[1]:
                if len(self.waypoint_list) > index + 1:
                    return self.waypoint_list[index + 1]
                else:
                    return None
        return None

    def draw(self, canvas):
        canvas.blit(self.surface, (0, 0))
        for slot in self.slots:
            slot.draw(canvas)
        for tower in self.towers:
            tower.draw(canvas)
        self.draw_waypoints(canvas)
        for e in self.enemies:
            e.draw(canvas)
        canvas.blit(self.wave_text, (0, 0))
        canvas.blit(self.money_text, (0,40))
        canvas.blit(self.health_text, (0, 20))
        if self.health_index <= 0:
            canvas.fill(0)
            canvas.blit(self.lost, (640, 360))
            #canvas.blit(self.lost, (500,500))

    def enemy_has_been_killed(self):
        self.killed += 1
        self.money += 50

    def update_wave_label(self):
        self.wave_text = text_surface("Wave: {}".format(self.wave_time_index), font_size=24)
    def update_money_label(self):
        self.money_text = text_surface("Danish Dollars: " + str(self.money_index), font_size=24)
    def load_wave(self):
        pass

    def update(self, dt):
        for t in self.towers:
            t.update(dt)

        delete_list = []
        for i, e in enumerate(self.enemies):
            e.update(dt)
            if not e.active:
                print("Adding enemy to delete list")
             #   self.health_index = self.health_index - 1
             #   self.update_health_text()
             #  print("Health minus 1")
                delete_list.append(i)
        if delete_list:
            for d in reversed(delete_list):
                del self.enemies[d]
                self.enemy_has_been_killed()

        self.game_timer += dt

        if self.current_wave:
            # we have an active wave, so, we need to see if we need to spawn an enemy
            if self.game_timer > self.current_wave[self.current_wave_index]:
                # our game timer was greater than the next value in the spawn list
                # check if our wave is completed, if its not completed
                if not self.current_wave_completed:
                    self.spawn_enemy()

                # after spawning enemy, see if we can go to the next time to spawn in our wave
                if len(self.current_wave) > self.current_wave_index + 1:
                    # we have another enemy to spawn, setting our index to it
                    self.current_wave_index += 1
                else:
                    self.current_wave_completed = True
                    # we don't have any more timers in our list to spawn enemies from
                    # we need to move to the next wave or end the game
                    # print("We are done with this wave", self.game_timer)

                    if self.spawned == self.killed:
                        # print("Spawned = Killed: {} {}".format(self.spawned, self.killed))
                        if len(self.wave_times) > self.wave_time_index + 1:
                            self.wave_time_index += 1
                            self.current_wave = self.wave_times[self.wave_time_index]
                            self.current_wave_index = 0
                            self.game_timer = 10
                            self.health_index = self.health_index - self.killed
                            self.update_health_text()
                            print("Health minus 1")
                            self.current_wave_completed = False

                            self.update_wave_label()
                        else:
                            print("You win!")
                            self.current_wave = None
                    else:
                        pass
                        # print("Spawned != Killed: {} {}".format(self.spawned, self.killed))

    def can_buy_tower(self):
        if self.money_index > 0:
            return True

    def create_tower(self, base_pos, base):
        new_tower = BasicTower(base_pos[0], base_pos[1], base, self)
        for index, slot in enumerate(self.slots):
            if slot.x == base_pos[0] and slot.y == base_pos[1]:
                print("Found the tower")
                self.slots[index].tower = True
                self.towers.append(new_tower)

    def create_tower2(self, base_pos, base):
        new_tower = BasicTower2(base_pos[0], base_pos[1], base, self)
        for index, slot in enumerate(self.slots):
            if slot.x == base_pos[0] and slot.y == base_pos[1]:
                print("Found the tower")
                self.slots[index].tower = True
                self.towers.append(new_tower)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.can_buy_tower() == True:
                for tower_base in self.slots:
                    if tower_base.get_rect().collidepoint(event.pos):
                        if self.irand <= 5:
                            self.create_tower((tower_base.x, tower_base.y), tower_base)
                            self.irand = randint(5, 10)
                            self.money_index= self.money_index - 50
                            self.update_money_label()

                        elif self.irand > 5:
                            self.create_tower2((tower_base.x, tower_base.y), tower_base)
                            self.irand = randint(0, 10)
                            self.money_index= self.money_index - 100
                            self.update_money_label()



if __name__ == '__main__':
    set_screensize(1280, 720)
    e = Engine(Game)
    e.game_loop()

