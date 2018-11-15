from __future__ import print_function
import math
import random

class Vector2d:
    def __init__(self, x_or_pos, y = None):
        try:
            if len(x_or_pos) == 2 and not y:
                self.x = float(x_or_pos[0])
                self.y = float(x_or_pos[1])
        except TypeError:
            try:
                self.x = float(x_or_pos)
                self.y = float(y)
            except ValueError:
                raise Exception('Bad values sent to Vector2d', x_or_pos, y)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            return False

    def __add__(self, other):
        if isinstance(other, Vector2d):
            return Vector2d(self.x + other.x, self.y + other.y)
        else:
            try:
                return Vector2d(self.x + other[0], self.y + other[1])
            except IndexError:
                return False

    def add(self, other):
        # try:
        #     self.x += other[0]
        #     self.y += other[1]
        # except IndexError:
        #     return False
        return self.__add__(other)

    def sub(self, other):
        try:
            self.x -= other[0]
            self.y -= other[1]
        except IndexError:
            return False

    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        mag = self.mag()
        if mag:
            self.x /= mag
            self.y /= mag

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def limit(self, size):
        if self.x > size:
            self.x = size
        if self.y > size:
            self.y = size

    def pos(self):
        return (int(self.x), int(self.y))

    def __mul__(self, num):
        self.x *= num
        self.y *= num

    def mult(self, num):
        self.__mul__(num)
        

    @staticmethod
    def random2d():
        return Vector2d(random.random(), random.random())

def main():
    location = Vector2d(100, 100)
    velocity = Vector2d(2, 10)
    print("Location:" + str(location))
    #location.add(velocity)
    location += velocity
    print("Location after update:", str(location))
    print("Vector Magnitude:", str(location.mag()))
    velocity.normalize()
    print("Velocity Normalized:", str(velocity))

if __name__ == '__main__':
    main()