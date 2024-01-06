import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random
from glfw.GLFW import *
global camera_position
global g
druga = -1
color = -1
swiatlo = 0
swiatlo2 = 0
oddalenie=1
x=10
y=0
z=0
ex=0
ey=0
g=0
theta = 0.0

material_ambient = [1.0, 1.0, 1.0, 1.0]
material_diffuse = [10.0, 10.0, 10.0, 1.0]
material_specular = [10.0, 10.0, 10.0, 1.0]
material_shininess = 100.0

light_ambient = [4, 4, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

light1_ambient = [4, 0.0, 0.0, 1.0]
light1_diffuse = [1.0, 1.8, 1.2, 1.0]
light1_specular = [0.6, 0.7, 0.4, 1.0]
light1_position = [0.0, 10.0, 0.0, 1.0]
att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

# Tekstura
texture_surface = pygame.image.load("2.png")
texture_data = pygame.image.tostring(texture_surface, 'RGB', 1)
width, height = texture_surface.get_width(), texture_surface.get_height()

texture_surface2 = pygame.image.load("sky.png")
texture_data2 = pygame.image.tostring(texture_surface2, 'RGB', 1)
width2, height2 = texture_surface2.get_width(), texture_surface2.get_height()
# Kwadrat
vertices2 = (
    (-100, -3, -100),
    (100, -3, -100),
    (100, -3, 100),
    (-100, -3, 100)
)
vertices3 = (
    (-100, 80, -100),
    (100, 80, -100),
    (100, 80, 100),
    (-100, 80, 100)
)
edges2 = (
    (0, 1, 2, 3),
)


def draw_sky():
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3fv(vertices3[0])
    glTexCoord2f(1, 0)
    glVertex3fv(vertices3[1])
    glTexCoord2f(1, 1)
    glVertex3fv(vertices3[2])
    glTexCoord2f(0, 1)
    glVertex3fv(vertices3[3])
    glEnd()



def interpolate_color(color1, color2, t):
    return [color1[i] * (1 - t) + color2[i] * t for i in range(len(color1))]

def triangle(A, B, C, color1, color2, color3):
    glBegin(GL_TRIANGLES)
    glColor3fv(color1)
    glVertex3fv(A)
    glColor3fv(color2)
    glVertex3fv(B)
    glColor3fv(color3)
    glVertex3fv(C)
    glEnd()

def tetra(V1, V2, V3, V4, color1, color2, color3, color4):
    triangle(V1, V2, V3, color1, color2, color3)
    triangle(V1, V3, V4, color1, color3, color4)
    triangle(V2, V3, V4, color2, color3, color4)
    triangle(V1, V2, V4, color1, color2, color4)

def divide(V1, V2, V3, V4, color1, color2, color3, color4, n):
    global color
    if n > 0:
        V12 = [(V1[i] + V2[i]) / 2 for i in range(3)]
        V23 = [(V2[i] + V3[i]) / 2 for i in range(3)]
        V31 = [(V3[i] + V1[i]) / 2 for i in range(3)]
        V14 = [(V1[i] + V4[i]) / 2 for i in range(3)]
        V24 = [(V2[i] + V4[i]) / 2 for i in range(3)]
        V34 = [(V3[i] + V4[i]) / 2 for i in range(3)]

        C12 = interpolate_color(color1, color2, 0.5)
        C23 = interpolate_color(color2, color3, 0.5)
        C31 = interpolate_color(color3, color1, 0.5)
        C14 = interpolate_color(color1, color4, 0.5)
        C24 = interpolate_color(color2, color4, 0.5)
        C34 = interpolate_color(color3, color4, 0.5)

        divide(V1, V12, V31, V14, color1, C12, C31, C14, n - 1)
        divide(V12, V2, V23, V24, C12, color2, C23, C24, n - 1)
        divide(V31, V23, V3, V34, C31, C23, color3, C34, n - 1)
        divide(V14, V24, V34, V4, C14, C24, C34, color4, n - 1)
    else:
        if(color==-1):
            tetra(V1, V2, V3, V4, [1,1,1], [1,1,1], [1,1,1], [1,1,1])
        else:
            tetra(V1, V2, V3, V4, color1, color2, color3, color4)
def draw():
    global theta
    global N
    global oddalenie
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(y, z, x, y, z, x-1, 0, 1.0, 0.0)
    glRotatef(ex, 1, 0, 0)
    glRotatef(ey, 0, 1, 0)


    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
   

    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, material_shininess)

    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)
    
    glRotatef(90,1,0,0)
    glTranslatef(0,0,3)
    gluDisk(quadric, 0, 100, 32, 1)
    glTranslatef(0,0,-3)
    glRotatef(-90,1,0,0)


    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, width2, height2, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data2)
    draw_sky()
    glEnable(GL_NORMALIZE) 
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    theta += 0.5
    glRotatef(-theta, 0.0, 1.0, 0.0)

    if(N==-1):
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluSphere(quadric, 3.0, 12, 10)
        gluDeleteQuadric(quadric)

    else:     
        P1 = [
        [-6.5,-2.99, -5],
        [ 6.5,-2.99, -5],
        [ 0  ,-2.99 , 6.5],
        [ 0  ,10,-0.5],
        ]
        divide(P1[0], P1[1], P1[2], P1[3], (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), N) 

    glRotatef(2*theta, 0.0, 1.0, 0.0)
    xs = (oddalenie*-10 )* math.cos(2 * math.pi * theta / 360) 
    ys = 0+swiatlo
    zs = (oddalenie*10) * math.sin(2 * math.pi * theta / 360)
    glTranslate(xs, ys, zs)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, 2, 12, 5)
    gluDeleteQuadric(quadric)

    light_position[0] = xs
    light_position[1] = ys
    light_position[2] = zs

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)


    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)
    if(druga==1):

        glTranslate(-xs, -ys, -zs)
        xs = (oddalenie*10)* math.cos(2 * math.pi * theta / 360) 
        ys = 0+swiatlo2
        zs = (oddalenie*-10) * math.sin(2 * math.pi * theta / 360) 
        glTranslate(xs, ys, zs)

        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluSphere(quadric, 2, 12, 5)
        gluDeleteQuadric(quadric)

        light1_position[0] = xs
        light1_position[1] = ys
        light1_position[2] = zs

        glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
        glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
        glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

        glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
        glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
        glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    glFlush()


def initialize():
    pygame.init()
    display = (1400, 800)
    scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_COLOR_MATERIAL)
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, material_shininess)
    glShadeModel(GL_SMOOTH)
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 150.0)
    
    glMatrixMode(GL_MODELVIEW)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()

    return scree, viewMatrix
def handle_events(paused, displayCenter, mouseMove):
    global ex
    global ey
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return False
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                paused = not paused
                pygame.mouse.set_pos(displayCenter) 
        if not paused: 
            if event.type == pygame.MOUSEMOTION:
                delta_x, delta_y = event.rel
                ex += delta_y*0.1
                ey += delta_x*0.1
            pygame.mouse.set_pos(displayCenter)

    return paused, mouseMove

def handle_movement(keypress, mouseMove, up_down_angle, viewMatrix):
    global camera_position
    global rotation
    global x
    global y
    global z
    global swiatlo
    global swiatlo2
    global light_ambient
    global light_diffuse
    global light_specular
    global light_position
    global color
    global oddalenie
    global druga
    glPushMatrix()
    glLoadIdentity()

    if keypress[pygame.K_w]:
            x-=0.2
    if keypress[pygame.K_s]:
             x+=0.2
    if keypress[pygame.K_d]:
            y+=0.2
    if keypress[pygame.K_a]:
            y-=0.2
    if keypress[pygame.K_SPACE]:
            z+=0.2
    if keypress[pygame.K_LSHIFT]:
            z-=0.2
    if keypress[pygame.K_l]:
            light3_direction = [20.0, 20.0, 20.0, 0.0]
            glLightfv(GL_LIGHT3, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])  
            glLightfv(GL_LIGHT3, GL_DIFFUSE,  [0.2, 0.2, 0.2, 1.0])  
            glLightfv(GL_LIGHT3, GL_SPECULAR,  [0.2, 0.2, 0.2, 1.0]) 
            glLightfv(GL_LIGHT3, GL_POSITION, light3_direction)
            glEnable(GL_LIGHT3)
    if keypress[pygame.K_o]:
            glDisable(GL_LIGHT3)       
    if keypress[pygame.K_r]:   
            light_ambient = [random.random(), random.random(), random.random(), 1.0]
            light_diffuse = [random.random(), random.random(), random.random(), 1.0]
            light_specular =[random.random(), random.random(), random.random(), 1.0]
            light_position = [random.random(), random.random(), random.random(), 1.0]
    if keypress[pygame.K_1]:
            rotation*=-1;     
                    
    if keypress[pygame.K_t]:    
            glEnable(GL_TEXTURE_2D) 
    if keypress[pygame.K_y]:    
            glDisable(GL_TEXTURE_2D) 
    if keypress[pygame.K_e]:    
            glDisable(GL_LIGHTING)
    if keypress[pygame.K_UP]:    
           swiatlo+=0.2
    if keypress[pygame.K_DOWN]:    
           swiatlo-=0.2
    if keypress[pygame.K_RIGHT]:    
           swiatlo2+=0.2
    if keypress[pygame.K_LEFT]:    
           swiatlo2-=0.2
    if keypress[pygame.K_c]:    
           color*=-1
    if keypress[pygame.K_9]:    
           oddalenie-=0.2
    if keypress[pygame.K_8]:    
           oddalenie+=0.2
    if keypress[pygame.K_EQUALS]:    
           druga*=-1
    glRotatef(mouseMove[0] * 0.1, 0.0, 1.0, 0.0)
    glMultMatrixf(viewMatrix)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    camera_position = viewMatrix
    glPopMatrix()
    glMultMatrixf(viewMatrix)

    return up_down_angle, viewMatrix


def main():
    global N
    rotation = -1
    N = int(input("Podaj ile stopni piramidy: "))
    scree, viewMatrix = initialize()
    displayCenter = [scree.get_size()[i] // 2 for i in range(2)]
    mouseMove = [0, 0]
    pygame.mouse.set_pos(displayCenter)
    pygame.mouse.set_visible(False)  # Ukryj kursor myszy
    up_down_angle = 0.0
    paused = False
    run = True
    while run:
        paused, mouseMove = handle_events(paused, displayCenter, mouseMove)
        if not paused:
            keypress = pygame.key.get_pressed()
            up_down_angle, viewMatrix = handle_movement(keypress, mouseMove, up_down_angle, viewMatrix)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            draw()
            pygame.display.flip()
            pygame.time.wait(10)
    pygame.quit()
   

if __name__ == "__main__":
    main()