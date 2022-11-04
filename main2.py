import pygame
from math import cos, sin, pi
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SKY = (50, 100, 200)
GROUND = (200, 200, 100)

colors = [
    (0, 20, 10),
    (4, 40, 63),
    (0, 91, 82),
    (219, 242, 38),
    (21, 42, 138)
]

wall1 = pygame.image.load('./wall1.png')
wall2 = pygame.image.load('./wall2.png')
wall3 = pygame.image.load('./wall3.png')

walls = {
    "1" : wall1,
    "2" : wall2,
    "3" : wall3,
}

class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        x, y, self.width, self.height = screen.get_rect()
        self.block_size = 50
        self.map = []
        self.player = {
            "x": int(self.block_size + (self.block_size / 2)),
            "y": int(self.block_size + (self.block_size / 2)),
            "fov": int(pi / 3),
            "a": int(pi / 3)
        }

    def point(self, x, y, c = WHITE):
        # No usa aceleracion grafica. Usar pixel o point usado en juego de la vida
        self.screen.set_at((x, y), c)

    def block(self, x, y, wall):
        for i in range(x, x + self.block_size):
            for j in range(y, y + self.block_size):
                tx = int((i - x) * 128 / self.block_size)
                ty = int((j - y) * 128 / self.block_size)
                c = wall.get_at((tx, ty))
                self.point(i, j, c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def draw_stake(self, x, h, c,tx):
        start_y = int(self.height / 2 - h / 2)
        end_y = int(self.height / 2 + h / 2)
        height = end_y - start_y
        for y in range(start_y, end_y):
            ty = int((y - start_y) * 128 / height)
            color = walls[c].get_at((tx, ty))
            self.point(x, y, color)

    def cast_ray(self, a):
        d = 0
        origin_x = self.player["x"]
        origin_y = self.player["y"]


        while True:
            x = int(origin_x + d * cos(a))
            y = int(origin_y + d * sin(a))

            i = int(x / self.block_size)
            j = int(y / self.block_size)

            if self.map[j][i] != ' ':
                hitx = x - i * self.block_size
                hity = y - j * self.block_size

                if 1 < hitx and hitx < self.block_size - 1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / self.block_size)
                return d, self.map[j][i], tx

            self.point(x, y)
            d += 1

    def draw_map(self):
        for x in range(0, 500, self.block_size):
            for y in range(0, 500, self.block_size):
                i = int(x / self.block_size)
                j = int(y / self.block_size)

                if self.map[j][i] !=  ' ':
                    self.block(x, y, walls[self.map[j][i]])

    def draw_player(self):
        self.point(self.player["x"], self.player["y"])

    def render(self):
        self.draw_map()
        self.draw_player()

        density = 100

        # minimap

        for i in range(0, density):
            a = self.player["a"] - self.player["fov"] / 2 + self.player["fov"] * i / density
            d, c, t = self.cast_ray(a)


        # separador

        for i in range(0, 500): 
            self.point(499, i)
            self.point(500, i)
            self.point(501, i)

        # draw in 3d

        for i in range(0, int(self.width/2)):
            a = self.player["a"] - self.player["fov"] / 2 + self.player["fov"] * i / (self.width / 2)
            d, c, tx = self.cast_ray(a)
            
            x = int(self.width / 2) + i
            h = (self.height / (d * cos(a - self.player["a"]))) * self.height / 5

            self.draw_stake(x, h, c, tx)


pygame.init()
screen = pygame.display.set_mode((1000, 500))
r = Raycaster(screen)
r.load_map('map.txt')

running = True
while running:
    screen.fill(BLACK)
    screen.fill(SKY, (r.width / 2, 0, r.width, r.height / 2))
    screen.fill(GROUND, (r.width / 2, r.height / 2, r.width, r.height))

    r.render()

    pygame.display.flip()
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

        if (event.type == pygame.KEYDOWN):

            if event.key == pygame.K_a:
                r.player["a"] -= pi / 10
            if event.key == pygame.K_d:
                r.player["a"] += pi / 10

            if event.key == pygame.K_RIGHT:
                r.player["x"] -= 10
            if event.key == pygame.K_LEFT:
                r.player["x"] += 10 
            if event.key == pygame.K_UP:
                r.player["y"] += 10
            if event.key == pygame.K_DOWN:
                r.player["y"] -= 10