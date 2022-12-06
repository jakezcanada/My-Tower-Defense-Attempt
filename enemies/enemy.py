import pygame
import math


class Enemy:
    imgs = []

    def __init__(self):
        game_height = 448
        game_width = 704
        self.width = 32
        self.height = 32
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = [(-10, game_height/2), (game_width/11*3.5, game_height/2), (game_width/11*3.5, game_height/7*2.5), (game_width/11*7.5, game_height/7*2.5), (game_width/11*7.5, game_height/2), (game_width+50, game_height/2)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = None
        self.dis = 0
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.flipped = False
        self.max_health = 0

    def draw(self, win):

        self.img = self.imgs[self.animation_count//5]
        self.animation_count += 1
        if self.animation_count >= len(self.imgs)*5:
            self.animation_count = 0
        win.blit(self.img, (self.x-self.img.get_width()/2, self.y-self.img.get_height()/2))
        self.draw_health_bar(win)
        self.move()

    def draw_health_bar(self,win):
        length = 50
        move_by = length / self.max_health
        health_bar = move_by * self.health

        pygame.draw.rect(win, (255,0,0), (self.x-25, self.y - 25, length, 5), 0)
        pygame.draw.rect(win, (0,255,0), (self.x-25, self.y - 25, health_bar, 5), 0)

    def collide(self,X ,Y):
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def move(self):
        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (-10, 355)
        else:
            x2, y2 = self.path[self.path_pos+1]

        dirn = ((x2-x1)/2, (y2-y1)/2)
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = ((x2-x1)/length, (y2-y1)/length)

        if dirn[0] < 0 and not self.flipped:  #flips enemy sprite
            self.flipped = True
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
        self.dis += math.sqrt((move_x-x1)**2 + (move_y-y1)**2)

        self.x = move_x
        self.y = move_y

        if dirn[0] >= 0:
            if dirn[1] > 0:
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else:
            if dirn[1] >= 0:
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False