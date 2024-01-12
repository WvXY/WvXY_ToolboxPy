from . import main
from . import Renderer
from . import Geometry
from . import Physics
from . import Utils

# https://github.com/numpy/numpy/blob/main/numpy/__init__.py

__submodules__ = {
    "Renderer",
    "Geometry",
    "Physics",
    "Utils",
}

__all__ = list(
    __submodules__ |
    set(Renderer.__all__) |
    set(Geometry.__all__) |
    set(Physics.__all__) |
    set(Utils.__all__)
)

print("wXyEnginePy imported")

def __getattr__(name):
    if name in __submodules__:
        return __import__(name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")