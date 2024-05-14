import unittest
from PyMRT.Geometry import Particle, OrientedBox, Circle, Rectangle, Line
from PyMRT.Geometry import GameObjectManager
import torch


class TestPytorchGeometry(unittest.TestCase):
    def test_device_is_cuda(self):
        self.assertEqual(Particle.device, torch.device("cuda:0"))

    def test_cuda(self):
        P = Particle([0, 0])
        self.assertEqual(P.pos.device, torch.device("cuda:0"))

    def test_cuda2(self):
        a, b = torch.tensor([0.0, 0.0]), torch.tensor([1.0, 1.0])
        OB = OrientedBox(a, b, 0.0)
        self.assertEqual(OB.a.device, torch.device("cuda:0"))
        self.assertEqual(OB.theta.device, torch.device("cuda:0"))


if __name__ == "__main__":
    unittest.main()
