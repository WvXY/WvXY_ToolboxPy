import unittest
from src import PyGameEngine as pge

class MyTestCase(unittest.TestCase):
    def test_gen_particle(self):
        p = pge.Particle()
        p.setMass(1.0)
        p.setDamping(0.99)
        p.setPosition((0., 0., 0.))
        p.setVelocity((4., 100., 0.))
        p.setAcceleration((0., 0., 0.))

        self.p = p
        self.assertEqual(self.p.mass, 1.0)

    def test_integrate(self):
        self.p.integrate(0.01)


if __name__ == '__main__':
    unittest.main()
