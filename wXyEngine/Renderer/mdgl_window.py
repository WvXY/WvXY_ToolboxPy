import moderngl_window


# initialize window
class Window(moderngl_window.WindowConfig):
    gl_version = (4, 6)
    title = "ModernGL Window"
    window_size = (1280, 720)
    aspect_ratio = 1280 / 720
    resizable = True
    samples = 4  # anti-aliasing
    cursor = True
    vsync = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

