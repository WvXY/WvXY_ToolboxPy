from . import mdgl_window, mdgl_utils, renderer_2d, renderer_3d

__all__ = ["mdgl_window", "mdgl_utils", "renderer_2d", "renderer_3d"]


def __getattr__(name):
    if name in __all__:
        return __import__(name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
