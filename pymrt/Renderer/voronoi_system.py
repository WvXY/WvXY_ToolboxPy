import moderngl
import numpy as np

from .system_base import SystemBase


class VoronoiPushData:
    __MAX_SEEDS = 128

    def __init__(self, seeds=None):
        self.seeds = np.empty([self.__MAX_SEEDS, 3], dtype="f4")
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
        self.seeds = np.empty((0, 3))  # [x, y, w]
        self.push_data = VoronoiPushData()
        # self._program = self.load_program("./shaders/voronoi.glsl")

    def set_seeds(self, seeds):
        self.seeds = seeds
        self.push_data.update(seeds)

    # def set_uniform(self, name, value):
    #     self._program[name].write(value.tobytes())

    def draw(self, seeds=None, boundary=None):
        if seeds is not None:
            self.set_seeds(seeds)
        if self.seeds is None:
            raise ValueError("Seeds are None")

        self.set_uniform("seeds", self.push_data.seeds.tobytes())
        self.set_uniform("nSeeds", self.push_data.len.to_bytes(4, "little"))

        if boundary is not None:
            boundary = np.array(boundary, dtype="f4")
            boundary_vbo = self.ctx.buffer(boundary.tobytes())
            boundary_vao = self.ctx.vertex_array(
                self._program, boundary_vbo, "in_vert"
            )
            boundary_vao.render(moderngl.TRIANGLE_FAN)
            self._release(boundary_vbo, boundary_vao)
        else:
            view = np.array(
                [-1, -1, -1, 1, 1, -1, 1, 1], dtype="f4"
            )  # Cover the viewport (not used)
            view_vbo = self.ctx.buffer(view.tobytes())
            view_vao = self.ctx.vertex_array(self._program, view_vbo, "in_vert")
            view_vao.render(moderngl.TRIANGLE_STRIP)
            self._release(view_vbo, view_vao)
