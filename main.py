import sys
import pygame
from pygame import *

from level import *
from line import *

PLATFORM_CELL = 1

FILLED_CELL = 5

LINED_CELL = 3
EMPTY_CELL = 0

GAME_NAME = "Xonix"
sys.setrecursionlimit(3000)

TIMEOUT = 30
LEVEL_FILE_NAME = "level.txt"
WIN_WIDTH = 640
WIN_HEIGHT = 664
# WIN_WIDTH1 = 176
# WIN_HEIGHT1 = 224
# DISPLAY = (WIN_WIDTH1, WIN_HEIGHT1)
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#000000"
matrix_mask = []
for i in range(int(WIN_WIDTH / 4)):
    matrix_mask.append(list(map(int, ("0" * int(WIN_HEIGHT / 4)))))


def try_fill(x: int, y: int):
    is_free = False
    for i in range(-1, 2):
        for n in range(-1, 2):
            if matrix_mask[x + i][y + n] == EMPTY_CELL:
                is_free = True

    if not is_free:
        return
    matrix_mask[x][y] = FILLED_CELL
    queue = []
    x1 = x + 1
    x2 = x - 1
    y1 = y + 1
    y2 = y - 1
    while matrix_mask[x1][y] == EMPTY_CELL:
        matrix_mask[x1][y] = FILLED_CELL
        queue.append((x1, y))
        x1 += 1
    while matrix_mask[x2][y] == EMPTY_CELL:
        matrix_mask[x2][y] = FILLED_CELL
        queue.append((x2, y))
        x2 -= 1
    while matrix_mask[x][y1] == EMPTY_CELL:
        matrix_mask[x][y1] = FILLED_CELL
        queue.append((x, y1))
        y1 += 1
    while matrix_mask[x][y2] == EMPTY_CELL:
        matrix_mask[x][y2] = FILLED_CELL
        queue.append((x, y2))
        y2 -= 1
    for l in queue:
        try_fill(l[0], l[1])


def fill():
    new_platforms = []
    for line in range(len(matrix_mask)):
        for cell in range(len(matrix_mask[line])):
            if matrix_mask[line][cell] == EMPTY_CELL or matrix_mask[line][cell] == LINED_CELL:
                new_platforms.append(Platform(line * 4, cell * 4))  # maybe in another way
                matrix_mask[line][cell] = PLATFORM_CELL
            elif matrix_mask[line][cell] == FILLED_CELL:
                matrix_mask[line][cell] = EMPTY_CELL
    return new_platforms


def main():
    # Casual init
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption(GAME_NAME)
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))
    timer = pygame.time.Clock()
    # Game parts init
    left = right = up = down = False
    entities = pygame.sprite.Group()
    level = Level(LEVEL_FILE_NAME)
    line = []
    line_group = pygame.sprite.Group()
    platforms = level.platforms
    edges = level.edges
    hero = level.player
    enemies = level.enemies

    for g in edges:
        matrix_mask[int(g.rect.x / 4)][int(g.rect.y / 4)] = EMPTY_CELL

    for p in platforms:
        matrix_mask[int(p.rect.x / 4)][int(p.rect.y / 4)] = PLATFORM_CELL

    for e in enemies + edges + platforms:
        entities.add(e)
    # Main cycle
    while 1:
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()

            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYUP and e.key == K_UP:
                up = False

            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYUP and e.key == K_DOWN:
                down = False

        screen.blit(bg, (0, 0))
        hero.update(left, right, up, down, edges)
        if not hero.is_grounded(platforms + edges):
            line_part = LinePart(hero.rect.x, hero.rect.y)
            line.append(line_part)
            line_group.add(line_part)
            matrix_mask[int(hero.rect.x / 4)][int(hero.rect.y / 4)] = LINED_CELL
        elif len(line) != 0:
            # rewrite for filling and "platforming"
            for e in enemies:
                try_fill(int(e.rect.x / 4), int(e.rect.y / 4))
            for p in fill():
                platforms.append(p)
                entities.add(p)
            line = []
            line_group = pygame.sprite.Group()
            left = right = up = down = False
            hero.stop()
        for e in enemies:
            e.update(platforms + edges, hero, line)
        # draws
        line_group.draw(screen)
        entities.draw(screen)
        hero.draw(screen)

        pygame.display.update()
        timer.tick(TIMEOUT)


if __name__ == "__main__":
    main()
