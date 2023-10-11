import unittest
import src.PyGameEngine as pge

class MyTestCase(unittest.TestCase):
    def gen_particle(self):
        p = pge.Particle()
        p.setMass(1.0)
        p.setDamping(0.99)
        p.setPosition((0., 0., 0.))
        p.setVelocity((4., 100., 0.))
        p.setAcceleration((0., 0., 0.))

        self.p = p
        self.assertEqual(True, True)

    def test2(self):
        p = pge.Particle()


if __name__ == '__main__':
    unittest.main()
