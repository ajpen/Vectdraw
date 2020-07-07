import unittest
from vectdraw.draw.pen import Pen
from vectdraw.draw.colour import Colour


class TestPen(unittest.TestCase):

   def setUp(self):
      self.pen = Pen()

   def test_change_colour(self):

      with self.assertRaises(TypeError):
         self.pen.ChangeColour((1, 2, 3, 4))

   def test_pen_movement(self):
      self.assertEqual(self.pen.IsPenDown(), False)
      self.pen.down()
      self.assertEqual(self.pen.IsPenDown(), True)
      self.pen.lift()
      self.assertEqual(self.pen.IsPenDown(), False)

   def test_reset(self):
      self.pen.ChangeColour(Colour((233, 233, 11, 244)))
      self.assertEqual(self.pen.colour(), Colour((233, 233, 11, 244)))
      self.pen.reset()
      self.assertEqual(self.pen.colour(), Colour())
      self.assertEqual(self.pen.IsPenDown(), False)