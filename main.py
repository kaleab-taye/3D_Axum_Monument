import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from dataLoaders.TextureLoader import load_texture
from dataLoaders.ObjLoader import ObjLoader


vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;
uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;
out vec2 v_texture;
void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330
in vec2 v_texture;
out vec4 out_color;
uniform sampler2D s_texture;
void main()
{
    out_color = texture(s_texture, v_texture);
}
"""


# glfw callback functions
def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(
        20, width / height, 0.1, 1000)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

# def scroll_callback(window, xoffset, yoffset):

# # eye, target, up
#     view = pyrr.matrix44.create_look_at(pyrr.Vector3(
#     [0+xoffset, 50+yoffset, 220]), pyrr.Vector3([0, 20, 0]), pyrr.Vector3([0, 4, 0]))
#     pass


if not glfw.init():
    raise Exception("glfw initialization failed!")


window = glfw.create_window(1280, 720, "Axum Monument", None, None)


if not window:
    glfw.terminate()
    raise Exception("glfw window creation failed!")


glfw.set_window_pos(window, 500, 300)


glfw.set_window_size_callback(window, window_resize)


glfw.make_context_current(window)

######################################################################test
# glfw.SetScrollCallback(window, scroll_callback)

axum_indices, axum_buffer = ObjLoader.load_model("Axum monument v-07.obj")

shader = compileProgram(compileShader(
    vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# VAO and VBO
VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)

glBindVertexArray(VAO)

glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, axum_buffer.nbytes,
             axum_buffer, GL_STATIC_DRAW)


glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      axum_buffer.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      axum_buffer.itemsize * 8, ctypes.c_void_p(12))

glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      axum_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)


textures = glGenTextures(1)
# load_texture("texture/collection07.jpg", textures)
load_texture("texture/collection09.jpg", textures)

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST) 

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(
    20, 1280 / 720, 0.1, 1000)
chibi_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, -10]))


view = pyrr.matrix44.create_look_at(pyrr.Vector3(
    [0, 50, 220]), pyrr.Vector3([0, 20, 0]), pyrr.Vector3([0, 4, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)


while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_y = pyrr.Matrix44.from_y_rotation(0.2 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, chibi_pos)


    glBindVertexArray(VAO)
    glBindTexture(GL_TEXTURE_2D, textures)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(axum_indices))

    glfw.swap_buffers(window)


glfw.terminate()
