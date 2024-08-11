import moderngl

from pathlib import Path
from .mdgl_window import Window
import moderngl_window


class SystemBase(Window):
    resource_dir = Path(__file__).parent.resolve()

    def __init__(self, ctx, prog_src):
        # super().__init__(**kwargs)
        self.ctx = ctx
        self._program = self.load_program(prog_src)  # if prog_src else None

    @staticmethod
    def _release(*args):
        for arg in args:
            arg.release()

    def set_uniform(self, name: str, value: bytes):
        self._program[name].write(value)

    def draw(self):
        pass
