import unittest
import matplotlib.pyplot as plt


# collision test
class MyTestCase(unittest.TestCase):
    def test_AABB(self):
        from wXyEngine.Physics.collision import AABB
        from wXyEngine.Geometry import Circle, Rectangle, Line, LineBox, Particle
        from wXyEngine.Geometry.GameObject import GameObjectManager

        game_objs = GameObjectManager()
        game_objs.add(Circle(1, [0, 0]))
        game_objs.add(Circle(1, [2, 0]))
        game_objs.add(Rectangle([0, 0], 2, 2))
        game_objs.add(Rectangle([0, 0], 2, 2))
        game_objs.add(Line([0, 0], [1, 1]))
        game_objs.add(Line([0, 0], [1, 1]))
        game_objs.add(Particle([1,2]))

        for obj in game_objs.game_objects:
            print(obj.min, obj.max)

        self.assertEqual(AABB(game_objs.game_objects, 0, 1), True)


if __name__ == '__main__':
    unittest.main()
