import unittest


class MyTestCase(unittest.TestCase):
    def test_import(self):
        import wxy_engine as x
        # from external.wXyEngine.wXyEngine.main import test
        print(dir(x))
        # x.main.test()
        
        
if __name__ == '__main__':
    unittest.main()
