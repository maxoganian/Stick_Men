import unittest

from stick_men import Platform


class TestPlatform(unittest.TestCase):

	def test_move(self):
		p = Platform(200,200, 500, 10, 10)
		x,y = p.rect.center

		self.assertEqual(200, x)
		p.move()
		x,y = p.rect.center
		self.assertEqual(210, x)


if __name__ == '__main__':
	unittest.main()