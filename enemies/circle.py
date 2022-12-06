import pygame
import os
from .enemy import Enemy
imgs = []
for x in range(9):
    imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/circle", "Circle" + str(x) + ".png")),
        (64, 64)))
class Circle(Enemy):
    def __init__(self):
        super().__init__()
        self.max_health = 5
        self.health = self.max_health
        self.imgs = imgs[:]