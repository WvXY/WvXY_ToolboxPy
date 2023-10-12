import unittest
from src import PyGameEngine as pge

class MyTestCase(unittest.TestCase):
    p = pge.Particle()

    def test_gen_particle(self):
        self.p.setMass(1.0)
        self.p.setDamping(0.99)
        self.p.setPosition((0., 0., 0.))
        self.p.setVelocity((4., 100., 0.))
        self.p.setAcceleration((0., 0., 0.))

        self.assertEqual(self.p.mass, 1.0)

    def test_integrate(self):
        self.p.integrate(0.01)


if __name__ == '__main__':
    unittest.main()
