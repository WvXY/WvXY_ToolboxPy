import moderngl
import numpy as np

from .system_base import SystemBase


class VoronoiPushData:
    __MAX_SEEDS = 128

    def __init__(self, seeds=None):
        self.seeds = np.empty([self.__MAX_SEEDS, 3], dtype="f4")  # [x, y, w]
        if seeds is not None:
            self.len = len(seeds)
            self.seeds[: self.len] = seeds
        else:
            self.len = 0

    def update(self, seeds):
        self.seeds.fill(0)
        self.len = len(seeds)
        self.seeds[: self.len] = seeds

    def tobytes(self):
        return self.seeds.tobytes() + self.len.to_bytes(4, "little")


class VoronoiSystem(SystemBase):
    def __init__(self, ctx):
        super().__init__(ctx, "./shaders/voronoi.glsl")
        self.push_data = VoronoiPushData()
        self.boundary = None
        self.vao, self.vbo = None, None

    def set_seeds(self, seeds):
        self.push_data.update(seeds)

    def create_buffer(self, seeds, boundary=None):
        if boundary is None:
            self.set_uniform("fullCanvas", True.to_bytes(4, "little"))
            self.boundary = np.array(
                [
                    [0, 0],
                    [0, 1],
                    [1, 1],
                    [1, 0],
                ],
                dtype="f4",
            )
        else:
            self.boundary = boundary

        self.set_seeds(seeds)
        self.vbo = self.ctx.buffer(self.boundary.tobytes())

    def setup(self):
        self.set_uniform("seeds", self.push_data.seeds.tobytes())
        self.set_uniform("nSeeds", self.push_data.len.to_bytes(4, "little"))
        self.vao = self.ctx.vertex_array(self._program, self.vbo, 0)

    def draw(self):
        self.setup()
        self.vao.render(moderngl.TRIANGLE_FAN)
        self._release(self.vao, self.vbo)
        self.boundary = None
