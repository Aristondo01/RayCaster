import pygame
from OpenGL.GL import *
pygame.init()


screen = pygame.display.set_mode(
    (800,600),
    pygame.OPENGL | pygame.DOUBLEBUF)

x = 5
y = 10
speed = 1
speed2 = 1


running = True

def point(x,y,color):
    glEnable(GL_SCISSOR_TEST)
    glScissor(x,y,50,50)
    glClearColor(color[0], color[1], color[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)
    

while running:
    
    #clean
    glClearColor(0.2, 0.8, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    #paint
    
    if x == 800:
        speed = -1
    elif x == 0:
        speed = 1
        
    x += speed
    
    
    if y == 600:
        speed2 = -1
    elif y == 0:
        speed2 = 1
        
        
    y += speed2
    point(x,y,[1,0,0])
    
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False