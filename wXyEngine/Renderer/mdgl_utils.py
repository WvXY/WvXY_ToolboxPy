import numpy as np


class Transform2d:
    def __init__(self, scale=[1.0, 1.0], offset=[0., 0.], rotation=0.):
        self.transform = np.eye(3, dtype=np.float32)
        self.scale(*scale)
        self.rotate(rotation)
        self.offset(*offset)

    def set_transform(self, transform):
        self.transform = transform

    @property
    def mat3(self):
        return self.transform.flatten().astype("f4")

    def scale(self, x, y):
        self.transform = np.matmul(self.transform, np.diag([x, y, 1]))

    def rotate(self, theta):
        self.transform = np.matmul(self.transform, np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ]))

    def offset(self, x, y):
        self.transform[2, 0] += x
        self.transform[2, 1] += y


class Transform3d:
    pass
