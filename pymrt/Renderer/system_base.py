from .mdgl_window import Window


class SystemBase(Window):
    def __init__(self, ctx, prog_src):
        self.ctx = ctx
        self._program = self.load_program(prog_src)  # if prog_src else None

    def set_uniform(self, name: str, value: bytes):
        self._program[name].write(value)

    def create_buffer(self, **kwargs):
        pass

    def setup(self, **kwargs):
        pass

    def draw(self, **kwargs):
        pass

    @staticmethod
    def _release(*args):
        for arg in args:
            if arg is None:
                continue
            arg.release()
