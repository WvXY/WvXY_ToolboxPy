import numpy as np
import torch


def manhattan_distance(
    a: np.ndarray | torch.Tensor, b: np.ndarray | torch.Tensor
):
    if isinstance(a, torch.Tensor):
        return torch.sum(torch.abs(a - b), dim=-1)
    else:
        return np.sum(np.abs(a - b), axis=-1)


def euclidean_distance(
    a: np.ndarray | torch.Tensor, b: np.ndarray | torch.Tensor
):
    if isinstance(a, torch.Tensor):
        return torch.norm(a - b, dim=-1)
    else:
        return np.linalg.norm(a - b, axis=-1)


def chebyshev_distance(
    a: np.ndarray | torch.Tensor, b: np.ndarray | torch.Tensor
):
    if isinstance(a, torch.Tensor):
        return torch.max(torch.abs(a - b), dim=-1)[0]
    else:
        return np.max(np.abs(a - b), axis=-1)


def minkowski_distance(
    a: np.ndarray | torch.Tensor, b: np.ndarray | torch.Tensor, p: int
):
    if p == 1:
        return manhattan_distance(a, b)
    elif p == 2:
        return euclidean_distance(a, b)
    elif p >= 16:  # 2^4 (approximation)
        return chebyshev_distance(a, b)

    # other cases
    if isinstance(a, torch.Tensor):
        return torch.sum(torch.abs(a - b) ** p, dim=-1)
    else:
        return np.sum(np.abs(a - b) ** p, axis=-1)
