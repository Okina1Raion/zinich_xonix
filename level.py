from block import *
from enemy import *
from player import *


class Level:
    def __init__(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            read_file = file.read()
        self.edges, self.platforms, self.player = self.parse_level(read_file.split('|')[0])
        self.enemies = self.parse_enemies(read_file.split('|')[1])

    def parse_enemies(self, raw_enemies):
        result_enemies = []
        enemies = raw_enemies.splitlines()
        for enemy in enemies:
            e = enemy.split(';')
            result_enemies.append(Enemy(int(e[0]), int(e[1]), int(e[2]), int(e[3])))
        return result_enemies

    def parse_level(self, raw_level):
        x = y = 0
        edges = []
        platforms = []
        player = None
        for row in raw_level.splitlines():
            for col in row:
                if col == "-":
                    edge = Platform(x, y)
                    edges.append(edge)
                if col == "0":
                    platform = Platform(x, y)
                    platforms.append(platform)
                if col == "p":
                    player = Player(x, y)
                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0
        return edges, platforms, player
