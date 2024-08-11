import moderngl
import numpy as np

from .system_base import SystemBase


class ParticleSystem(SystemBase):
    def __init__(self, ctx):
        super().__init__(ctx, "./shaders/particle.glsl")
        self.point_size = 10
        self.use_circle = True

        self.vao, self.vbo, self.ebo = None, None, None

    def set_point_size(self, size):
        self.point_size = size
        self.set_uniform("point_size", self.point_size.to_bytes(4, "little"))

    def set_use_circle(self, use_circle):
        self.use_circle = use_circle
        self.set_uniform("use_circle", self.use_circle.to_bytes(4, "little"))

    def draw(self, vertices=None, indices=None, point_size=40, use_circle=True):
        self._program["point_size"].value = self.point_size
        self._program["use_circle"].value = self.use_circle
        vbo = self.ctx.buffer(np.array(vertices, dtype="f4"))

        has_indices = indices is not None
        if has_indices:
            ebo = self.ctx.buffer(np.array(indices, dtype="i4"))
            vao_content = [
                (vbo, "2f", 0),
                (ebo, "1i", 1),
            ]
        else:
            vao_content = [
                (vbo, "2f", 0),
                # (indices_buffer, "1i /r", 1), # maybe specify a color
            ]

        vao = self.ctx.vertex_array(self._program, vao_content)
        vao.render(moderngl.POINTS)

        if has_indices:
            self._release(vao, vbo, ebo)
        else:
            self._release(vao, vbo)

    # def draw(self):
    #     self.vao = self.ctx.vertex_array(self._program, vao_content)
    #     self.vao.render(moderngl.POINTS)
    #
    #     self._release(self.vao, self.vbo, self.ebo)
