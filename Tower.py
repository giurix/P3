import sys
import pygame
import math
from Engine.AssetManager import load_image


def distance(obj1, obj2):
    try:
        return math.hypot(obj2[0] - obj1[0], obj2[1] - obj1[1])
    except TypeError:
        #enemy
        return math.hypot(obj2.x - obj1.x, obj2.y - obj1.y)

class Bullet(object):
    def __init__(self, movement, target, tower):
        self.target = target
        self.tower = tower
        self.image = load_image("bullet.png")
        self.active = True
        self.x = tower.get_rect().centerx
        self.y = tower.get_rect().centery
        self.damage = 3
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.movement = movement

    def draw(self, canvas):
        canvas.blit(self.image, (self.x, self.y))

    def update(self, dt):
        if self.target.get_rect().colliderect(self.get_rect()):
            #we hit our target
            self.target.take_damage(self.damage, self.tower)
            self.active = False
        else:
            self.x += self.movement[0] * dt
            self.y += self.movement[1] * dt

    def handle_event(self, event):
        pass

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class BasicTower(object):
    def __init__(self, x, y, slot, game):
        self.game = game
        self.default_direction = None
        self.x = x
        self.y = y
        self.attack_range = 200
        self.damage = 10
        self.fire_rate = 1000
        self.attacking = False
        self.target = None
        self.angle = 0
        self.image = load_image("tower.png")
        self.rotated_image = self.image
        self.image_rect = self.image.get_rect()
        self.draw_range_circle = True
        self.last_image_update = 0
        self.last_image_update_max = 10
        self.attack_timer = 0
        self.bullets = []
        self.set_default_direction(slot)

    def set_default_direction(self, slot):
        if slot.facing == "down":
            self.default_direction = 270
        elif slot.facing == "up":
            self.default_direction = 90
        elif slot.facing == "left":
            self.default_direction = 180
        elif slot.facing == "right":
            self.default_direction = 0
        self.angle = self.default_direction
     #   self.update_image_rotation()

    def fire_cannon(self):
        speed = 0.2
        if self.target:
            if self.attack_timer > self.fire_rate:
                self.attack_timer = 0
                b_angle = self.get_angle(self, self.target)
                b_rads = math.radians(b_angle)
                bdx = speed * math.cos(b_rads)
                bdy = speed * math.sin(b_rads)
                b = Bullet([bdx, -bdy], self.target, self)
                self.bullets.append(b)

    def draw(self, canvas):
        canvas.blit(self.rotated_image, (self.x, self.y))
        if self.draw_range_circle:
            pygame.draw.circle(canvas, (255, 255, 255), (self.x + int((self.image_rect.width / 2)), self.y + int((self.image_rect.height / 2))), self.attack_range, 1)
        for b in self.bullets:
            b.draw(canvas)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image_rect.width, self.image_rect.height)

    def update(self, dt):
        #update attack timer
        self.attack_timer += dt

        #if we don't have a target, search for one
        if not self.target:
            self.set_target(self.scan_for_enemies())
        
        #do we have a target?
        if self.target:
            #if so, is it in range
            if not self.in_range(self.target):
                print("Target out of range, setting to none")
                self.target = None
        #update bullets
        for b in self.bullets:
            b.update(dt)

        self.fire_cannon()
        self.clear_dead_bullets()
     #   self.update_image(dt)
        
    def clear_dead_bullets(self):
        old_bullets = []
        for i, b in enumerate(self.bullets):
            if not b.active:
                old_bullets.append(i)
        for o in reversed(old_bullets):
            del self.bullets[o]

    def in_range(self, obj):
        dist = distance(self, obj)
        if dist > self.attack_range:
            return False
        return True

    def get_angle(self, origin, target):
        dx = target.x - origin.x
        dy = target.y - origin.y
        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi
        degs = math.degrees(rads)

        return int(degs)

 #   def update_image_rotation(self):
  #      old_center = self.image.get_rect().center
   #     rotated_image = self.rot_center(self.image, self.angle)
    #    self.rotated_image = rotated_image
     #   self.rotated_image.get_rect().center = old_center

#    def update_image(self, dt):
 #       self.last_image_update += dt
  #      if self.last_image_update > self.last_image_update_max:
   #         self.last_image_update = 0
    #        if self.target:
     #           self.angle = self.get_angle(self, self.target)
      #          print("Angle: {}".format(self.angle))
       #         self.update_image_rotation()
        #    else:
         #       #we don't have a target, reset
          #      if self.angle > self.default_direction:
           #         self.angle -= 1
            #    elif self.angle < self.default_direction:
             #       self.angle += 1
              #  self.update_image_rotation()

    def handle_event(self, event):
        pass

    def set_target(self, target):
        print("Setting Target")
        self.target = target

 #  def rot_center(self, image, angle):
  #      """rotate an image while keeping its center and size"""
   #     print("Rotating image by angle: {}".format(angle))
    #    orig_rect = image.get_rect()
     #   rot_image = pygame.transform.rotate(image, angle)
      #  rot_rect = orig_rect.copy()
       # rot_rect.center = rot_image.get_rect().center
        #rot_image = rot_image.subsurface(rot_rect).copy()
        #return rot_image

    def scan_for_enemies(self):
        found = None
        closest = sys.maxsize
        for enemy in self.game.get_enemy_list():
            e_dist = distance(self.get_rect(), enemy.get_rect())
            if e_dist < closest and e_dist < self.attack_range:
                found = enemy
                closest = e_dist
        print("Found: {}".format(found))
        return found

    def target_died(self):
        print("Tower got message that target has died")
        self.target = None


class TowerSlot(object):
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.surface = load_image("open_spot.png")


    def draw(self, canvas):
        r = self.surface.get_rect()
        
        canvas.blit(self.surface, (self.x, self.y))
        
    def get_rect(self):
        i = self.surface.get_rect()
        return pygame.Rect(self.x, self.y, i.width, i.height)

    def update(self, dt):
        pass

    def handle_event(self, event):
        pass