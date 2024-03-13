import torch
import numpy as np
from numpy.linalg import norm

from .. import TORCH_DEVICE as device

# Under construction....


class Kinematics:
    def __init__(self):
        self.disp, self.vel = torch.rand(2, 2, device=device)
        # self.disp, self.vel = torch.zeros(2, 2)
        self.acc = torch.zeros(2, device=device)

    def update(self, dt):
        self.disp += self.vel * dt + 0.5 * self.acc * dt**2
        self.vel += self.acc * dt


class MassSpringSystem(object):
    def __init__(self, center, shape, adjMatrix, **kwargs):
        self.c = center
        self.s = shape
        self.adj = adjMatrix
        self.n = len(self.c)
        self.dim = self.c.shape[-1]

        self.lr = kwargs.get("lr", 1e-4)
        self.path = kwargs.get(
            "path", f"./save/s{self.s.shape[0]}-d{self.dim}.npy"
        )
        self.isEquilibrium = False
        self.beta = 0.9  # momentum term
        self.v = np.zeros((self.n, self.dim))  # momentum
        self.solve_all_overlap()

    def wdwddw(self, i, j, len_ini):
        """calculate energy, gradient and hessian of a spring(2 nodes)"""
        stiffness = self.adj[i, j]
        length = np.linalg.norm(self.c[i] - self.c[j])
        C = length - len_ini
        # unit vector from j to i
        uij = (self.c[i] - self.c[j]) / length

        w = 0.5 * stiffness * C**2  # energy
        dw = np.zeros((2, self.dim))  # gradient
        ddw = np.zeros((2, 2, self.dim, self.dim))  # hessian (untested)

        for d in range(2):
            dw[d] = stiffness * C * uij * (-1) ** d
            # for e in range(2):
            #     ddw[d, e] = stiffness * uij * uij.T * (-1) ** (d + e) \
            #         + stiffness * C * (np.eye(self.dim) - uij * uij.T) * (-1) ** (d + e)
        return w, dw, ddw

    # -------------------overlap----------------------------------
    def is_overlap(self, i, j, tolerance=0):  # AABB
        if i == j:
            return False
        if (
            abs(self.c[i] - self.c[j]) - (self.s[i] + self.s[j]) / 2.0
            <= tolerance
        ).all():
            return True
        else:
            return False

    def solve_all_overlap(self):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.is_overlap(i, j):
                    c_dist = self.c[j] - self.c[i]
                    min_dist = self.s[i] / 2 + self.s[j] / 2
                    mov = min_dist - abs(c_dist)  # [x, y, z]
                    min_axis = np.argmin(mov)
                    if c_dist[min_axis] < 0:  # i is on the left of j
                        self.c[i][min_axis] += mov[min_axis] / 2.0
                        self.c[j][min_axis] -= mov[min_axis] / 2.0
                    else:  # i is on the right of j
                        self.c[i][min_axis] -= mov[min_axis] / 2.0
                        self.c[j][min_axis] += mov[min_axis] / 2.0

    def correct_move(self, i):
        for j in range(self.n):
            if self.is_overlap(i, j):
                c_dist = self.c[j] - self.c[i]
                min_dist = self.s[i] / 2 + self.s[j] / 2
                mov = min_dist - abs(c_dist)  # [x, y, z]
                min_axis = np.argmin(mov)
                if c_dist[min_axis] < 0:  # i is on the left of j
                    self.c[i][min_axis] += mov[min_axis]
                else:  # i is on the right of j
                    self.c[i][min_axis] -= mov[min_axis]

    def position_optimize(self):
        disp = np.zeros((self.n, self.dim))
        w_sum = 0
        c_old = self.c.copy()
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.adj[i, j] != 0:
                    w, dw, ddw = self.wdwddw(i, j, 0)

                    # momentum
                    self.v[i] = self.beta * self.v[i] + self.lr * dw[0]
                    self.v[j] = self.beta * self.v[j] + self.lr * dw[1]
                    disp[i] -= self.v[i]
                    disp[j] -= self.v[j]

                    w_sum += w
        for i in range(self.n):
            self.c[i] += disp[i]
            self.correct_move(i)

        if abs(self.c - c_old).max() < 1e-2:  # reach equilibrium
            self.isEquilibrium = True

    def post_optimize(self):
        pass

    def find_border(self):
        pass

    def get_nodes(self, i):
        return (
            self.c[i] - self.s[i] / 2,
            self.c[i] + np.array([self.s[i, 0], -self.s[i, 1]]) / 2,
            self.c[i] + self.s[i] / 2,
            self.c[i] + np.array([-self.s[i, 0], self.s[i, 1]]) / 2,
        )

    def rebuild_connection(self):
        adj = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.is_overlap(i, j, tolerance=0.1):
                    adj[i, j] = 1
                    adj[j, i] = 1
        self.adj = adj

    # --------------------execute------------------------------------
    def optimize(self):  # small lr is better(no overlap) but slower
        if not self.isEquilibrium:
            self.position_optimize()
        else:  # reach equilibrium
            # print('reach equilibrium')
            self.rebuild_connection()
            self.isEquilibrium = False
            # self.rebuild_connection()
        self.solve_all_overlap()

    # ----------------some useful func-----------------
    def force3(self, i, j):  # not using
        dist2 = self.c[j] - self.c[i]
        stiffness = self.adj[i, j]
        length2 = np.linalg.norm(dist2)
        length2_init = np.linalg.norm(self.s[i] - self.s[j])
        f = stiffness * (length2 - length2_init)
        F = np.zeros((2, 2))
        angle = dist2 / length2  # [cos, sin]
        F[0] = f * angle
        F[1] = -F[0]
        return F

    def calc_energy(self):
        energy = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.adj[i, j] != 0:
                    w, _, _ = self.wdwddw(i, j, 0)
                    energy += w
        return energy

    def rotate(fixed_point, points, theta):
        """rotate the whole system"""
        R = np.array([
            [np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]
        ])
        return (R @ (points - fixed_point).T).T + fixed_point


def wdwddw(i, j, len_ini):
    """calculate energy, gradient and hessian of a spring(2 nodes)"""
    stifness = adj[i, j]
    dim = c.shape[-1]  # dimension

    length = norm(c[i] - c[j])
    C = length - len_ini
    uij = (c[i] - c[j]) / length  # unit vector from j to i

    w = 0.5 * stifness * C**2  # energy
    dw = np.zeros((2, dim))  # gradient
    ddw = np.zeros((2, 2, dim, dim))  # hessian (untested)

    for d in range(2):
        dw[d] = stifness * C * uij * (-1) ** d
        for e in range(2):
            ddw[d, e] = stifness * uij * uij.T * (-1) ** (
                d + e
            ) + stifness * C * (np.eye(dim) - uij * uij.T) * (-1) ** (d + e)
    return w, dw, ddw
