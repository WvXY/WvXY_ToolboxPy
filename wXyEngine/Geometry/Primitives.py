import torch
import torch.nn as nn

torch.set_default_dtype(torch.float64)


class GameObject:
    GUID = -1

    def __init__(self):
        self.guid = GameObject.GUID
        GameObject.GUID += 1

    def update(self, dt):
        pass

    def draw(self):
        pass


# TODO: optimize this part
class Particle(GameObject):
    def __init__(self, center, mass=1.0, damping=1.0):
        GameObject.__init__(self)

        self.center = torch.tensor(center)
        self.r = 0.0  # for relaxation
        self.inverseMass = 1.0 / mass if mass != 0 else 0.0
        self.damping = damping
        self.type = 1


class OrientedBox(GameObject):
    def __init__(self, a: torch.Tensor, b: torch.Tensor, th):
        GameObject.__init__(self)
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


class Circle(GameObject):
    def __init__(self, radius, center):
        GameObject.__init__(self)
        self.center = center
        self.radius = radius


class Rectangle(GameObject):
    def __init__(self, center, width, height, theta=0.0):
        GameObject.__init__(self)

        self.center = torch.tensor(center, dtype=torch.float32)
        self.width = width
        self.height = height
        self.theta = torch.tensor(theta)


class Line(GameObject):
    def __init__(self, a, b, r=0.0):
        GameObject.__init__(self)
        self.a = torch.tensor(a, dtype=torch.float32)
        self.b = torch.tensor(b, dtype=torch.float32)
        self.r = r
        self.direction = self.a - self.b
        self.length = torch.norm(self.direction)


class LineBox(GameObject):
    def __init__(self, a, b, th):
        GameObject.__init__(self)
        self.a = torch.tensor(a, dtype=torch.float32)
        self.b = torch.tensor(b, dtype=torch.float32)
        self.th = th

        self.ba, self.len, self.dir, self.center = (None, None, None, None)
        self.updateParams()

    def updateParams(self):
        self.center = self.a / 2.0 + self.b / 2.0
        self.ba = self.b - self.a
        self.len = torch.norm(self.ba)
        self.dir = self.ba / self.len
