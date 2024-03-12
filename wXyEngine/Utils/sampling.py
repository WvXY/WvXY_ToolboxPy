import matplotlib.patches
import matplotlib.pyplot as plt
import numpy as np
import torch
from del_msh import TriMesh, PolyLoop

from .. import TORCH_DEVICE as device

torch.set_default_dtype(torch.float64)


class Boundary:
    def __init__(self, vtx):
        self.vtx = np.array(vtx, dtype=np.float32)
        self.sample_points = None

        if self.area < 0:  # flip if clockwise
            self.vtx = np.flip(self.vtx, axis=0)

        self.tri2vtx, self.vtx2xy = PolyLoop.tesselation2d(self.vtx)

    def sample_inside(self, n, inplace=False, device="cpu"):
        if inplace:
            self.sample_points = torch.tensor(
                TriMesh.sample_many(self.tri2vtx, self.vtx2xy, n), device=device
            )
        else:
            return torch.tensor(
                TriMesh.sample_many(self.tri2vtx, self.vtx2xy, n), device=device
            )

    @property
    def area(self):
        vtx = torch.from_numpy(self.vtx)
        vtx_shifted = torch.roll(vtx, 1, dims=0)
        return (
            torch.sum(
                vtx[:, 1] * vtx_shifted[:, 0] - vtx[:, 0] * vtx_shifted[:, 1]
            )
            / 2.0
        )

    # TODO: move it to Renderer module
    def draw_boundary(self, ax, draw_points=False, auto_aspect=False):
        if auto_aspect:
            ax.set_aspect("equal")
            ax.set_xlim(min(self.vtx[:, 0]) - 1, max(self.vtx[:, 0]) + 1)
            ax.set_ylim(min(self.vtx[:, 1]) - 1, max(self.vtx[:, 1]) + 1)

        ax.add_patch(
            matplotlib.patches.Polygon(
                self.vtx,
                closed=True,
                fill=False,
                linewidth=2,
                linestyle="dashdot",
                edgecolor="darkgreen",
                alpha=0.7,
            )
        )

        if draw_points:
            ax.scatter(
                self.sample_points[:, 0],
                self.sample_points[:, 1],
                s=1,
            )


class Grid:
    N = 128
    xmin, xmax, ymin, ymax = -5, 5, -5, 5

    def __init__(self, N=None, range=None):
        self.N = N if N else self.N
        self.xmin = range[0] if range else self.xmin
        self.xmax = range[1] if range else self.xmax
        self.ymin = range[2] if range else self.ymin
        self.ymax = range[3] if range else self.ymax

    def make_grid(self):
        x = np.linspace(self.xmin, self.xmax, self.N)
        y = np.linspace(self.ymin, self.ymax, self.N)
        X, Y = np.meshgrid(x, y)
        grid = np.stack([X.flatten(), Y.flatten()], axis=-1)
        return (
            torch.from_numpy(X).to(device),
            torch.from_numpy(Y).to(device),
            torch.from_numpy(grid).to(device),
        )

    # X, Y, grid = make_grid()

    def calculate_grid_distance(self, signed_distance):
        return signed_distance(self.grid).reshape(self.N, self.N)


if __name__ == "__main__":
    # vtx2xy_in = np.array(
    #     [[0, 0],
    #     [1, 0],
    #     [1, 0.8],
    #     [0.6, 0.6],
    #     [0.6, 1.2],
    #     [0, 1]], dtype=np.float32
    # )
    vtx2xy_in = np.array([[-1, 0], [0, -1], [1, 0], [0, 1]], dtype=np.float32)

    B = Boundary(vtx2xy_in)
    B.sample_inside(inplace=True)

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    B.draw_boundary(ax, draw_points=True)
    plt.show()
    print(B.area)
