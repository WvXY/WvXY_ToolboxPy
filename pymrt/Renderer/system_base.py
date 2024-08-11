import moderngl

from pathlib import Path
from pymrt.Renderer.mdgl_window import Window


class SystemBase(Window):
    resource_dir = Path(__file__).parent.resolve()

    def __init__(self, ctx, program=None):
        self.ctx = ctx
        self.program = program if program else None

    def release_resources(self, *args):
        for arg in args:
            arg.release()

    def draw(self):
        pass
