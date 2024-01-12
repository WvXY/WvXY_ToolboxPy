from . import (
    MdglWindow,
    Mdgl2d,
    MdglUtils2d,
    Mdgl3d,
    Texture
)

__all__ = [
    "MdglWindow",
    "Mdgl2d",
    "MdglUtils2d",
    "Mdgl3d"
]


def __getattr__(name):
    if name in __all__:
        return __import__(name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")