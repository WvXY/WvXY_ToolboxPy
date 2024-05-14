import unittest
import math
import random


class MyTestCase(unittest.TestCase):
    def test_import(self):
        import wXyEngine as xe
        import wXyEngine.Geometry as Geometry
        import wXyEngine.Renderer as Renderer
        import wXyEngine.Physics as Physics
        import wXyEngine.Utils as Utils

        self.assertEqual(Geometry.__name__, "mrpyet.Geometry")
        self.assertEqual(Renderer.__name__, "mrpyet.Renderer")
        self.assertEqual(Physics.__name__, "mrpyet.Physics")
        self.assertEqual(Utils.__name__, "mrpyet.Utils")

    def test_create_geometry(self):
        import wXyEngine.Geometry as Geometry

        P = Geometry.Primitives.Particle([0, 0])
        for c in P.pos:
            self.assertEqual(c, 0)

    def test_game_object_manager(self):
        import wXyEngine.Geometry as Geometry

        game_objects = Geometry.GameObjectManager()
        for i in range(10):
            P = Geometry.Primitives.Particle([0, 0])
            R = Geometry.Primitives.Rectangle([1, 1], 1, 1)
            game_objects.add(P)
            game_objects.add(R)

        for i in range(10 * 2):
            self.assertEqual(i, game_objects.get(i).guid)

        del game_objects

    def test_game_object_manager_random(self):
        import wXyEngine.Geometry as Geometry

        game_objects = Geometry.GameObjectManager()
        # game_objects.reset_global_guid()
        for i in range(100):
            rnd = random.random()
            if rnd < 0.5:
                P = Geometry.Primitives.Particle([0, 0])
                game_objects.add(P)
            elif rnd < 0.8:
                R = Geometry.Primitives.Rectangle([1, 1], 1, 1)
                game_objects.add(R)
            else:
                C = Geometry.Primitives.Circle(1, [0, 0])
                game_objects.add(C)

        for i in range(100):
            self.assertEqual(i + 20, game_objects.get(i + 20).guid)

        del game_objects


if __name__ == '__main__':
    unittest.main()
