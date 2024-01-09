from copy import deepcopy, copy
import torch
import torch.nn as nn
from .operations import *
from .dynamics import Movement
from .grid import Grid

torch.set_default_dtype(torch.float64)


# =============================================================================
# primitive shapes
class SdOrientedBox(object):
    def __init__(self, a: torch.Tensor, b: torch.Tensor, th):
        # super().__init__(a, b, th)

        self.a = nn.Parameter(a)
        self.b = nn.Parameter(b)
        self.th = nn.Parameter(torch.tensor(th, dtype=torch.float64))

        self.center = nn.Parameter((self.a + self.b) / 2.0)
        self.ba = self.b - self.a
        self.theta = torch.atan2(self.ba[1], self.ba[0])
        self.dir = self.ba / torch.norm(self.ba)
        self.len = torch.norm(self.ba)  # + self.th
        # end will be at a/b if "th" is removed
        # (other functions need to be changed)

        # set parameters
        self.len = nn.Parameter(self.len)
        self.th = nn.Parameter(self.th)
        self.theta = nn.Parameter(self.theta)

    def update_other_parameters(self):
        """update parameters based on center, len, th, theta"""
        self.dir = torch.tensor([torch.cos(self.theta), torch.sin(self.theta)])
        self.ba = self.dir * (self.len - self.th)
        self.a = self.center - self.ba / 2.0
        self.b = self.center + self.ba / 2.0

    def update_parameters(self):
        """update parameters based on a, b, th"""
        self.center = torch.tensor((self.a + self.b) / 2.0)
        self.ba = self.b - self.a
        self.theta = torch.atan2(self.ba[1], self.ba[0])
        self.dir = self.ba / torch.norm(self.ba)
        self.len = torch.norm(self.ba) + self.th

    def sd(self, p: torch.Tensor) -> torch.Tensor:
        # self.zero_grad()
        # self.update_other_parameters()
        # # self.update_parameters()    # under construction
        self.ba = self.b - self.a
        self.len = torch.norm(self.ba)  # + self.th
        self.dir = self.ba / self.len
        self.center = (self.a + self.b) / 2.0

        d = self.dir
        q = p.reshape(-1, 2) - self.center
        zeros = torch.zeros_like(q)
        q = torch.tensor([[d[0], d[1]], [-d[1], d[0]]]) @ q.T

        # len th gradient cannot be computed, being reset every time
        # q = torch.abs(q.T) - torch.Tensor([[self.len / 2.0, self.th / 2.0]])

        temp0 = torch.abs(q[0]) - self.len / 2.0
        temp1 = torch.abs(q[1]) - self.th / 2.0
        q = torch.stack((temp0, temp1), dim=0)
        outside = torch.norm(torch.fmax(q.T, zeros), dim=1)  # outside
        inside = torch.fmin(torch.max(q.T, 1)[0], zeros[:, 0])  # inside
        # print(f"outside: {outside.shape}, inside: {inside.shape}")
        return outside + inside

    # properties
    @property
    def area(self):
        return self.len * self.th

    def parameters(self):
        return [self.center, self.len, self.th, self.theta]

    def zero_grad(self):
        self.center.grad = None
        self.len.grad = None
        self.th.grad = None


class SdParticle:
    def __init__(self, center):
        self.center = torch.tensor(center)
        self.r = 0.0

    def sd(self, p, r=None) -> float:
        self.r = self.r if r is None else r
        return torch.norm(p - self.center, dim=-1) - self.r


class SdCircle(SdParticle):
    def __init__(self, radius, center):
        super().__init__(center)
        self.radius = radius

    def sd(self, p, r=None) -> float:
        self.r = self.r if r is None else r
        return torch.norm(p - self.center, dim=-1) - self.radius - r


class SdSquare:
    def __init__(self, width, height, center=[0.0, 0.0], theta=0.0):
        # super().__init__()
        self.center = torch.tensor(center, dtype=torch.float32)
        self.width = width
        self.height = height
        self.theta = torch.tensor(theta)

    def __repr__(self) -> str:
        return (
            f"center: {self.center}, " f"width: {self.width}, " f"height: {self.height}"
        )

    def correct_position(self, point):
        R = torch.tensor(
            [
                [torch.cos(self.theta), -torch.sin(self.theta)],
                [torch.sin(self.theta), torch.cos(self.theta)],
            ]
        )
        point_rotated = (point - self.center) @ R.T  # not sure if it is correct
        return point_rotated

    def sd(self, point, r=0.0) -> float:
        point = torch.tensor(point, dtype=torch.float32)
        point_corrected = self.correct_position(point)
        dx = torch.abs(point_corrected[0]) - self.width / 2.0
        dy = torch.abs(point_corrected[1]) - self.height / 2.0
        return (
            torch.minimum(torch.maximum(dx, dy), torch.tensor(0))
            + torch.norm(
                torch.stack(
                    [torch.fmax(dx, torch.tensor(0)), torch.fmax(dy, torch.tensor(0))]
                ),
                dim=0,
            )
            - r
        )  # inside + outside


class SdLine(Grid):
    def __init__(self, a, b, r=0.0):
        super().__init__()
        self.a = torch.tensor(a, dtype=torch.float32)
        self.b = torch.tensor(b, dtype=torch.float32)
        self.r = r
        self.direction = self.a - self.b
        self.length = torch.norm(self.direction)

    def sd(self, p) -> float:
        pa, ba = p - self.a, self.b - self.a
        h = torch.clip((pa @ ba) / (ba @ ba), 0, 1)
        return torch.norm(pa - torch.outer(h, ba), dim=-1) - self.r

    def getSD4Grid(self):
        return self.calculate_grid_distance(self.sd)


# Chebyshev distance
class SdLineBox:
    def __init__(self, a, b, th):
        self.a = torch.tensor(a, dtype=torch.float32)
        self.b = torch.tensor(b, dtype=torch.float32)
        self.th = th

        self.grid = Grid()
        self.ba, self.len, self.dir, self.center = (None, None, None, None)
        self.updateParams()

    def updateParams(self):
        self.center = self.a / 2.0 + self.b / 2.0
        self.ba = self.b - self.a
        self.len = torch.norm(self.ba)
        self.dir = self.ba / self.len

    def sd(self, p):
        if p.shape == (1, 2):
            p = p.reshape(
                2,
            )

        self.updateParams()
        pa = p - self.a

        if 0 <= self.ba.dot(pa) / self.len <= 1:  # (a,b)
            return torch.norm(torch.cross(self.ba, pa)) / self.len - self.th / 2.0
        else:
            ac = torch.abs(pa.dot(self.ba)) / self.len
            v = torch.tensor([self.ba[1], -self.ba[0]])
            pc = torch.abs(pa.dot(v)) / self.len
            return (
                max(ac, pc) - self.th / 2.0
                if self.ba.dot(pa) < 0
                else max(ac - self.len, pc) - self.th / 2.0
            )

    def sds(self, p):
        # Assuming p is an array of points
        pa = p - self.a  # vector from a to each point
        pb = p - self.b  # vector from b to each point

        # Dot product with unit direction vector
        # (can be precomputed in updateParams)
        h = torch.clip(torch.dot(pa, self.dir), 0, self.len)

        # Distance calculation
        dist = torch.norm(pa - self.dir * h[:, torch.newaxis], dim=1) - self.th / 2.0
        return dist

    def grad(self, p):
        if p.shape == (1, 2):
            p = p.reshape(
                2,
            )
        self.ba = self.b - self.a
        self.len = torch.norm(self.ba)
        pa = p - self.a

        if 0 <= self.ba.dot(pa) / self.len <= 1:  # debug
            return torch.cross(self.ba, pa) / self.len
        else:
            ac = torch.abs(pa.dot(self.ba)) / self.len
            v = torch.tensor([self.ba[1], -self.ba[0]])
            pc = torch.abs(pa.dot(v)) / self.len
            return torch.tensor([ac, pc])

    def getArea(self):
        return (self.len + self.th) * self.th

    def __setAB(self):
        if self.a[0] > self.b[0]:
            self.a, self.b = self.b, self.a

    def changeLength(self, new_length, fixed_point="a"):
        if fixed_point == "a":
            self.b = self.a + self.ba * new_length / self.len
        elif fixed_point == "b":
            self.a = self.b - self.ba * new_length / self.len
        else:  # center
            self.a = self.center - self.ba * new_length / self.len / 2.0
            self.b = self.center + self.ba * new_length / self.len / 2.0
        self.len = new_length

    def rotate(self, theta):
        """Rotate theta around center"""
        R = torch.tensor(
            [
                [torch.cos(theta), -torch.sin(theta)],
                [torch.sin(theta), torch.cos(theta)],
            ]
        )
        self.a = R @ (self.a - self.center) + self.center
        self.b = R @ (self.b - self.center) + self.center

    def move(self, d):
        self.a += d
        self.b += d
        self.center += self.d

    def getSD4Grid(self):
        return self.grid.calculate_grid_distance(self.sds)
