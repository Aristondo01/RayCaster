import pygame
from OpenGL.GL import *
pygame.init()
pixeltam =7
tam =100*pixeltam
screen = pygame.display.set_mode(
    (tam,tam),
    pygame.OPENGL | pygame.DOUBLEBUF)


Framebuffer= []
tam = int(tam/pixeltam)
    
for i in range(tam):
    Framebuffer.append([])
    for j in range(tam):
        Framebuffer[i].append(0)


def estable(x,y):
    Framebuffer[y][x] = 1
    Framebuffer[y][x+1] = 1
    Framebuffer[y+1][x] = 1
    Framebuffer[y+1][x+1] = 1
    
def boat(x,y):
    Framebuffer[y-1][x] = 1
    Framebuffer[y+1][x] = 1
    Framebuffer[y][x+1] = 1
    Framebuffer[y][x-1] = 1
    Framebuffer[y-1][x-1] = 1

def glider(x,y):
    Framebuffer[y][x] = 1
    Framebuffer[y][x+1] = 1
    Framebuffer[y][x+2] = 1
    Framebuffer[y+1][x+2] = 1
    Framebuffer[y+2][x+1] = 1  
    
def oscillators(x,y):
    Framebuffer[y][x] = 1
    Framebuffer[y+1][x] = 1
    Framebuffer[y-1][x] = 1
    
def Penta(x,y):
    Framebuffer[y-4][x] = 1
    Framebuffer[y-3][x] = 1
    Framebuffer[y-2][x+1] = 1
    Framebuffer[y-2][x-1] = 1
    Framebuffer[y-1][x] = 1
    Framebuffer[y][x] = 1
    Framebuffer[y+1][x] = 1
    Framebuffer[y+2][x] = 1
    Framebuffer[y+3][x+1] = 1
    Framebuffer[y+3][x-1] = 1
    Framebuffer[y+4][x] = 1
    Framebuffer[y+5][x] = 1

def die_hard(x,y):
    Framebuffer[y][x] = 1
    Framebuffer[y][x-1] = 1
    Framebuffer[y-1][x] = 1
    
    Framebuffer[y-1][x+4] = 1
    Framebuffer[y-1][x+5] = 1
    Framebuffer[y-1][x+6] = 1
    
    Framebuffer[y+1][x+5] = 1
    


def generator(x,y):
    Framebuffer[y][x] = 1
    
    Framebuffer[y][x+2] = 1
    Framebuffer[y][x+3] = 1
    Framebuffer[y+1][x+2] = 1
    Framebuffer[y-1][x+2] = 1
    
    Framebuffer[y-2][x+1] = 1
    Framebuffer[y+2][x+1] = 1
    
    
    Framebuffer[y][x-4] = 1
    Framebuffer[y-1][x-4] = 1
    Framebuffer[y+1][x-4] = 1
    
    Framebuffer[y+2][x-3] = 1
    Framebuffer[y-2][x-3] = 1
    
    Framebuffer[y+3][x-2] = 1
    Framebuffer[y-3][x-2] = 1
    Framebuffer[y+3][x-1] = 1
    Framebuffer[y-3][x-1] = 1
    
    
    #Cubo
    estable(x-14,y)
    estable(x+20,y+2)
    
    #Cola
    Framebuffer[y+1][x+6] = 1
    Framebuffer[y+2][x+6] = 1
    Framebuffer[y+3][x+6] = 1
    Framebuffer[y+2][x+7] = 1
    Framebuffer[y+1][x+7] = 1
    Framebuffer[y+3][x+7] = 1
    
    Framebuffer[y][x+8] = 1
    Framebuffer[y+4][x+8] = 1
    
    Framebuffer[y][x+10] = 1
    Framebuffer[y+4][x+10] = 1
    
    Framebuffer[y-1][x+10] = 1
    Framebuffer[y+5][x+10] = 1
    
    
    
    

    
    
    
def pulsar(x,y):
    #Izquierda arriba
    Framebuffer[y+2][x-1] = 1
    Framebuffer[y+3][x-1] = 1
    Framebuffer[y+4][x-1] = 1
    
    Framebuffer[y+2][x-6] = 1
    Framebuffer[y+3][x-6] = 1
    Framebuffer[y+4][x-6] = 1
    
    Framebuffer[y+1][x-2] = 1
    Framebuffer[y+1][x-3] = 1
    Framebuffer[y+1][x-4] = 1
    
    Framebuffer[y+6][x-2] = 1
    Framebuffer[y+6][x-3] = 1
    Framebuffer[y+6][x-4] = 1
    
    #Izquierda abajo
    Framebuffer[y-2][x-1] = 1
    Framebuffer[y-3][x-1] = 1
    Framebuffer[y-4][x-1] = 1
    
    
    Framebuffer[y-2][x-6] = 1
    Framebuffer[y-3][x-6] = 1
    Framebuffer[y-4][x-6] = 1
    
    Framebuffer[y-1][x-2] = 1
    Framebuffer[y-1][x-3] = 1
    Framebuffer[y-1][x-4] = 1
    
    Framebuffer[y-6][x-2] = 1
    Framebuffer[y-6][x-3] = 1
    Framebuffer[y-6][x-4] = 1
    
    #Derecha arriba
    Framebuffer[y+2][x+1] = 1
    Framebuffer[y+3][x+1] = 1
    Framebuffer[y+4][x+1] = 1
    
    Framebuffer[y+2][x+6] = 1
    Framebuffer[y+3][x+6] = 1
    Framebuffer[y+4][x+6] = 1
    
    Framebuffer[y+1][x+2] = 1
    Framebuffer[y+1][x+3] = 1
    Framebuffer[y+1][x+4] = 1
    
    Framebuffer[y+6][x+2] = 1
    Framebuffer[y+6][x+3] = 1
    Framebuffer[y+6][x+4] = 1
    
    #Derecha abajo
    Framebuffer[y-2][x+1] = 1
    Framebuffer[y-3][x+1] = 1
    Framebuffer[y-4][x+1] = 1
    
    
    Framebuffer[y-2][x+6] = 1
    Framebuffer[y-3][x+6] = 1
    Framebuffer[y-4][x+6] = 1
    
    Framebuffer[y-1][x+2] = 1
    Framebuffer[y-1][x+3] = 1
    Framebuffer[y-1][x+4] = 1
    
    Framebuffer[y-6][x+2] = 1
    Framebuffer[y-6][x+3] = 1
    Framebuffer[y-6][x+4] = 1
    
    
    
    
   
running = True
    
    
def point2(points):
    glEnable(GL_SCISSOR_TEST)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    for y in range(tam):
        for x in range(tam):
            if points[y][x] ==1:
                glScissor(x*pixeltam,y*pixeltam,pixeltam,pixeltam)
                glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)



def vida ():
    Framebuffer2 =[]
    for i in range(tam):
        Framebuffer2.append([])
        for j in range(tam):
            celulas =0
            #Derecha
            if Framebuffer[i][(j+1)%tam] == 1:
                celulas+=1
            #Izquierda
            if Framebuffer[i][j-1] == 1:
                celulas+=1
            #Abajo
            if Framebuffer[i-1][j] == 1:
                celulas+=1
            #Arriba
            if Framebuffer[(i+1)%tam][j] == 1:
                celulas+=1
                
            #Derecha arriba
            if Framebuffer[(i+1)%tam][(j+1)%tam] == 1:
                celulas+=1
            #Izquierda arriba
            if Framebuffer[(i+1)%tam][j-1] == 1:
                celulas+=1
            #Abajo izquierda
            if Framebuffer[i-1][j-1] == 1:
                celulas+=1
            #abajo derecha
            if Framebuffer[i-1][(j+1)%tam] == 1:
                celulas+=1
                
            Framebuffer2[i].append(0)
            
            if celulas < 2 and Framebuffer[i][j]==1:
                Framebuffer2[i][j]=0
            
            if celulas > 3 and Framebuffer[i][j]==1:
                Framebuffer2[i][j]=0
                
            if celulas == 3 and Framebuffer[i][j]==0:
                Framebuffer2[i][j]=1
                
            if celulas <= 3 and celulas >= 2  and Framebuffer[i][j]==1:
                Framebuffer2[i][j]=1
            
            
                
    
    
    return Framebuffer2
                
            
            
    

oscillators(80,75)
pulsar(50,50)
glider(20,20)
glider(20,25)
glider(20,30)
Penta(12,17)
#generator(50,50)
#generator(-30,-30)
#generator(-80,-80)








#print(Framebuffer)
while running:
    
    #clean
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    #paint
    
    point2(Framebuffer)
    
    
    
    Framebuffer =vida()
    
    pygame.display.flip()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False