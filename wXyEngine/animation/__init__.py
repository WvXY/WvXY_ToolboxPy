__all__ = ["mgl_window", "mgl_2d", "mgl_utils2d",  "mgl_3d"]

for module in __all__:
    __import__(module, globals(), locals(), level=1)
