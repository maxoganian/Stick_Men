import unittest

from stick_men import Player


class TestPlayer(unittest.TestCase):

	def test_grav(self):
		p = Player(200,200)
		x,y = p.rect.center
		self.assertEqual(200, x)


if __name__ == '__main__':
	unittest.main()