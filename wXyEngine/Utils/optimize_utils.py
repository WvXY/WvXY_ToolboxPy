import numpy as np
import torch


def set_points_to_groups(
    points: torch.Tensor | np.ndarray,
    groups: torch.Tensor | np.ndarray,
    weight=None,
    p=2,
    device="cpu",
):
    _numpy = False
    if isinstance(points, np.ndarray):
        points = torch.from_numpy(points).clone().detach()
        _numpy = True
    elif points.device != device:
        points = points.to(device)

    if isinstance(groups, np.ndarray):
        groups = torch.from_numpy(groups).clone().detach()
        _numpy = True
    elif groups.device != device:
        groups = groups.to(device)

    if weight is None:
        weight = torch.ones_like(groups[:, 0], device=device)
    elif isinstance(weight, np.ndarray):
        weight = torch.tensor(weight, device=device)
        _numpy = True

    if p == 1:
        # print("Using manhattan distance")
        dist = torch.sum(
            torch.abs(points[:, None, :] - groups[None, :, :]),
            dim=2,
        )
    elif p == 2:
        # print("Using euclidean distance")
        dist = torch.norm(points[:, None, :] - groups[None, :, :], dim=2)
    elif p >= 16:  # 2^4
        # print("Using chebyshev distance")
        dist = torch.max(
            torch.abs(points[:, None, :] - groups[None, :, :]),
            dim=2,
        )[0]
    else:
        # print(f"Using minkowski distance with p={p}")  # also Lp norm
        dist = torch.sum(
            torch.abs(points[:, None, :] - groups[None, :, :]) ** p,
            dim=2,
        )
    idx = torch.argmin(torch.mul(dist, weight), dim=1)

    if _numpy:
        idx = idx.cpu().numpy()
    return idx


def map_indices(a2b_idx, b2c_idx):
    return b2c_idx[a2b_idx]


def cut_edge(vertices, edges, groups):
    cut_pos = []
    edges_to_delete = []
    for i, (j, k) in enumerate(edges):
        if groups[j] == groups[k]:
            continue
        w1, w2 = vertices[j, -1], vertices[k, -1]
        if w1 == 0 and w2 == 0:
            continue

        edges_to_delete.append(i)
        u, v = vertices[j, :-1], vertices[k, :-1]
        cut_pos.append(u * w1 / (w1 + w2) + v * w2 / (w1 + w2))

    return np.array(cut_pos), np.delete(edges, edges_to_delete, axis=0)
