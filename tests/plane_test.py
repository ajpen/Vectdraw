import unittest

from decimal import Decimal as D

from vectdraw.draw.plane import Point
from vectdraw.draw.plane import Axis
from vectdraw.draw.plane import VirtualPlane

class TestPoint(unittest.TestCase):

   def test_default(self):
      self.assertEqual(Point(), Point(0, 0))

   def test_equality(self):
      self.assertEqual(Point(2, 3), Point(2, 3))

   def test_add(self):
      self.assertEqual(Point(2, 3) + Point(2, 3), Point(4, 6))

   def test_add_negative(self):
      self.assertEqual(Point(2, 3) + Point(2, -3), Point(4, 0))



class TestAxis(unittest.TestCase):

   def test_constructor(self):
      with self.assertRaises(ValueError):
         Axis('1, 2')

      with self.assertRaises(ValueError):
         Axis(('1', 2))

      with self.assertRaises(ValueError):
         Axis((1,))

   def test_default(self):
      self.assertEqual(Axis(), Axis((-8192, 8191)))

   def test_equality(self):
      self.assertEqual(Axis((321, 321)), Axis((321, 321)))
      self.assertNotEqual(Axis((321, 321)), Axis((-8192, 8191)))


class TestVirtualPlane(unittest.TestCase):

   def setUp(self):
      self.plane_10x10 = VirtualPlane(Axis((-10, 10)), Axis((-10, 10)))

   def compare_point_distance_tuples(self, expected, actual):
      # tests point first
      self.assertTrue(
         actual[0] == expected[0],
         msg="expected {}, got {}".format(expected[0], actual[0]))

      # test distance
      self.assertAlmostEqual(actual[1], expected[1], delta=0.1)

   def check_point_distance_list_lengths(self, expected, actual):
      self.assertTrue(
         len(expected) == len(actual),
         msg="expected and actual have different lengths {} != {}"
            .format(expected, actual))

   def test_border_crossed(self):
      self.assertListEqual(
         [self.plane_10x10.kOutXLowerBounds],
         self.plane_10x10.BoundariesCrossedByLine(Point(1, 3), Point(-15, 0))
      )
      self.assertListEqual(
         [self.plane_10x10.kOutXLowerBounds],
         self.plane_10x10.BoundariesCrossedByLine(Point(-12, 3), Point(5, 0))
      )
      self.assertListEqual(
         [self.plane_10x10.kOutXUpperBounds],
         self.plane_10x10.BoundariesCrossedByLine(Point(1, 3), Point(15, 0))
      )

      self.assertListEqual(
         [self.plane_10x10.kOutXUpperBounds],
         self.plane_10x10.BoundariesCrossedByLine(Point(51, 3), Point(5, 0))
      )

      self.assertListEqual(
         [self.plane_10x10.kOutYLowerBounds],
         self.plane_10x10.BoundariesCrossedByLine(Point(1, 3), Point(0, -15))
      )

      self.assertListEqual(
         [self.plane_10x10.kOutYLowerBounds],
         self.plane_10x10.BoundariesCrossedByLine(Point(1, -13), Point(0, 5))
      )

      self.assertListEqual(
         [self.plane_10x10.kOutYUpperBounds],
         self.plane_10x10.BoundariesCrossedByLine(Point(1, 3), Point(0, 15))
      )

      self.assertListEqual(
         [self.plane_10x10.kOutYUpperBounds],
         self.plane_10x10.BoundariesCrossedByLine(Point(1, 13), Point(0, 5))
      )

      self.assertListEqual(
         [self.plane_10x10.kOutXLowerBounds, self.plane_10x10.kOutXUpperBounds],
         self.plane_10x10.BoundariesCrossedByLine(Point(-15, 3), Point(15, 1))
      )

      self.assertListEqual(
         [self.plane_10x10.kOutYLowerBounds, self.plane_10x10.kOutYUpperBounds],
         self.plane_10x10.BoundariesCrossedByLine(Point(1, -13), Point(1, 13))
      )

      self.assertListEqual(
         [self.plane_10x10.kOutXLowerBounds,
          self.plane_10x10.kOutYUpperBounds],
         self.plane_10x10.BoundariesCrossedByLine(Point(-13, 0), Point(1, 13))
      )

   def test_single_boundary_intercept(self):
      start = Point(4, 6)
      end = Point(8, 12)
      expected = [(Point(7, 10), D(5))]
      actual = self.plane_10x10.GetBoundaryIntercepts(start, end)

      self.check_point_distance_list_lengths(expected, actual)

      for index, pair in enumerate(expected):
         self.compare_point_distance_tuples(expected[index], actual[index])

   def test_multiple_boundary_intercepts(self):
      start = Point(-14, 6)
      end = Point(12, 8)
      expected = [(Point(-10, 6), D(4)), (Point(10, 8), D(24.0832))]
      actual =  self.plane_10x10.GetBoundaryIntercepts(start, end)

      self.check_point_distance_list_lengths(expected, actual)

      for index, pair in enumerate(expected):
         self.compare_point_distance_tuples(expected[index], actual[index])

   def test_boundary_intercepts_order(self):
      start = Point(12, 8)
      end = Point(-14, 6)
      expected = [(Point(10, 8), D(2)), (Point(-10, 6), D(22.0907))]
      actual =  self.plane_10x10.GetBoundaryIntercepts(start, end)

      self.check_point_distance_list_lengths(expected, actual)

      for index, pair in enumerate(expected):
         self.compare_point_distance_tuples(expected[index], actual[index])
