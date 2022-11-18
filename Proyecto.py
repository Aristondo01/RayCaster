import pygame
from math import cos, sin, pi,atan2
from OpenGL.GL import *


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


TRASPARENTE = (1,255,1)

SKY = (38, 36, 50)
GROUND = (88, 92, 121)

colors = [
    (0, 20, 10),
    (4, 40, 63),
    (0, 91, 82),
    (219, 242, 38),
    (21, 42, 138)
]
load_screen = pygame.image.load('./inicio2.png')
next_level = pygame.image.load('./next_level.png')
win = pygame.image.load('./WIN.png')






wall1 = pygame.image.load('./PARED1.jpg')
wall2 = pygame.image.load('./PARED2.jpeg')

walls = {
    "1" : wall1,
    "2" : wall2,
}

enemie1 = pygame.image.load('./sprite1.png')

enemies = [{
    "x": 120,
    "y": 120,
    "sprite": enemie1,
    "pos": 0
    },
           
    {
    "x": 100,
    "y": 300,
    "sprite": enemie1,
    "pos": 1
    }
]


enemies2 = [{
    "x": 200,
    "y": 120,
    "sprite": enemie1,
    "pos": 0
    },
           
    {
    "x": 250,
    "y": 300,
    "sprite": enemie1,
    "pos": 1
    },
    
    {
    "x": 100,
    "y": 100,
    "sprite": enemie1,
    "pos": 2
    }
]



class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        x, y, self.width, self.height = screen.get_rect()
        self.block_size = 50
        self.map = []
        self.last_move=None
        self.puntos=0
        self.player = {
            "x": int(self.block_size + (self.block_size / 2)),
            "y": int(self.block_size + (self.block_size / 2)),
            "fov": int(pi / 3),
            "a": int(0)
        }
        self.clearZ()

    def clearZ(self):
        self.zbuffer = [9999999 for z in range(0, 500)]
        
    def point(self, x, y, c = RED):
        # No usa aceleracion grafica. Usar pixel o point usado en juego de la vida
        self.screen.set_at((x, y), c)

    def block(self, x, y, wall):
        for i in range(x, x + self.block_size):
            for j in range(y, y + self.block_size):
                tx = int((i - x) * 256 / self.block_size)
                ty = int((j - y) * 256 / self.block_size)
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
            ty = int((y - start_y) * 256 / height)
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

                tx = int(maxhit * 256 / self.block_size)
                return d, self.map[j][i], tx

            #self.point(x, y)
            d += 1
    def draw_sprite(self,sprite):
        
        
        px,py = self.player["x"],self.player["y"]
        sx,sy = sprite["x"],sprite["y"]
        
        
        
        d = ((px - sx)**2 + (py -sy)**2)**0.5
        sprite_a = atan2(sy - py,sx-px)
        sprite_size = int(500/d  * 500/20)
        sprite_y = int (500/2 - sprite_size/6) 
        
        sprite_x =int((sprite_a - self.player["a"])* 500/self.player["fov"] + sprite_size/2)
        
        
        
        
        for x in range(sprite_x,sprite_x+sprite_size):
            for y in range(sprite_y,sprite_y+sprite_size):
                tx = int((x - sprite_x)  * 580/sprite_size)
                ty = int((y - sprite_y) * 580/sprite_size)
                c = sprite["sprite"].get_at((tx,ty))
                if c != TRASPARENTE:
                    if x>0 and x<500:
                        if self.zbuffer[x] >= d:
                            self.zbuffer[x] =d
                            self.point(x,y,c)
            
        
    def draw_map(self):
        for x in range(0, 500, int(self.block_size)):
            for y in range(0, 500, int(self.block_size)):
                i = int(x / self.block_size)
                j = int(y / self.block_size)

                if self.map[j][i] !=  ' ':
                    self.block(x, y, walls[self.map[j][i]])

    def draw_player(self):
        self.point(self.player["x"], self.player["y"])

    def start(self,imagen):
        for x in range(0,500):
            for y in range(0,500):
                c = imagen.get_at((x,y))
                self.point(x,y,c)
            
    def disparo(self,sprite):
        pygame.mixer.Sound.play(laser_sound)
        px,py = self.player["x"],self.player["y"]
        sx,sy = sprite["x"],sprite["y"]
        
        
        
        d = ((px - sx)**2 + (py -sy)**2)**0.5
        sprite_a = atan2(sy - py,sx-px)
        sprite_size = int(500/d  * 500/20)
        sprite_y = int (500/2 - sprite_size/6) 
        
        sprite_x =int((sprite_a - self.player["a"])* 500/self.player["fov"] + sprite_size/2)
        
        
        
        for x in range(250, 251):
            for y in range(250, 251):
                tx = int((x - sprite_x)  * 580/sprite_size)
                ty = int((y - sprite_y) * 580/sprite_size)
                try:
                    c = sprite["sprite"].get_at((tx,ty))
                except:
                    c = 0
                if c != 0 and c != TRASPARENTE and self.zbuffer[250] >= d:
                    #print("le di al tropper #"+str(sprite["pos"]))
                    c=0
                    ubicacion = sprite["pos"]
                    enemies.pop(ubicacion)
                    enemies.insert(ubicacion,None)
                    self.puntos+=1
                    break
                
                    
                    
        
    def error(self):
        if self.last_move == "l":
                
            if self.player["a"] == 0:
                self.player["y"] += 10
                    
            if self.player["a"] == pi/4:
                self.player["x"] -= 10
                self.player["y"] += 10
                
            if self.player["a"] == pi/2:
                self.player["x"] -= 10
                
            if self.player["a"] == pi*3/4:
                self.player["x"] -= 10
                self.player["y"] -= 10
                    
            if self.player["a"] == pi:
                self.player["y"] -= 10
                
            if self.player["a"] == pi*5/4:
                self.player["x"] += 10
                self.player["y"] -= 10
                
            if self.player["a"] == pi*6/4:
                self.player["x"] += 10
                
            if self.player["a"] == pi*7/4:
                self.player["y"] += 10
                self.player["x"] += 10
                    
        if self.last_move == "r":
            if self.player["a"] == 0:
                self.player["y"] -= 10
                
            if self.player["a"] == pi/4:
                self.player["x"] += 10
                self.player["y"] -= 10
                
            if self.player["a"] == pi/2:
                self.player["x"] += 10
                
            if self.player["a"] == pi*3/4:
                self.player["x"] += 10
                self.player["y"] += 10
                
            if self.player["a"] == pi:
                self.player["y"] += 10
                
            if self.player["a"] == pi*5/4:
                self.player["x"] -= 10
                self.player["y"] += 10
            
            if self.player["a"] == pi*6/4:
                self.player["x"] -= 10
                
            if self.player["a"] == pi*7/4:
                self.player["y"] -= 10
                self.player["x"] -= 10
        if self.last_move == "d":
            
            if self.player["a"] == 0:
                self.player["x"] += 10
                
            if self.player["a"] == pi/4:
                self.player["x"] += 10
                self.player["y"] += 10
                
            if self.player["a"] == pi/2:
                self.player["y"] += 10
                
            if self.player["a"] == pi*3/4:
                self.player["x"] -= 10
                self.player["y"] += 10
                
            if self.player["a"] == pi:
                self.player["x"] -= 10
                
            if self.player["a"] == pi*5/4:
                self.player["x"] -= 10
                self.player["y"] -= 10
            
            if self.player["a"] == pi*6/4:
                self.player["y"] -= 10
                
            if self.player["a"] == pi*7/4:
                self.player["y"] -= 10
                self.player["x"] += 10
                
                
        if self.last_move == "u":
            if self.player["a"] == 0:
                self.player["x"] -= 10
                
            if self.player["a"] == pi/4:
                self.player["x"] -= 10
                self.player["y"] -= 10
                
            if self.player["a"] == pi/2:
                self.player["y"] -= 10
                
            if self.player["a"] == pi*3/4:
                self.player["x"] += 10
                self.player["y"] -= 10
                
            if self.player["a"] == pi:
                self.player["x"] += 10
                
            if self.player["a"] == pi*5/4:
                self.player["x"] += 10
                self.player["y"] += 10
            
            if self.player["a"] == pi*6/4:
                self.player["y"] += 10
                
            if self.player["a"] == pi*7/4:
                self.player["y"] += 10
                self.player["x"] -= 10
        
    def render(self):
        #self.draw_map()
        #self.draw_player()
        self.clearZ()

        # draw in 3d

        for i in range(0, int(self.width)):
            a = self.player["a"] - self.player["fov"] / 2 + self.player["fov"] * i / (self.width)
            d, c, tx = self.cast_ray(a)
            
            x = i
            try:
                h = (self.height / (d * cos(a - self.player["a"]))) * self.height / 5
            except:
                self.error()
                h=0
                
            
            if self.zbuffer[i] >= d:
                self.zbuffer[i] = d
                self.draw_stake(x, h, c, tx)
        
        """for enemigo in enemies:
            self.point(enemigo["x"],enemigo["y"],(255,0,0))"""
            
        for enemigo in enemies:
            if enemigo:
                self.draw_sprite(enemigo)
            
        # mira
        for i in range(240, 260): 
            self.point(249, i)
            self.point(250, i)
            self.point(251, i)
            
            self.point(i,249)
            self.point(i,250)
            self.point(i,251)

def fps():
    text = font.render("fps = "+str(round(clock.get_fps(),2)), True, (255,255,255), (0,0,0))
    textRect = text.get_rect()
    textRect.center = (35, 10)
    display_surface.blit(text, textRect)
    pygame.display.update() 
    clock.tick(60)
    

pygame.init()
import os
os.getcwd() 
pygame.mixer.music.load("SW.mp3")
laser_sound = pygame.mixer.Sound('disparo_1.mp3')
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((500, 500))
font = pygame.font.Font('freesansbold.ttf', 14)

r = Raycaster(screen)
r.load_map('map.txt')
inicio = True
running1 = True
running2 = True

nivel=True
final=True

pygame.mixer.music.play(-1)
while inicio:

    r.start(load_screen)

    pygame.display.flip()
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            inicio = False
            running1 = False
            running2 = False
            final =False
            nivel = False
            

        if (event.type == pygame.KEYDOWN):

            if event.key == pygame.K_1:
                inicio=False
            if event.key == pygame.K_2:
                inicio=False
                running1 = False
                r.puntos=2
            


while running1:
    fps()
    if r.puntos ==2:
        break
    
    screen.fill(BLACK)
    screen.fill(SKY, (0, 0, r.width, r.height / 2))
    screen.fill(GROUND, (0, r.height / 2, r.width, r.height))

    r.render()

    pygame.display.flip()
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            inicio = False
            running1 = False
            running2 = False
            nivel=False
            final =False

        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_SPACE:
                for enemigo in enemies:
                    if enemigo:
                        r.disparo(enemigo)

            if event.key == pygame.K_a:
                r.player["a"] = (r.player["a"] - pi / 4) % (pi * 2)
            if event.key == pygame.K_d:
                r.player["a"] = (r.player["a"] + pi / 4) % (pi * 2)
                

            if event.key == pygame.K_RIGHT:
                r.last_move="r"
                if r.player["a"] == 0:
                    r.player["y"] += 10
                    
                if r.player["a"] == pi/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
                    
                if r.player["a"] == pi/2:
                    r.player["x"] -= 10
                    
                if r.player["a"] == pi*3/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi:
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi*5/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
                
                if r.player["a"] == pi*6/4:
                    r.player["x"] += 10
                    
                if r.player["a"] == pi*7/4:
                    r.player["y"] += 10
                    r.player["x"] += 10
                    
            if event.key == pygame.K_LEFT:
                r.last_move="l"
                
                if r.player["a"] == 0:
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi/2:
                    r.player["x"] += 10
                    
                if r.player["a"] == pi*3/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
                    
                if r.player["a"] == pi:
                    r.player["y"] += 10
                    
                if r.player["a"] == pi*5/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
                
                if r.player["a"] == pi*6/4:
                    r.player["x"] -= 10
                    
                if r.player["a"] == pi*7/4:
                    r.player["y"] -= 10
                    r.player["x"] -= 10
            if event.key == pygame.K_UP:
                r.last_move="u"
                
                if r.player["a"] == 0:
                    r.player["x"] += 10
                    
                if r.player["a"] == pi/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
                    
                if r.player["a"] == pi/2:
                    r.player["y"] += 10
                    
                if r.player["a"] == pi*3/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
                    
                if r.player["a"] == pi:
                    r.player["x"] -= 10
                    
                if r.player["a"] == pi*5/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
                
                if r.player["a"] == pi*6/4:
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi*7/4:
                    r.player["y"] -= 10
                    r.player["x"] += 10
                    
                    
            if event.key == pygame.K_DOWN:
                r.last_move="d"
                
                if r.player["a"] == 0:
                    r.player["x"] -= 10
                    
                if r.player["a"] == pi/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi/2:
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi*3/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi:
                    r.player["x"] += 10
                    
                if r.player["a"] == pi*5/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
                
                if r.player["a"] == pi*6/4:
                    r.player["y"] += 10
                    
                if r.player["a"] == pi*7/4:
                    r.player["y"] += 10
                    r .player["x"] -= 10
while nivel:

    r.start(next_level)

    pygame.display.flip()
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            inicio = False
            running1 = False
            running2 = False
            nivel=False
            final =False
            
            

        if (event.type == pygame.KEYDOWN):

            if event.key == pygame.K_SPACE:
                nivel=False

                   
#Nivel 2
r.player["x"] = int(r.block_size + (r.block_size / 2))
r.player["y"] = int(r.block_size + (r.block_size / 2))

r.map=[]
r.load_map('map2.txt')
enemies = enemies2
while running2:
    fps()
    if r.puntos ==5:
        break
    
    screen.fill(BLACK)
    screen.fill(SKY, (0, 0, r.width, r.height / 2))
    screen.fill(GROUND, (0, r.height / 2, r.width, r.height))

    r.render()

    pygame.display.flip()
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            inicio = False
            running1 = False
            running2 = False
            nivel=False
            final =False

        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_SPACE:
                for enemigo in enemies:
                    if enemigo:
                        r.disparo(enemigo)

            if event.key == pygame.K_a:
                r.player["a"] = (r.player["a"] - pi / 4) % (pi * 2)
            if event.key == pygame.K_d:
                r.player["a"] = (r.player["a"] + pi / 4) % (pi * 2)
                

            if event.key == pygame.K_RIGHT:
                r.last_move="r"
                if r.player["a"] == 0:
                    r.player["y"] += 10
                    
                if r.player["a"] == pi/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
                    
                if r.player["a"] == pi/2:
                    r.player["x"] -= 10
                    
                if r.player["a"] == pi*3/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi:
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi*5/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
                
                if r.player["a"] == pi*6/4:
                    r.player["x"] += 10
                    
                if r.player["a"] == pi*7/4:
                    r.player["y"] += 10
                    r.player["x"] += 10
                    
            if event.key == pygame.K_LEFT:
                r.last_move="l"
                
                if r.player["a"] == 0:
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi/2:
                    r.player["x"] += 10
                    
                if r.player["a"] == pi*3/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
                    
                if r.player["a"] == pi:
                    r.player["y"] += 10
                    
                if r.player["a"] == pi*5/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
                
                if r.player["a"] == pi*6/4:
                    r.player["x"] -= 10
                    
                if r.player["a"] == pi*7/4:
                    r.player["y"] -= 10
                    r.player["x"] -= 10
            if event.key == pygame.K_UP:
                r.last_move="u"
                
                if r.player["a"] == 0:
                    r.player["x"] += 10
                    
                if r.player["a"] == pi/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
                    
                if r.player["a"] == pi/2:
                    r.player["y"] += 10
                    
                if r.player["a"] == pi*3/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
                    
                if r.player["a"] == pi:
                    r.player["x"] -= 10
                    
                if r.player["a"] == pi*5/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
                
                if r.player["a"] == pi*6/4:
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi*7/4:
                    r.player["y"] -= 10
                    r.player["x"] += 10
                    
                    
            if event.key == pygame.K_DOWN:
                r.last_move="d"
                
                if r.player["a"] == 0:
                    r.player["x"] -= 10
                    
                if r.player["a"] == pi/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi/2:
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi*3/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
                    
                if r.player["a"] == pi:
                    r.player["x"] += 10
                    
                if r.player["a"] == pi*5/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
                
                if r.player["a"] == pi*6/4:
                    r.player["y"] += 10
                    
                if r.player["a"] == pi*7/4:
                    r.player["y"] += 10
                    r .player["x"] -= 10 


while final:

    r.start(win)

    pygame.display.flip()
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            final = False