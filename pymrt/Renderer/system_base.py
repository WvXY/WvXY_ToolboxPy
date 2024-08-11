import moderngl

from pathlib import Path
from .mdgl_window import Window
import moderngl_window


class SystemBase(Window):
    resource_dir = Path(__file__).parent.resolve()

    def __init__(self, ctx, prog_src):
        self.ctx = ctx
        self._program = self.load_program(prog_src)  # if prog_src else None

    def set_uniform(self, name: str, value: bytes):
        self._program[name].write(value)

    def create_buffer(self):
        pass

    def setup(self):
        pass

    def draw(self):
        pass

    @staticmethod
    def _release(*args):
        for arg in args:
            if arg is None:
                continue
            arg.release()
