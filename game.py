import pygame
import os
from enemies.circle import Circle
from towers.cannon import Cannon
from textRender import render
import time
import random
pygame.font.init()
font = pygame.font.SysFont(None, 64)
lives_imgs = []
for x in range(1,12):
    lives_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/misc/heart", "Heart" + str(x) + ".png")),
        (128, 128)))
    lives_imgs[x-1].set_colorkey((255,255,255))
class Game:
    def __init__(self):
        self.width = 704
        self.height = 448
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = []
        self.towers = [Cannon(704/11*4.5,448/7*3.5)]
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("game_assets","bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.timer = 0
        self.heartTimer = time.time()
        self.heartFrame = 1

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            if self.timer >= 1.0:
                self.timer = 0
                self.enemys.append(random.choice([Circle()]))
            self.timer += 0.01
            clock.tick(600)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
            to_del = []
            for en in self.enemys:
                if en.x < -15 or en.x > self.width+15:
                    to_del.append(en)
                    if self.lives!=0:
                        self.lives -= 1

            for d in to_del:
                self.enemys.remove(d)

            for tw in self.towers:
                tw.attack(self.enemys)


            self.draw()
        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0,0))
        for tw in self.towers:
            tw.draw(self.win)
        for en in self.enemys:
            en.draw(self.win)
        self.win.blit(render(str(self.lives), font, gfcolor=(37,125,192), opx=1.5), (64,15))
        if self.heartFrame != 0:
            if self.heartFrame == 10*3:
                self.heartFrame = 0
            else:
                self.heartFrame += 1
        if self.heartTimer >= 3.3:
            self.heartFrame += 1
            self.heartTimer = 0
        self.heartTimer += 0.01

        self.win.blit(lives_imgs[self.heartFrame//3], (-32,-32))
        pygame.display.update()

g = Game()
g.run()