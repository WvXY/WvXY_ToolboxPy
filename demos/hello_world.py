import moderngl

import PyMRT.Geometry as Geometry
import PyMRT.Interface.interface as Interface


class HelloWorld(Interface.SimpleInterfaceInteractive):
    title = "Hello World"
    vsync = True
    window_size = (800, 600)
    resizable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_objects = Geometry.GameObjectManager()

    def render(self, time: float, frame_time: float):
        self.ctx.clear(0.2, 0.4, 0.6)

        self.ctx.enable(moderngl.BLEND)


if __name__ == "__main__":
    HelloWorld.run()
