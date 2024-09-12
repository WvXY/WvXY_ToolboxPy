from ..Renderer.renderer import Renderer

import moderngl
import imgui
from moderngl_window.integrations.imgui import ModernglWindowRenderer


class SimpleApp(Renderer):
    """
    A simple Application demo
    Just showing but not interactive
    """

    title = "Simple App Base"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def map_wnd_to_gl(self, x, y):
        return x / self.wnd.width * 2 - 1, 1 - y / self.wnd.height * 2

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.BLEND | moderngl.PROGRAM_POINT_SIZE)


class SimpleAppInteractive(SimpleApp):
    """
    A simple interface as demo
    Can take input from mouse and keyboard
    """

    title = "Simple Application with Interaction"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def mouse_press_event(self, x, y, button):
        fixed_x, fixed_y = self.map_wnd_to_gl(x, y)
        # print(f"mouse press at {fixed_x}, {fixed_y}")

    def mouse_position_event(self, x, y, dx, dy):
        fixed_x, fixed_y = self.map_wnd_to_gl(x, y)
        # print(f"mouse move to {fixed_x}, {fixed_y}")

    def mouse_drag_event(self, x, y, dx, dy):
        fixed_x, fixed_y = self.map_wnd_to_gl(x, y)
        # print(f"mouse drag to {fixed_x}, {fixed_y}")


class SimpleAppWithImgui(SimpleApp):
    """
    A simple interface template using imgui
    Don't forget to override the render_ui function
    and call self.render_ui() in render function
    """

    title = "Simple Application with Imgui"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        imgui.create_context()
        self.wnd.ctx.error()
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

    # --------------- event functions -------------------
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
        # print("new x, y:", self.map_wnd_to_gl(x, y))

    def mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)

    def unicode_char_entered(self, char):
        self.imgui.unicode_char_entered(char)
