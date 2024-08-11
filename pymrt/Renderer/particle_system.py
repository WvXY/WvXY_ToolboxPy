import moderngl
import numpy as np
import torch

from .system_base import SystemBase


class ParticleSystem(SystemBase):
    def __init__(self, ctx):
        super().__init__(ctx, "./shaders/particle.glsl")
        self.point_size = 10
        self.rect_mode = False

        self.particles = []
        self.vao, self.vbo, self.ebo = None, None, None

    # def set_point_size(self, size):
    #     self.point_size = size
    #     self.set_uniform("point_size", self.point_size.to_bytes(4, "little"))

    def set_to_rect_mode(self, rect_mode):
        self.rect_mode = rect_mode
        self.set_uniform("rectMode", self.rect_mode.to_bytes(4, "little"))

    def create_buffer(
        self,
        pos: list | np.ndarray | torch.Tensor = None,
        color=[0.0, 0.0, 0.0],
        point_size: float = 6,
    ):
        for i in range(len(pos)):
            self.particles.append((*pos[i], *color, point_size))

    def setup(self):
        self.set_uniform("rectMode", self.rect_mode.to_bytes(4, "little"))
        self.vbo = self.ctx.buffer(np.array(self.particles, dtype="f4"))

        vao_content = [(self.vbo, "2f 3f 1f", 0, 1, 2)]

        self.vao = self.ctx.vertex_array(self._program, vao_content)

    def draw(self):
        self.setup()
        self.vao.render(moderngl.POINTS)
        # clean up
        self.particles.clear()
        self._release(self.vao, self.vbo, self.ebo)
