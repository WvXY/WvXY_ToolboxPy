import numpy as np


class Grid:
    def __init__(self, xmin=-50, xmax=50, ymin=-50, ymax=50, N=256):
        self.N = N
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.X, self.Y, self.grid = self.make_grid(
            self.xmin, self.xmax, self.ymin, self.ymax
        )

    def __init__(self, N=256):
        self.N = N
        self.X, self.Y, self.grid = self.make_grid(
            self.xmin, self.xmax, self.ymin, self.ymax
        )

    def make_grid(self, xmin, xmax, ymin, ymax):
        x = np.linspace(xmin, xmax, self.N)
        y = np.linspace(ymin, ymax, self.N)
        X, Y = np.meshgrid(x, y)
        grid = np.stack([X.flatten(), Y.flatten()], axis=-1)
        return X, Y, grid

    def calculate_grid_distance(self, sd):
        sd = sd(self.grid)
        return sd.reshape(self.N, self.N)  # , gd.reshape(2, self.N, self.N)
