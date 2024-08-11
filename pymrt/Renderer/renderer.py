from pathlib import Path
import moderngl

from .mdgl_window import Window
from .voronoi_system import VoronoiSystem
from .basic_system import BasicSystem
from .particle_system import ParticleSystem
from .image_system import ImageSystem


class Renderer(Window):
    """
    A 2D renderer using ModernGL.
    """

    resource_dir = Path(__file__).parent.resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.basic_system = BasicSystem(ctx=self.ctx)
        self.particle_system = ParticleSystem(ctx=self.ctx)
        self.voronoi_system = VoronoiSystem(ctx=self.ctx)
        self.image_system = ImageSystem(ctx=self.ctx)

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.BLEND)

    def draw(self):
        # the order matters
        self.voronoi_system.draw()
        self.basic_system.draw()
        self.particle_system.draw()
