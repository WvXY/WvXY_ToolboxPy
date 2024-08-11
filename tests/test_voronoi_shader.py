import unittest
from pymrt.Interface import SimpleInterface
import moderngl
import numpy as np


class Voronoi(SimpleInterface):
    vsync = True

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.BLEND | moderngl.PROGRAM_POINT_SIZE)
        # self.draw_grid(n=10, scale=1)
        seeds = (
            np.array(
                [
                    [100, 100, 0.4],
                    [200, 300, 0.4],
                    [400, 200, 0.4],
                    [500, 400, 0.4],
                    [600, 100, 0.4],
                ],
                dtype="f4",
            )
            * (np.sin(time) + 1)
            / 2
        )

        self.voronoi_system.draw(seeds)


class VoronoiShaderTest(unittest.TestCase):
    def test_something(self):
        Voronoi.run()


if __name__ == "__main__":
    unittest.main()
