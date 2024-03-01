from time import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm


# TODO: refactor those functions to Physics module
# =====================spring system================================================
def force2(i, j):
    stifness = adj[i, j]
    dist2 = c[j] - c[i]
    length2 = norm(dist2)
    length2_init = norm(xy[i] - xy[j])
    f = stifness * (length2 - length2_init)
    F = np.zeros((2, 2))
    angle = dist2 / length2  # [cos, sin]
    F[0] = f * angle
    F[1] = -F[0]
    return F


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


# =====================collision================================================
def AABB(i, j):
    if i == j:
        return False
    imax = c[i] + xy[i] / 2
    imin = c[i] - xy[i] / 2
    jmax = c[j] + xy[j] / 2
    jmin = c[j] - xy[j] / 2
    if (imax - jmin < 0).any() or (jmax - imin < 0).any():
        return False
    else:
        return True


def solve_collision(i):
    n = len(c)
    for j in range(n):
        if AABB(i, j):
            dist = c[j] - c[i]
            dist_min = xy[i] / 2 + xy[j] / 2
            sub = dist_min - abs(dist)  # [dx, dy]
            min_axis = np.argmin(sub)
            if dist[min_axis] < 0:
                c[i][min_axis] += sub[min_axis]
            else:
                c[i][min_axis] -= sub[min_axis]


# =====================optimize================================================
def optimize(lr=0.03):
    global c
    for i in range(n):
        for j in range(n):
            if adj[i, j] != 0:
                w, dw, ddw = wdwddw(i, j, 0)
                c[i] -= dw[0] * lr
                solve_collision(i)


def ratio(xy):
    return max(xy[0] / xy[1], xy[1] / xy[0])


# =========================visulize=========================================
def draw_connection():
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i, j] != 0:
                plt.plot(
                    [c[i, 0], c[j, 0]],
                    [c[i, 1], c[j, 1]],
                    "--",
                    lw=adj[i, j] / 3,
                    c="gray",
                )
    plt.scatter(c[:, 0], c[:, 1], c="k", s=60, marker=".")  # s: rectangle


def draw_rectangle(i):
    p = c[i]
    color = np.random.rand(3)
    w, h = xy[i, :2] / 2  # width and height
    x = np.array([p[0] - w, p[0] + w, p[0] + w, p[0] - w])
    y = np.array([p[1] - h, p[1] - h, p[1] + h, p[1] + h])
    plt.fill(x, y, fc="w", hatch="//", color=color, alpha=0.8, lw=2)
    plt.text(
        p[0],
        p[1],
        f"Geo.{i}",
        ha="left",
        va="bottom",
        color=color / 2,
        fontsize=10,
        style="italic",
    )


def init_plot():
    ax.clear()
    # center_plot = np.average(c, axis=0)
    # ax.set_xlim(center_plot[0] - 5, center_plot[0] + 5)
    # ax.set_ylim(center_plot[1] - 5, center_plot[1] + 5)
    # ax.grid(True)
    # ax.axes.get_xaxis().set_visible(False)
    # ax.axes.get_yaxis().set_visible(False)
    # ax.axis("off")
    ax.set_aspect("equal")
    np.random.seed(0)


def ani(f):
    init_plot()

    # for _ in range(5):  # optimize n times
    optimize()

    # Draw rooms
    for i in range(n):
        draw_rectangle(i)
    draw_connection()

    # Show FPS
    global t
    plt.title(f"FPS: {1/(time() - t):.2f}")
    t = time()


# ===========================main==============================================
if __name__ == "__main__":
    # np.random.seed(1)
    n = 6  # number of rooms
    c = np.random.rand(n, 2) * 200  # center of rooms
    xy = np.random.randint(2, 8, (n, 2))  # size of rooms

    # adj = np.ones((n, n))  # graph of rooms
    # adj = np.triu(adj, 1) + np.tril(adj, -1)
    adj = [
        [0, 1, 0, 0, 0, 0],
        [1, 0, 1, 3, 0, 0],
        [0, 1, 0, 2, 0, 0],
        [0, 3, 2, 0, 1, 0],
        [0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 1, 0],
    ]  # graph of rooms with weights
    adj = np.array(adj)

    # update properties
    lr = 1e-1  # learning rate
    stifness = 1  # stifness of springs
    t = 0

    # plot
    fig, ax = plt.subplots()
    a = animation.FuncAnimation(fig, ani, repeat=False, frames=300, interval=0)
    # plt.show()
    a.save("spring_model1.gif", writer="pillow", fps=30)
