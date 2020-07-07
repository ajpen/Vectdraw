import unittest

from io import StringIO

from vectdraw.draw.board import Board
from vectdraw.draw.pen import Pen
from vectdraw.draw.colour import Colour
from vectdraw.draw.plane import Point


class TestBoardOutput(unittest.TestCase):

   def setUp(self):
      self.stream = StringIO()
      self.board = Board(Pen(), outputStream=self.stream)

   def test_clear(self):
      self.board.clear()

      self.assertEqual(self.stream.getvalue(), "CLR;\n")

   def test_pen(self):

      self.board.ChangePenPosition(0)

      self.assertEqual(self.board.pen.IsPenDown(), False)

      self.board.ChangePenPosition(1)

      self.assertEqual(self.board.pen.IsPenDown(), True)
      self.assertEqual(self.stream.getvalue(), "PEN UP;\nPEN DOWN;\n")

   def test_colour(self):
      self.board.SetColour(1, 2, 3, 4)

      self.assertEqual(self.board.pen.colour(), Colour((1, 2, 3, 4)))
      self.assertEqual(self.stream.getvalue(), "CO 1 2 3 4;\n")

   def test_move_pen_up(self):
      points = [Point(10, 10), Point(5, -5)]
      self.board.MovePen(points)

      self.assertEqual(
         self.board.currentPenLocation, Point(15, 5),
         msg="{} != {}".format(self.board.currentPenLocation, Point(15, 5)))

      self.assertEqual(self.stream.getvalue(), "MV (15, 5);\n")

   def test_move_pen_down(self):
      points = [Point(10, 10), Point(5, -5)]

      self.board.pen.down()
      self.board.MovePen(points)
      self.assertEqual(self.board.currentPenLocation, Point(15, 5),
                       msg="{} != {}".format(self.board.currentPenLocation,
                                             Point(15, 5)))

      self.assertEqual(self.stream.getvalue(), "MV (10, 10) (15, 5);\n")

   def test_move_pen_down_out_of_bounds(self):
      points = [Point(5000, 5000), Point(5000, 0),
                Point(-5000, 0), Point(-200, 0)]

      self.board.pen.down()
      self.board.MovePen(points)

      self.assertEqual(
         self.board.currentPenLocation, Point(4800, 5000),
         msg="{} != {}"
         .format(self.board.currentPenLocation, Point(4800, 5000)))

      self.assertEqual(self.stream.getvalue(),
                       "MV (5000, 5000) (8191, 5000);"
                       "\nPEN UP;\nMV (8191, 5000);"
                       "\nPEN DOWN;\nMV (5000, 5000) (4800, 5000);\n")


   def test_move_pen_up_out_of_bounds(self):
      points = [Point(10, 10), Point(50000, 0)]
      self.board.MovePen(points)

      self.assertEqual(
         self.board.currentPenLocation, Point(50010, 10),
         msg="{} != {}"
         .format(self.board.currentPenLocation, Point(50010, 10)))

      self.assertEqual(self.stream.getvalue(), "MV (8191, 10);\n")