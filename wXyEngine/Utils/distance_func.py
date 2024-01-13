import numpy as np
import torch


def manhattan_distance(a: np.ndarray | torch.Tensor, b: np.ndarray | torch.Tensor):
    if isinstance(a, torch.Tensor):
        return torch.sum(torch.abs(a - b), dim=-1)
    else:
        return np.sum(np.abs(a - b), axis=-1)


def euclidean_distance(a: np.ndarray | torch.Tensor, b: np.ndarray | torch.Tensor):
    if isinstance(a, torch.Tensor):
        return torch.norm(a - b, dim=-1)
    else:
        return np.linalg.norm(a - b, axis=-1)


def chebyshev_distance(a: np.ndarray | torch.Tensor, b: np.ndarray | torch.Tensor):
    if isinstance(a, torch.Tensor):
        return torch.max(torch.abs(a - b), dim=-1)[0]
    else:
        return np.max(np.abs(a - b), axis=-1)
