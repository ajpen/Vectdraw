import unittest

from vectdraw.draw.colour import Colour


class TestColour(unittest.TestCase):

   def test_colour_constructor(self):

      with self.assertRaises(TypeError):
         Colour('233 333 222 1')

      with self.assertRaises(ValueError):
         Colour((1000, 22, 22, 10000))

   def test_equality(self):
      self.assertEqual(Colour(), Colour())