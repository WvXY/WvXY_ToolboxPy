from copy import deepcopy
import torch


class Movement:
    def __init__(self, a: torch.Tensor, b: torch.Tensor, th):
        self.a = a.clone().detach().requires_grad_(True)
        self.b = b.clone().detach().requires_grad_(True)
        self.th = torch.tensor(th, dtype=torch.float64)

        # self.center = torch.tensor((self.a + self.b) / 2.0)
        # self.ba = self.b - self.a
        # self.theta = torch.atan2(self.ba[1], self.ba[0])
        # self.dir = self.ba / torch.norm(self.ba)
        # self.len = torch.norm(self.ba) + self.th
        self.center, self.ba, self.theta, self.dir, self.len = (
            None,
            None,
            None,
            None,
            None,
        )

    # operations
    def moveTo(self, new_center):
        delta = new_center - self.center  # it creates a shallow copy
        self.moveBy(delta)

    def moveBy(self, delta):
        self.a += delta
        self.b += delta
        self.center += delta

    def rotate(self, angle):
        c, s = torch.cos(angle), torch.sin(angle)
        rot = torch.Tensor([[c, -s], [s, c]])
        self.a = rot @ (self.a - self.center) + self.center
        self.b = rot @ (self.b - self.center) + self.center
        self.ba = rot @ self.ba
        self.dir = rot @ self.dir

    def scaleTo(self, new_th):
        self.th = new_th
        self.len = torch.norm(self.ba) + self.th

    def scaleBy(self, scale):
        self.th = self.th * scale
        self.len = torch.norm(self.ba) + self.th

    def expandBy(self, delta):
        self.th += delta
        self.len = torch.norm(self.ba) + self.th

    def lenTo(self, new_len):
        self.len = new_len
        self.ba = self.dir * (self.len - self.th)
        self.a = self.center - self.ba / 2.0
        self.b = self.center + self.ba / 2.0

    def lenAdd(self, delta):  # add to both sides by delta/2
        self.len += delta
        self.ba = self.dir * (self.len - self.th)
        self.a = self.center - self.ba / 2.0
        self.b = self.center + self.ba / 2.0


def grad(phi: Movement, p, dx=None, dy=None, dw=None, dlen=None, dth=None):
    """calculate gradient of phi at point p"""
    phi_old = deepcopy(phi)
    phi_new = deepcopy(phi)
    if dx:
        h = dx
        phi_new.moveBy([h / 2.0, 0])
        phi_old.moveBy([-h / 2.0, 0])
    elif dy:
        h = dy
        phi_new.moveBy([0, h / 2.0])
        phi_old.moveBy([0, -h / 2.0])
    elif dw:
        h = dw
        phi_new.rotate(h / 2.0)
        phi_old.rotate(-h / 2.0)
    elif dlen:
        h = dlen
        phi_new.lenAdd(h / 2.0)
        phi_old.lenAdd(-h / 2.0)
    elif dth:
        h = dth
        phi_new.expandBy(h / 2.0)
        phi_old.expandBy(-h / 2.0)
    else:
        raise ValueError("dx, dy, dtheta, dlen, dth must be given one of them")
    return (phi_new.sd(p) - phi_old.sd(p)) / h


def gradOne4All(phi: Movement, p, h=1e-3):
    """calculate gradients of phi at p"""
    dx = grad(phi, p, dx=h)
    dy = grad(phi, p, dy=h)
    dw = grad(phi, p, dw=h)
    dlen = grad(phi, p, dlen=h)
    dth = grad(phi, p, dth=h)
    return np.array([dx, dy, dw, dlen, dth])
