import unittest


class TestRendererInterface(unittest.TestCase):
    def test_create_window(self):
        from wXyEngine.Interface.interface import SimpleInterface
        SimpleInterface.run()
        del SimpleInterface

    def test_create_window_interactive(self):
        from wXyEngine.Interface.interface import SimpleInterfaceInteractive
        SimpleInterfaceInteractive.run()

    def test_create_window_with_imgui(self):
        from wXyEngine.Interface.interface import SimpleInterfaceWithImgui
        SimpleInterfaceWithImgui.run()

if __name__ == '__main__':
    unittest.main()
