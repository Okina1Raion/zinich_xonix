from block import *

PLATFORM_WIDTH = 4
PLATFORM_HEIGHT = 4
PLATFORM_COLOR = "#888888"


class LinePart(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def to_platform(self):
        return Platform(self.rect.x, self.rect.y)
