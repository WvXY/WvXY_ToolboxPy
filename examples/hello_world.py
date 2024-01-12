import moderngl

import wXyEngine as xe
import wXyEngine.Geometry as Geometry
import wXyEngine.Renderer as Renderer


class HelloWorld(Renderer.Mdgl2d.Mdgl2d):
    title = "Hello World"
    vsync = True
    window_size = (800, 600)
    resizable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_objects = Geometry.GameObject()

    def render(self, time: float, frame_time: float):
        self.ctx.clear(0.2, 0.4, 0.6)

        self.ctx.enable(moderngl.BLEND)


if __name__ == "__main__":
    HelloWorld.run()


