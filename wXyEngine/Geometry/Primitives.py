import torch
import torch.nn as nn

torch.set_default_dtype(torch.float32)

from .GameObject import _GameObject


# TODO: optimize this part
class Particle(_GameObject):
    def __init__(self, center, mass=1.0, damping=1.0):
        _GameObject.__init__(self)

        self.center = torch.tensor(center, device=self.device)
        self.r = 0.0  # for relaxation
        self.inverseMass = 1.0 / mass if mass != 0 else 0.0
        self.damping = damping
        self.type = 1


class OrientedBox(_GameObject):
    def __init__(self, a: torch.Tensor, b: torch.Tensor, th):
        _GameObject.__init__(self)

        self.a = nn.Parameter(a).to(self.device)
        self.b = nn.Parameter(b).to(self.device)
        self.th = nn.Parameter(torch.tensor(th, device=self.device))

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


class Circle(_GameObject):
    def __init__(self, radius, center):
        _GameObject.__init__(self)
        self.center = torch.tensor(center, device=self.device)
        self.radius = torch.tensor(radius, device=self.device)


class Rectangle(_GameObject):
    def __init__(self, center, width, height, theta=0.0):
        _GameObject.__init__(self)

        self.center = torch.tensor(center, device=self.device)
        self.width = width
        self.height = height
        self.theta = torch.tensor(theta, device=self.device)


class Line(_GameObject):
    def __init__(self, a, b, r=0.0):
        _GameObject.__init__(self)
        self.a = torch.tensor(a, dtype=torch.float32, device=self.device)
        self.b = torch.tensor(b, dtype=torch.float32, device=self.device)
        self.r = r
        self.direction = self.a - self.b
        self.length = torch.norm(self.direction)


class LineBox(_GameObject):
    def __init__(self, a, b, th):
        _GameObject.__init__(self)
        self.a = torch.tensor(a, dtype=torch.float32, device=self.device)
        self.b = torch.tensor(b, dtype=torch.float32, device=self.device)
        self.th = th

        self.ba, self.len, self.dir, self.center = (None, None, None, None)
        self.updateParams()

    def updateParams(self):
        self.center = self.a / 2.0 + self.b / 2.0
        self.ba = self.b - self.a
        self.len = torch.norm(self.ba)
        self.dir = self.ba / self.len
