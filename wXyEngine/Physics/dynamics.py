import torch


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
            ddw[d, e] = stifness * uij * uij.T * (-1) ** (d + e) + stifness * C * (
                    np.eye(dim) - uij * uij.T
            ) * (-1) ** (d + e)
    return w, dw, ddw