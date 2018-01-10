from pygame import *
import sys

WIDTH = 4
HEIGHT = 4
COLOR = "#FF0000"


class Enemy(sprite.Sprite):
    def __init__(self, x, y, x_speed, y_speed):
        sprite.Sprite.__init__(self)
        self.xvel = x_speed
        self.yvel = y_speed
        self.startX = x
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект

    def update(self, platforms, player, line):
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.kill_player(player, line)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = -self.xvel
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = -self.xvel
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.yvel = -self.yvel
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = -self.yvel

    def kill_player(self, player, line):
        if sprite.collide_rect(self, player):
            sys.exit()
        for line_part in line:
            if sprite.collide_rect(self, line_part):
                sys.exit()
