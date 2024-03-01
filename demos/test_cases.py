import numpy as np

from wXyEngine.Geometry.obj_process import read_obj


def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x))


def load_obj(obj_file):
    return normalize(np.delete(read_obj(obj_file)[0], 1, 1))


class Cases:
    boundary_vtx = {
        0: np.array(
            [
                [0, 0],
                [1, 0],
                [1, 0.8],
                [0.6, 0.6],
                [0.6, 1.2],
                [0, 1],
            ],
            dtype=np.float32,
        ),
        1: np.array(
            [
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1],
            ],
            dtype=np.float32,
        ),
        2: np.array(
            [
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1],
                [0.5, 0.5],
            ],
            dtype=np.float32,
        ),
        3: load_obj("data/test_case3.obj"),
        4: load_obj("data/test_case4.obj"),
        5: load_obj("data/test_case5.obj"),
    }
