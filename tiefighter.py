#use PyOpenGL to render 3d model of tiefighter (done)
#use a glowing cylinder to make a green laser (done)
#make it fly around ("""done""")
#make lasers fire on click (done)
#find way to do input (done)


#imports
from unittest import skip 
import pygame #make windows
from pygame.locals import * #allow opengl compatability
from OpenGL.GL import * #graphics library
from OpenGL.GLU import * #GL utility
from OpenGL.arrays import vbo #vertex buffer objects
from OpenGL.GL import shaders
import pywavefront #model importer

sensitivity = 20

laserverts = (
    (0,0,10),
    (0,0,-10)
)

laseredge = (
    (0, 1),
    (0, 0)
)

scene = pywavefront.Wavefront('CazaTie.obj', collect_faces=True, create_materials=True) #import tiefighter model (no materials)

scene_box = (scene.vertices[0], scene.vertices[0]) #create a scene
for vertex in scene.vertices: #add model to scene
    min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)] #negetive corner
    max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)] #positive corner
    scene_box = (min_v, max_v) #Scene container

scene_trans    = [-(scene_box[1][i]+scene_box[0][i])/2 for i in range(3)] #transform of the scene itself

scaled_size    = 5 #scene scale
scene_size     = [scene_box[1][i]-scene_box[0][i] for i in range(3)] #scene size
max_scene_size = max(scene_size) #the maximum scene size
scene_scale    = [scaled_size/max_scene_size for i in range(3)]

def Model():
    glPushMatrix() #push the models matrix to render
    glScalef(*scene_scale) #set the scene scale
    glTranslatef(*scene_trans) #set the scene transform

    for mesh in scene.mesh_list: #render meshes
        glBegin(GL_TRIANGLES) #primitive used to render 
        glColor3fv((1,1,1))
        for face in mesh.faces: #draw mesh faces
            for vertex_i in face: #collect tri vertexes
                glVertex3f(*scene.vertices[vertex_i]) #apply vertex
        glEnd() #end

    glPopMatrix() #remove render matrix

def laser(pos):
    glPushMatrix() #push the models matrix to render
    glScalef(*scene_scale) #set the scene scale
    glTranslatef(*scene_trans) #set the scene transform

    for mesh in scene.mesh_list: #render meshes
        glBegin(GL_LINES) #primitive used to render 
        glColor3fv((0,1,0))
        for edge in laseredge:
            for vert in edge:
                originpos = laserverts[vert]
                newpos = (originpos[0]+pos[0],originpos[1]+pos[1],originpos[2]+pos[2])
                glVertex3fv(newpos)
        glEnd() #end

    glPopMatrix() #remove render matrix

def main(): 
    pygame.init() #start pygame
    display = (1280,720) #display size in SD
    screen = pygame.display.set_mode(display,DOUBLEBUF|OPENGL) #apply opengl to the display window and change the render type to double buffer (standard for 3d)
    pygame.display.set_caption("TIEFIGHTER SIMULATOR")

    laserstart = (56.5,38,30)
    laserpos = laserstart

    mouse = pygame.mouse
    mouse.set_visible(False)
    gluPerspective(70,(display[0]/display[1]),0.1,100.0) #setup the camera

    glTranslatef(0.0,0.0,-7) #set the scene position

    glRotatef(0,0,0,0) #set the rotation of the scene

    while True:
        for event in pygame.event.get():  #quit when the pygame window is closed
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #mouse click input
                if mouse.get_pressed()[0]:
                    laserpos = laserstart
        #clear the buffers
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #mouse input
        move = mouse.get_rel()
        #make sure mouse doesnt leave during rotation
        if mouse.get_focused():
            mouse.set_pos((screen.get_width()/2,screen.get_height()/2))

        Model() #mode func
        laser(laserpos)
        last = laserpos
        laserpos = (last[0],last[1],last[2]+8)
        if abs(move[0] + move[1]) > 0:
            #no idea why but if i use the function without actually rotating the model it will slowly move away
            #this if statement fixes that
            glRotatef(1,move[1] * sensitivity,move[0] * sensitivity,0) #spin the model with mouse input
        pygame.display.flip() #swap buffer
        pygame.time.wait(10) #wait to render the next frame

main()