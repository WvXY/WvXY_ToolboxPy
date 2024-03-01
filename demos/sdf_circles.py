from time import time

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import torch

from wXyEngine.Geometry.SdPrimitives import SdCircle
from wXyEngine.Physics import Kinematics
from wXyEngine.Utils import Grid as _Grid
from wXyEngine.Utils.sdf_ops import sdUnion


class Grid(_Grid):
    def __init__(self):
        super().__init__()
        self.N = 100
        self.X, self.Y, self.grid = self.make_grid()

    def calculate_grid_distance(self, sdf):
        return sdf.sd(self.grid).reshape(self.N, self.N)


grid_sampler = Grid()


# primitive shapes
class Circle(SdCircle):
    def __init__(self, radius, center=None, r=0.0):
        if center is None:
            center = [0.0, 0.0]
        super().__init__(radius, center)
        self.kin = Kinematics()
        self.kin.disp = self.center
        self.r = torch.tensor(r, device=self.device)

    def update(self, dt):
        self.kin.update(dt)
        self.center = self.kin.disp


class Animate:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.t = time()

    def init_plot_settings(self):
        # np.random.seed(0)
        self.ax.clear()
        self.ax.axis("off")
        self.ax.set_aspect("equal")

        # show fps
        # plt.title(f"FPS: {1 / (time() - self.t):.2f}")
        self.t = time()

    def main_loop(self, f):
        self.init_plot_settings()

        Z = torch.zeros([grid_sampler.N, grid_sampler.N], device=Circle.device)
        for C in Cs:
            C.update(0.1)
            z = grid_sampler.calculate_grid_distance(C)
            boundary_condition(C)

            Z = sdUnion(Z, z)

        CS = self.ax.contourf(
            grid_sampler.X.cpu().numpy(),
            grid_sampler.Y.cpu().numpy(),
            Z.cpu().numpy(),
            levels=5,
            cmap="YlGnBu",
            #   hatches=["o", "///", "o", "///", "o"]
            alpha=0.5,
        )
        self.ax.contour(
            grid_sampler.X.cpu().numpy(),
            grid_sampler.Y.cpu().numpy(),
            Z.cpu().numpy(),
            levels=5,
        )

    def animate(self):
        self.t = time()
        anim = FuncAnimation(
            self.fig, self.main_loop, repeat=False, frames=300, interval=0
        )
        plt.show()
        # anim.save("demo_sdf.gif", writer="imagemagick", fps=60)


def boundary_condition(obj, scene=grid_sampler):
    if obj.center[0] - obj.radius <= scene.xmin:
        obj.kin.vel[0] = -obj.kin.vel[0]
    elif obj.center[0] + obj.radius >= scene.xmax:
        obj.kin.vel[0] = -obj.kin.vel[0]
    if obj.center[1] - obj.radius <= scene.ymin:
        obj.kin.vel[1] = -obj.kin.vel[1]
    elif obj.center[1] + obj.radius >= scene.ymax:
        obj.kin.vel[1] = -obj.kin.vel[1]


if __name__ == "__main__":
    Cs = []
    for i in range(8):
        Cs.append(Circle(1, r=0.2))

    Animate().animate()
