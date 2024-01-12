import unittest


class MyTestCase(unittest.TestCase):
    def test_import(self):
        import wXyEngine as xe
        import wXyEngine.Geometry as Geometry
        import wXyEngine.Renderer as Renderer
        import wXyEngine.Physics as Physics
        import wXyEngine.Utils as Utils

        self.assertEqual(Geometry.__name__, "wXyEngine.Geometry")
        self.assertEqual(Renderer.__name__, "wXyEngine.Renderer")
        self.assertEqual(Physics.__name__, "wXyEngine.Physics")
        self.assertEqual(Utils.__name__, "wXyEngine.Utils")

    def test_create_geometry(self):
        import wXyEngine.Geometry as Geometry

        P = Geometry.Primitives.Particle([0, 0])
        for c in P.center:
            self.assertEqual(c, 0)

    def test_guid_system(self):
        import wXyEngine.Geometry as Geometry

        game_objects = []
        for i in range(10):
            P = Geometry.Primitives.Particle([0, 0])
            R = Geometry.Primitives.Rectangle([1, 1], 1, 1)
            game_objects.append(P)
            game_objects.append(R)

        for i in range(10 * 2):
            self.assertEquals(i, game_objects[i].guid)

        
if __name__ == '__main__':
    unittest.main()
