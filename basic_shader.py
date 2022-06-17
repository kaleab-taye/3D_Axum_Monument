import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from OpenGL.GL.shaders import *
import numpy as np
import os
from PIL import Image

triangleVAO, program, texture = None, None, None


def getFileContents(filename):
    p = os.path.join(os.getcwd(), "shaders", filename)
    return open(p, 'r').read()


def init():
    global triangleVAO, program, texture
    pygame.init()
    display = (500, 500)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(.30, 0.20, 0.20, 1.0)
    glViewport(0, 0, 500, 500)

    vertexShaderContent = getFileContents("triangle.vertex.shader")
    fragmentShaderContent = getFileContents("triangle.fragment.shader")

    vertexShader = compileShader(vertexShaderContent, GL_VERTEX_SHADER)
    fragmentShader = compileShader(fragmentShaderContent, GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)
    glLinkProgram(program)
    # vertexes = np.array([
    #     [0.5, 0.0, 0.0,     0.0, 0.0, 1.0],
    #     [-0.5, 0.0, 0.0,    0.0, 1.0, 0.0],
    #     [0, 0.5, 0.0,       1.0, 0.0, 0.0]], dtype=np.float32)

    vertexes = np.array([
        # position          # color           # texture s, r
        [0.5, 0.5, -.50,    1.0, 0.20, 0.8,     1.0, 1.0],
        [0.5, -0.5, -.50,   1.0, 1.0, 0.0,      1.0, 0.0],
        [-0.5, 0.5, -.50,   0.0, 0.7, 0.2,      0.0, 1.0],

        [0.5, -0.5, -.50,   1.0, 1.0, 0.0,      1.0, 0.0],
        [-0.5, -0.5, -.50,  0.0, 0.4, 1.0,      0.0, 0.0],
        [-0.5, 0.5, -.50,   0.0, 0.7, 0.2,      0.0, 1.0],

    ], dtype=np.float32)

    triangleVBO = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, triangleVBO)
    glBufferData(GL_ARRAY_BUFFER, vertexes.nbytes, vertexes, GL_STATIC_DRAW)

    triangleVAO = glGenVertexArrays(1)
    glBindVertexArray(triangleVAO)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                          3 * vertexes.itemsize, None)
    positionLocation = glGetAttribLocation(program, "position")
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                          8 * vertexes.itemsize, ctypes.c_void_p(0))

    glEnableVertexAttribArray(0)

    colorLocation = glGetAttribLocation(program, "color")
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                          8 * vertexes.itemsize, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    texLocation = glGetAttribLocation(program, "texCoord")
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                          8*vertexes.itemsize, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open("images/up.png")
    width, height = image.size

    image_data = np.array(list(image.getdata()), dtype=np.uint8)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB,
                 GL_UNSIGNED_BYTE, image_data)

    glGenerateMipmap(GL_TEXTURE_2D)

    # unbind VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    # unbind VAO
    glBindVertexArray(0)


def draw():
    global triangleVAO, program, texture
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(program)
    glBindVertexArray(triangleVAO)

    glBindTexture(GL_TEXTURE_2D, texture)

    glDrawArrays(GL_TRIANGLES, 0, 6)

    glBindTexture(GL_TEXTURE_2D, 0)
    glBindVertexArray(0)


def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        draw()
        pygame.display.flip()
        pygame.time.wait(10)


main()
