import moderngl
import numpy as np
from PIL import Image

from .system_base import SystemBase


class ImageSystem(SystemBase):
    def __init__(self, ctx):
        super().__init__(ctx, "./shaders/texture.glsl")

        self.vert_and_coord = np.array(
            [  # x, y, u, v
                [-1.0, -1.0, 0.0, 1.0],
                [1.0, -1.0, 1.0, 1.0],
                [-1.0, 1.0, 0.0, 0.0],
                [1.0, 1.0, 1.0, 0.0],
            ],
            dtype="f4",
        ).flatten()  # uv is x-axis flipped

        self.texture = None
        self.vao, self.vbo = None, None

    @staticmethod
    def load_image(path):
        return np.array(Image.open(path))

    def create_buffer(self, image_data: np.ndarray):
        height, width, _ = image_data.shape
        self.texture = self.ctx.texture(
            (width, height), 3, image_data.astype(np.uint8).tobytes()
        )

        self.vbo = self.ctx.buffer(self.vert_and_coord)
        self.vao = self.ctx.vertex_array(self._program, [(self.vbo, "4f", 0)])
        self.texture.build_mipmaps()

    def setup(self):
        self.texture.use()

    def draw(self):
        self.setup()
        self.vao.render(moderngl.TRIANGLE_STRIP)
        self._release(self.vao, self.vbo, self.texture)
