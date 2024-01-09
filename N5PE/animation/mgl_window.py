import moderngl
import numpy as np
import moderngl_window as mglw
from pyrr import Matrix44
from moderngl_window.integrations.imgui import ModernglWindowRenderer
import imgui


# initialize window
class Window(mglw.WindowConfig):
    gl_version = (4, 5)
    title = "ModernGL Window"
    window_size = (800, 600)
    aspect_ratio = 4 / 3
    resizable = True
    samples = 4  # anti-aliasing
    cursor = True
    vsync = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
