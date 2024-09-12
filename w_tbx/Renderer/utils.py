import numpy as np


class Transform2d:  # order matters
    def __init__(self):
        self.transform = np.eye(3, dtype=np.float32)

    def set_transform(self, transform):
        self.transform = transform

    @property
    def mat3(self):
        return self.transform.astype("f4")

    @property
    def inv_mat3(self):
        return np.linalg.inv(self.transform).astype("f4")

    def scale(self, x, y):
        self.transform = np.diag([x, y, 1]) @ self.transform

    def rotate(self, theta):
        self.transform = (
            np.array(
                [
                    [np.cos(theta), -np.sin(theta), 0],
                    [np.sin(theta), np.cos(theta), 0],
                    [0, 0, 1],
                ]
            )
            @ self.transform
        )

    def translate(self, x, y):
        self.transform = (
            np.array([[1, 0, x], [0, 1, y], [0, 0, 1]]) @ self.transform
        )


def generate_grids(n=10):
    grid = np.array([], dtype="f4")
    for i in range(n * 2 + 1):
        grid = np.append(grid, [i - n, -n])
        grid = np.append(grid, [i - n, n])
        grid = np.append(grid, [-n, i - n])
        grid = np.append(grid, [n, i - n])
    return (grid / n).astype("f4")
