import moderngl
from ..Renderer.mdgl_window import Window


class KbdController(Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keys = {}
        self.mouse = {}

    def mouse_position(self, x, y, dx, dy):
        self.mouse['x'] = x
        self.mouse['y'] = y
        self.mouse['dx'] = dx
        self.mouse['dy'] = dy

    def mouse_delta(self, dx, dy):
        self.mouse['dx'] = dx
        self.mouse['dy'] = dy

    def mouse_scroll(self, x_offset, y_offset):
        self.mouse['scroll'] = y_offset
        self.mouse['scroll_dx'] = x_offset
        self.mouse['scroll_dy'] = y_offset

    def mouse_press(self, x, y, button):
        if button == moderngl.MOUSE_BUTTON_LEFT:
            self.mouse['left'] = True
        elif button == moderngl.MOUSE_BUTTON_RIGHT:
            self.mouse['right'] = True
        elif button == moderngl.MOUSE_BUTTON_MIDDLE:
            self.mouse['middle'] = True

    def mouse_release(self, x, y, button):
        if button == moderngl.MOUSE_BUTTON_LEFT:
            self.mouse['left'] = False
        elif button == moderngl.MOUSE_BUTTON_RIGHT:
            self.mouse['right'] = False
        elif button == moderngl.MOUSE_BUTTON_MIDDLE:
            self.mouse['middle'] = False

    def key_press(self, key, modifiers):
        self.keys[key] = True

    def key_release(self, key, modifiers):
        self.keys[key] = False

    def is_pressed(self, key):
        pass