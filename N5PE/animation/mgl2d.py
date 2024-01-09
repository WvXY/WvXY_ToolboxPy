from pathlib import Path
from time import time

import imgui
import moderngl
import numpy as np
from moderngl_window.integrations.imgui import ModernglWindowRenderer

from .mgl_window import Window
from .mgl_utils2d import MglUtil2d


class Mgl2d(Window, MglUtil2d):
    gl_version = (4, 5)
    title = "ModernGL Draw in 2D"
    resource_dir = Path(__file__).parent.resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.load_program("shaders/basic_shader.glsl")
        self.particle_prog = self.load_program("shaders/particle.glsl")

    # ---------------render loop-------------------
    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.BLEND)

        # ==================
        # add code here
        self.draw_grid()
        self.draw_rectangles(np.array([[0, 0]]), np.array([[1, 1]]))
        p = np.random.randint(-10, 10, (10, 2))
        self.draw_points(p)


class MglGUIEvent(Mgl2d):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        imgui.create_context()
        self.wnd.ctx.error
        self.imgui = ModernglWindowRenderer(self.wnd)

    def render_ui(self):
        imgui.new_frame()
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", "Cmd+Q", False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        imgui.show_test_window()

        imgui.begin("Custom window", True)
        imgui.text("Bar")
        imgui.text_colored("Eggs", 0.2, 1.0, 0.0)
        imgui.end()

        imgui.render()
        self.imgui.render(imgui.get_draw_data())

    def render(self, time: float, frame_time: float):
        super().render(time, frame_time)
        self.render_ui()

    # ---------------imgui functions-------------------
    def key_event(self, key, action, modifiers):
        self.imgui.key_event(key, action, modifiers)

    def mouse_position_event(self, x, y, dx, dy):
        self.imgui.mouse_position_event(x, y, dx, dy)

    def mouse_drag_event(self, x, y, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset, y_offset):
        self.imgui.mouse_scroll_event(x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        self.imgui.mouse_press_event(x, y, button)

    def mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)

    def unicode_char_entered(self, char):
        self.imgui.unicode_char_entered(char)


if __name__ == "__main__":
    # Mgl2d.run()
    MglGUIEvent.run()
