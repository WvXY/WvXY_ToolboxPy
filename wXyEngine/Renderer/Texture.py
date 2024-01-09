import moderngl
import numpy as np
from PIL import Image

from .MdglWindow import Window

# Define the size of the window and the pixel matrix
window_width = 800
window_height = 600
matrix_width = 100
matrix_height = 100


class VisualAsPixels(Window):
    gl_version = (3, 3)
    title = "Research 3D Visualization"
    resizable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a shader program
        self.prog = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_vert;
            out vec2 frag_tex;
            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
                frag_tex = in_vert;
            }
            """,
            fragment_shader="""
            #version 330
            uniform sampler2D image;
            in vec2 frag_tex;
            out vec4 fragColor;
            void main() {
                fragColor = texture(image, frag_tex);
            }
            """,
        )

        # image = Image.open("test.jpg")
        # image_data = np.array(image)
        image_data = np.random.randint(
            0, 255, (matrix_width, matrix_height, 3), dtype=np.uint8
        )
        height, width, _ = image_data.shape

        # Create a VBO for a quad
        quad_data = (
            np.array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype="f4") / 2.0
        )

        vbo = self.ctx.buffer(quad_data)
        self.vao = self.ctx.simple_vertex_array(self.prog, vbo, "in_vert")

        self.texture = self.ctx.texture((width, height), 3, image_data.tobytes())
        self.texture.build_mipmaps()

    def render(self, time, frame_time):
        # Clear the screen
        # self.ctx.enable(moderngl.BLEND)
        self.ctx.clear()
        self.prog["image"].value = 0

        self.texture.use()
        self.vao.render(moderngl.TRIANGLE_STRIP)

    def key_event(self, key, action, modifiers):
        if key == self.keys.ESCAPE and action == self.keys.ACTION_PRESS:
            self.close()


if __name__ == "__main__":
    VisualAsPixels.run()
