import moderngl
import numpy as np

import w_tbx.Geometry as Geometry
import w_tbx.Interface.interface as Interface


class HelloWorld(Interface.SimpleAppInteractive):
    title = "Hello World"
    vsync = True
    window_size = (800, 600)
    resizable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_objects = Geometry.GameObjectManager()
        self.position = (0, 0, 0)

    def render(self, time: float, frame_time: float):
        self.ctx.clear(0.2, 0.4, 0.6)
        self.ctx.enable(moderngl.BLEND | moderngl.PROGRAM_POINT_SIZE)

        self.particle_system.create_buffer([self.position], [100])
        self.particle_system.draw()


if __name__ == "__main__":
    HelloWorld.run()
