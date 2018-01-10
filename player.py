from pygame import *

MOVE_SPEED = 4
WIDTH = 4
HEIGHT = 4
COLOR = "#0000FF"


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.startX = x
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект

    def update(self, left, right, up, down, platforms):
        if up:
            self.yvel = -MOVE_SPEED
        if down:
            self.yvel = MOVE_SPEED
        if left:
            self.xvel = -MOVE_SPEED
        if right:
            self.xvel = MOVE_SPEED

        if up or down:
            self.xvel = 0
        if left or right:
            self.yvel = 0

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def stop(self):
        self.yvel = 0
        self.xvel = 0

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                if yvel < 0:
                    self.rect.top = p.rect.bottom

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_grounded(self, grounds):
        for ground in grounds:
            if sprite.collide_rect(self, ground):
                return True
        return False
