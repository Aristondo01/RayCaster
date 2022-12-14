import numpy
import random
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm
from math import *

pygame.init()

screen = pygame.display.set_mode(
    (900, 600),
    pygame.OPENGL | pygame.DOUBLEBUF
)
# dT = pygame.time.Clock()


vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;

uniform mat4 amatrix;

out vec3 ourColor;
out vec2 fragCoord;
out vec2 XY;



void main()
{
    gl_Position = amatrix * vec4(position, 1.0f);
    fragCoord =  gl_Position.xy;
    XY = fragCoord;
    ourColor = vertexColor;

}
"""

fragment_shader = """
#version 460

layout (location = 0) out vec4 fragColor;

uniform vec3 color;
uniform float iTime;
float pi = 3.1415926435;



in vec3 ourColor;

void main()
{
    fragColor = vec4(color.x * (iTime/255),0,0, 1.0f);
    vec3 t = (iTime) / color;
    float i = iTime;
    vec3 cs = cos(i * pi * 2.0 + color * pi + t);
    fragColor = vec4(0.5 + 0.5 * cs, 1.0);    
}
"""


fragment_shader2 = """
#version 460

layout (location = 0) out vec4 fragColor;

uniform float iTime;
vec2 vp = vec2(320.0, 200.0);
uniform vec3 color;

in vec2 fragCoord;

vec3 iResolution = vec3(500,500,500);
float pi = 3.1415926435;

void main()
{
    float i = fragCoord.x;
    vec3 t = (iTime) / color;
    vec3 cs = cos(i * pi * 2.0 + vec3(0.0, 1.0, -0.5) * pi + t);
    fragColor = vec4(0.5 + 0.5 * cs, 1.0);    
}
"""

fragment_shader3 = """
#version 460

#define NUM_LAYER 8.

#define PI 3.14159265358979

layout (location = 0) out vec4 fragColor;

uniform vec3 color;
uniform float iTime;
in vec2 fragCoord;

in vec3 ourColor;

mat2 Rot(float angle){
    float s=sin(angle), c=cos(angle);
    return mat2(c, -s, s, c);
}

//random number between 0 and 1
float Hash21(vec2 p){
    p = fract(p*vec2(123.34, 456.21));
    p +=dot(p, p+45.32);
    return  fract(p.x*p.y);
}

float Star(vec2 uv, float flare){
    float d = length(uv);//center of screen is origin of uv -- length give us distance from every pixel to te center
    float m = .05/d;
    float rays = max(0., 1.-abs(uv.x*uv.y*1000.));
    m +=rays*flare;
    
    uv *=Rot(3.1415/4.);
    rays = max(0., 1.-abs(uv.x*uv.y*1000.));
    m +=rays*.3*flare;
    m *=smoothstep(1., .2, d);
    return m;
}

vec3 StarLayer(vec2 uv){
   
   vec3 col = vec3(0.);
   
    vec2 gv= fract(uv)-.5; //gv is grid view
    vec2 id= floor(uv);
    
    for(int y=-1; y<=1; y++){
        for(int x=-1; x<=1; x++){
            
            vec2 offset= vec2(x, y);
            float n = Hash21(id+offset);
            float size = fract(n*345.32);
                float star= Star(gv-offset-(vec2(n, fract(n*34.))-.5), smoothstep(.9, 1., size)*.6);
            vec3 color = sin(vec3(.2, .3, .9)*fract(n*2345.2)*123.2)*.5+.5;
            color = color*vec3(1., .25, 1.+size);
            
            star *=sin(iTime*3.+n*6.2831)*.5+1.;
            col +=star*size*color; 
            
         }
     }
    return col;
}

void main()
{
    vec2 iResolution = vec2(20, 20);
    vec2 iMouse = vec2(1, 1);
    vec2 uv = (fragCoord-.5*iResolution.xy)/iResolution.y;
    float t=  iTime*.02;
    vec2 M = (iMouse.xy-iResolution.xy*.5)/iResolution.y;
    uv *=Rot(t);
    uv +=M*4.;
    
    vec3 col = vec3(0.);
    
    for(float i =0.; i<1.; i += 1./NUM_LAYER){
        float depth = fract(i+t);
        float scale= mix(10.,.5, depth);
        float fade = depth*smoothstep(1., .9, depth);
        col += StarLayer(uv*scale+i*453.32-M)*fade;
    }
    fragColor = vec4(col,1.0);
}


"""
compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
compiled_fragment_shader2 = compileShader(fragment_shader2, GL_FRAGMENT_SHADER)
compiled_fragment_shader3 = compileShader(fragment_shader3, GL_FRAGMENT_SHADER)


shader1 = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader
)

shader2 = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader2
)

shader3 = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader3
)

shader = shader1
glUseProgram(shader)      
glEnable(GL_DEPTH_TEST)



vertex_data = numpy.array([
    #Caras frontales
    1, 0, 0,
    0, 1, 0,
    0, 0, 0,
    
    1, 0, 0,
    0, 1, 0,
    1, 1, 0,
    
    1, 0, 1,
    0, 1, 1,
    0, 0, 1,
    
    1, 0, 1,
    0, 1, 1,
    1, 1, 1,
#---------------------------------------    
    
    0, 1, 0,
    0, 0, 1, 
    0, 0, 0,
    
    0, 1, 0,
    0, 0, 1,
    0, 1, 1,
    
    1, 1, 0, 
    1, 0, 1, 
    1, 0, 0, 
    
    1, 1, 0, 
    1, 0, 1, 
    1, 1, 1, 
    
#---------------------------------------    
    
    0, 1, 1,  
    1, 1, 0,  
    0, 1, 0,  
    
    0, 1, 1, 
    1, 1, 0, 
    1, 1, 1,     
    
    
    0, 0, 1,  
    1, 0, 0,  
    0, 0, 0,  
    
    0, 0, 1, 
    1, 0, 0, 
    1, 0, 1, 

], dtype=numpy.float32)

vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(
    GL_ARRAY_BUFFER,  # tipo de datos
    vertex_data.nbytes,  # tama??o de da data en bytes    
    vertex_data, # puntero a la data
    GL_STATIC_DRAW
)
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

glVertexAttribPointer(
    0,
    3,
    GL_FLOAT,
    GL_FALSE,
    3*4,
    ctypes.c_void_p(0)
)
glEnableVertexAttribArray(0)


glVertexAttribPointer(
    1,
    3,
    GL_FLOAT,
    GL_FALSE,
    3*4,
    ctypes.c_void_p(3 * 4)
)
glEnableVertexAttribArray(1)


def calculateMatrix(angle,vector_rotatio,vector_translate =(0,-0.5,0)):
    i = glm.mat4(1)
    translate = glm.translate(i, glm.vec3(vector_translate))
    rotate = glm.rotate(i, glm.radians(angle), glm.vec3(vector_rotatio))
    scale = glm.scale(i, glm.vec3(1, 1, 1))

    model = translate * rotate * scale

    view = glm.lookAt(
        glm.vec3(0, 0, 5),
        glm.vec3(0, 0, 0),
        glm.vec3(0, 1, 0)
    )

    projection = glm.perspective(
        glm.radians(45),
        900/600,
        0.1,
        1000.0
    )

    amatrix = projection * view * model

    glUniformMatrix4fv(
        glGetUniformLocation(shader, 'amatrix'),
        1,
        GL_FALSE,
        glm.value_ptr(amatrix)
    )

glViewport(0, 0, 900, 600)



running = True

glClearColor(0.5, 1.0, 0.5, 1.0)

r = 0
opcion1 = True
opcion2 = False
opcion3 = False
suma = 1
color1 = 0.2
color2 = 0.5
color3 = 0.1
Giro = 0
while running:
    
    r += suma
    
    glUniform1f(
                glGetUniformLocation(shader,'iTime'),
                r/100
            )
    
    if opcion1:
        shader = shader1
        glUseProgram(shader)              
        if r >= 255:
            suma =-3
        if r <= 0:
            suma =3
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        color = glm.vec3(255,0,0)
        glUniform3fv(
                glGetUniformLocation(shader,'color'),
                1,
                glm.value_ptr(color)
            )
        
        
        calculateMatrix(Giro,(0, 1, 0))
        
        
    if opcion2:
        suma =1
        shader = shader3
        glUseProgram(shader)              
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
       

        color = glm.vec3(0, 0, 0)

        glUniform3fv(
            glGetUniformLocation(shader,'color'),
            1,
            glm.value_ptr(color)
        )
    
        calculateMatrix(r,(0.5, 1, 0.1))
        
    
    if opcion3:
        suma =1
        shader = shader2
        glUseProgram(shader)              
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        mov = (-sin(r/10),sin(r/10),cos(-r/10))

        if r % 15 ==0:
            color1 = random.random()
            color2 = random.random()
            color3 = random.random()

            color = glm.vec3(color1, color2, color3)
        
        glUniform3fv(
                glGetUniformLocation(shader,'color'),
                1,
                glm.value_ptr(color)
            )
        calculateMatrix(5*r,(0, 0.1, 0.1),mov)
    
    
    

    pygame.time.wait(50)


    glDrawArrays(GL_TRIANGLES, 0, len(vertex_data))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
            
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_1):
                opcion1 = True
                opcion2 = False
                opcion3 = False
            if (event.key == pygame.K_2):
                opcion1 = False
                opcion2 = True
                opcion3 = False
                suma =1
                
            if (event.key == pygame.K_3):
                opcion1 = False
                opcion2 = False
                opcion3 = True
                suma =1
                
            if (event.key == pygame.K_LEFT):
                Giro -=5
            if (event.key == pygame.K_RIGHT):
                Giro +=5
                
                