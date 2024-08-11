import unittest
from pymrt.Interface import SimpleInterface
import moderngl
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_draw_image(self):
        class ImageDrawTest(SimpleInterface):
            vsync = True
            samples = 8

            def render(self, time, frame_time):
                self.ctx.clear(1.0, 1.0, 1.0)
                self.ctx.enable(moderngl.BLEND | moderngl.PROGRAM_POINT_SIZE)

                # img = np.random.randint(0, 255, (1200, 800, 3), dtype=np.uint8)
                img = self.image_system.load_image("../doc/test_pic.jpg")

                self.image_system.create_buffer(img)
                self.image_system.draw()

                # self.voronoi_system.create_buffer(seeds)
                # self.voronoi_system.draw()

        ImageDrawTest.run()

    def test_draw_voronoi(self):
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
                            [300, 100, 0.4],
                        ],
                        dtype="f4",
                    )
                    * (np.sin(time) + 1)
                    / 2
                )

                self.voronoi_system.create_buffer(seeds)
                self.voronoi_system.draw()

        Voronoi.run()


if __name__ == "__main__":
    unittest.main()
