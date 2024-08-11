from pathlib import Path

import moderngl
import numpy as np

from .mdgl_window import Window
from .voronoi_system import VoronoiSystem
from .basic_system import BasicSystem
from .particle_system import ParticleSystem
from .image_system import ImageSystem


# some drawing functions
class Renderer2D(Window):
    """
    This is a 2D renderer based on ModernGL.
    Draw functions are implemented here.
    """

    title = "ModernGL 2D Renderer"
    resource_dir = Path(__file__).parent.resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.basic_system = BasicSystem(ctx=self.ctx)
        self.particle_system = ParticleSystem(ctx=self.ctx)
        self.voronoi_system = VoronoiSystem(ctx=self.ctx)
        self.image_system = ImageSystem(ctx=self.ctx)

        self.grid = None

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.BLEND)

    def map_wnd_to_gl(self, x, y):
        return x / self.wnd.width * 2 - 1, 1 - y / self.wnd.height * 2

    @staticmethod
    def make_grid(n=10):  # deprecate this
        grid = np.array([], dtype="f4")
        for i in range(n * 2 + 1):
            grid = np.append(grid, [i - n, -n])
            grid = np.append(grid, [i - n, n])
            grid = np.append(grid, [-n, i - n])
            grid = np.append(grid, [n, i - n])
        return (grid / n).astype("f4")

    def draw(self):
        # the order matters
        self.voronoi_system.draw()
        self.basic_system.draw()
        self.particle_system.draw()
