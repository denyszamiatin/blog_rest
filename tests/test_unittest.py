import unittest


class Test1(unittest.TestCase):
    def setUp(self) -> None:
        print("setUp")
        self.x = 2

    def tearDown(self) -> None:
        print("tearDown")

    def test_1(self):
        self.assertEqual(self.x + 2, 4)
        self.x = 5

    def test_2(self):
        self.assertEqual(self.x + 3, 5)
