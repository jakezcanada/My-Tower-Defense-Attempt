import pygame
import os
import math
import time
from .tower import Tower

class Cannon(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.tower_imgs = []
        self.cannon_imgs = []
        self.cannon_count = 0
        self.range = 100
        self.inRange = False
        self.pointx=self.x
        self.pointy=self.y+100
        self.closest_enemy = None;
        self.turnAngle = 0
        self.damage = 0.75
        self.attack_speed = 3
        for x in range(3):
            self.tower_imgs.append(pygame.transform.scale(
                pygame.image.load(os.path.join("game_assets/towers/cannon", "CannonBase" + str(x) + ".png")),
                (52, 52)))
        for x in range(5):
            self.cannon_imgs.append(pygame.transform.scale(
                pygame.image.load(os.path.join("game_assets/towers/cannon", "Cannon" + str(x) + ".png")),
                (52, 52)))

    def getAngle(self, a, b, c):
        ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
        return ang + 360 if ang < 0 else ang

    def rot_center(self, image, angle):
        """rotate a Surface, maintaining position."""

        loc = image.get_rect().center  # rot_image is not defined
        rot_sprite = pygame.transform.rotate(image, angle)
        rot_sprite.get_rect().center = loc
        return rot_sprite
    def draw(self, win):
        circle_surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(circle_surface, (128,128,128, 100), (self.range, self.range), self.range, 0)

        win.blit(circle_surface, (self.x - self.range, self.y - self.range))
        super().draw(win)
        super().draw(win)
        if self.inRange:
            self.cannon_count +=1
            """
            get distance between 2 points, dist = math.hypot(x1-x2, y1-y2)
            get new line length
            """
            enemy = self.closest_enemy
            self.turnAngle = self.getAngle([enemy.x,enemy.y],[self.x,self.y],[self.pointx,self.pointy])
            if self.cannon_count >= len(self.cannon_imgs) * self.attack_speed:
               self.cannon_count = 0
        elif self.cannon_count != 0:
            self.cannon_count += 1
            if self.cannon_count >= len(self.cannon_imgs) * self.attack_speed:
                self.cannon_count = 0
        cannon = self.cannon_imgs[self.cannon_count // self.attack_speed]
        cannon = self.rot_center(cannon, self.turnAngle)
        win.blit(cannon, ((self.x + self.width / 2) - (cannon.get_width() / 2), self.y - cannon.get_height() / 2))
    def change_range(self, r):
        self.range = r


    def attack(self, enemies):
        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            x = enemy.x
            y = enemy.y
            dis = math.sqrt((self.x-x)**2 + (self.y-y)**2)
            if dis < self.range:
                self.inRange = True
                enemy_closest.append(enemy)
        enemy_closest.sort(key=lambda x: x.x)
        if len(enemy_closest) > 0:
            self.closest_enemy = enemy_closest[len(enemy_closest)-1]
            if self.cannon_count == 4:
                if self.closest_enemy.hit(self.damage) == True:
                   enemies.remove(self.closest_enemy)
