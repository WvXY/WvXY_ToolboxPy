__all__ = ["animation", "primitives", "main"]

for module in __all__:
    __import__(module, globals(), locals(), level=1)