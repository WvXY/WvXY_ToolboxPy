from time import time

import numpy as np
from numpy.linalg import norm
import torch


def AABB(game_objs, i, j):
    if i == j:
        return False
    go1, go2 = game_objs[i], game_objs[j]
    if (go1.max < go2.min).any() or (go2.max < go1.min).any():
        return False
    else:
        return True


# def solve_collision(i):
#     n = len(c)
#     for j in range(n):
#         if AABB(i, j):
#             dist = c[j] - c[i]
#             dist_min = xy[i] / 2 + xy[j] / 2
#             sub = dist_min - abs(dist)  # [dx, dy]
#             min_axis = np.argmin(sub)
#             if dist[min_axis] < 0:
#                 c[i][min_axis] += sub[min_axis]
#             else:
#                 c[i][min_axis] -= sub[min_axis]

