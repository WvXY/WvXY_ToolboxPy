from w_tbx.Interface.interface import SimpleAppInteractive
import moderngl
import numpy as np


class MouseEventDemo(SimpleAppInteractive):
    resizable = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mouse_pos = (0, 0)
        self.mouse_pos_str = "mouse pos: (0, 0)"
        self.mouse_button = "mouse button: None"
        self.mouse_wheel = "mouse wheel: 0"
        self.mouse_drag = "mouse drag: None"

        self.point_list = [[0, 0]]
        self.start_draw = False

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.BLEND | moderngl.PROGRAM_POINT_SIZE)

        self.draw_grid()
        # self.draw_rectangles(np.array([[0, 0]]), np.array([[1, 1]]))
        # p = np.random.randint(-10, 10, (10, 2))
        # self.draw_points(p)

        self.particle_prog["point_size"].value = 100
        if self.point_list:
            self.draw_particles(
                np.array(self.point_list).astype("f4"),
                np.arange(len(self.point_list)).astype("i4"),
            )

    def mouse_press_event(self, x, y, button):
        # fixed_x, fixed_y = self.map_wnd_to_gl(x, y)
        # self.point_list.append([fixed_x, fixed_y])
        self.start_draw = not self.start_draw

    def mouse_position_event(self, x, y, dx, dy):
        if not self.start_draw:
            return
        fixed_x, fixed_y = self.map_wnd_to_gl(x, y)
        self.point_list.append([fixed_x, fixed_y])

    def map_wnd_to_gl(self, x, y):
        return x / self.wnd.width * 2 - 1, 1 - y / self.wnd.height * 2

    # def draw_text(self, text, pos):
    #     self.text.render(text, pos)


if __name__ == "__main__":
    MouseEventDemo.run()
