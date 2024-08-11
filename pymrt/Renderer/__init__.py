from . import mdgl_window, utils, renderer

__all__ = ["utils", "renderer"]


def __getattr__(name):
    if name in __all__:
        return __import__(name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
