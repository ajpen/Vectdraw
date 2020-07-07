

"""
Classes for managing the vector drawing space and positioning
"""

import decimal

from decimal import getcontext as D_cxt
from decimal import Decimal as D


class Point:
   x = 0
   y = 0

   def __init__(self, x=None, y=None):
      if x:
         self.x = x
      if y:
         self.y = y

   def __str__(self):
      return str((self.x, self.y))

   def __add__(self, other):
      return Point(
         self.x + other.x,
         self.y + other.y
      )

   def __eq__(self, other):
      if isinstance(other, self.__class__):
         return (self.x == other.x and
                 self.y == other.y)


class Axis(object):

   # Default Domain
   upperBound = 8191
   lowerBound = -8192

   def __init__(self, domain=None):
      """
      :param domain: integer tuple of size 2 representing the domain of an axis
      """
      if domain:
         self.setDomain(domain)

   def setDomain(self, new_domain):
      """
      updates upper and lower bound using "new_domain" if "new_domain" is valid
      :param new_domain: tuple of ints of size 2

      raises ValueError if new_domain does not confirm to the expected format
      """
      if (new_domain and isinstance(new_domain, tuple) and len(new_domain) == 2
            and self._VerifyTupleValueType(new_domain, int)):

         self.lowerBound, self.upperBound = new_domain

      else:
         raise ValueError("Bad argument. Expected tuple of two ints (int, int)"
                          "received {}".format(str(new_domain)))

   @staticmethod
   def _VerifyTupleValueType(tup, expectedType):
      """
      checks that tup values are instances of expected_type
      :param tup: tuple of values to be tested
      :param expectedType: type tested for
      :return: true if tuple values all match expected type, false otherwise
      """
      for val in tup:
         if not isinstance(val, expectedType):
            return False

      return True

   def __eq__(self, other):
      if isinstance(other, self.__class__):
         return (self.lowerBound == other.lowerBound and
                 self.upperBound == other.upperBound)
      else:
         raise NotImplemented

   def __str__(self):
      return str((self.lowerBound, self.upperBound))


class VirtualPlane(object):

   # Out of bounds constants for identifying the breached boundary
   kOutXLowerBounds = 20
   kOutXUpperBounds = 21
   kOutYLowerBounds = 22
   kOutYUpperBounds = 23

   XAxis = Axis()
   YAxis = Axis()


   def __init__(self, xAxis=None, yAxis=None):
      if xAxis:
         if isinstance(xAxis, Axis):
            self.XAxis = xAxis
         else:
            raise TypeError("Expected type Axis, received {}"
                            .format(type(xAxis)))
      if yAxis:
         if isinstance(yAxis, Axis):
            self.YAxis = yAxis
         else:
            raise TypeError("Expected type Axis, received {}"
                            .format(type(yAxis)))

   @staticmethod
   def _validatePoint(point):
      if not isinstance(point, Point):
         raise TypeError("Expected Point, received {}".format(type(point)))


   def BoundariesCrossedByLine(self, lineStart, lineEnd):
      """
      returns a list of boundaries crossed by the line starting at lineStart and
      ending at lineEnd.
      (boundary crossed first is added first to list)
      :param lineStart: Point where line starts
      :param lineEnd: Point where line ends
      :return: list of boundary constants representing the boundary crossed

            example:
      if lineStart=Point(x=1000, y=300), lineEnd=Point(x=300, y=300),
      XAxis=(-500, 500), YAxis=(-500, 500),
      boundary_crossed(point) will return kOutXUpperBounds
      """
      self._validatePoint(lineStart)
      self._validatePoint(lineEnd)

      crossedBoundaries = list()

      if self.__NumberInRange(
            lineStart.x, lineEnd.x, self.XAxis.lowerBound):
         crossedBoundaries.append(self.kOutXLowerBounds)

      if self.__NumberInRange(
            lineStart.x, lineEnd.x, self.XAxis.upperBound):
         crossedBoundaries.append(self.kOutXUpperBounds)

      if self.__NumberInRange(
            lineStart.y, lineEnd.y, self.YAxis.lowerBound):
         crossedBoundaries.append(self.kOutYLowerBounds)

      if self.__NumberInRange(
            lineStart.y, lineEnd.y, self.YAxis.upperBound):
         crossedBoundaries.append(self.kOutYUpperBounds)

      return crossedBoundaries

   def GetBoundaryIntercepts(self, lineStart, lineEnd):
      """
      Returns the Point(s) where the line that connects lineStart and lineEnd
      crosses the plane border, else None

      :param lineStart: Point representing the start of the line
      :param lineEnd: Point representing the end of the line
      :return: list of tuples of point-distance pairs where the line crosses the
      boundary in chronological order
      """
      crossedBoundaries = self.BoundariesCrossedByLine(lineStart, lineEnd)
      pointsCrossedWithDistance = list()

      for boundary in crossedBoundaries:
         partialIntercept = self.__GetBoundaryCoordinates(boundary)

         boundaryIntercept = self.__GetBoundaryIntercept(
            lineStart, lineEnd, partialIntercept)

         distanceFromLine = self.__CalculateDistanceFromPoints(
            lineStart, boundaryIntercept)

         pointsCrossedWithDistance.append(
            (boundaryIntercept, distanceFromLine))

      return sorted(pointsCrossedWithDistance, key=lambda x: x[1])

   def __GetBoundaryIntercept(self, lineStart, lineEnd, borderIntercept):
      """
      Returns the Point where the line that connects intercept and lineEnd
      crosses the plane border

      :param borderIntercept: intercept with missing x or y value
      :param lineStart: Point representing the start of the line
      :param lineEnd: Point representing the end of the line
      :return: tuple of Points where the line crosses the boundary
      """
      gradient = self.__CalculateGradientFromPoints(lineStart, lineEnd)

      if borderIntercept.y is None:
         borderIntercept.y = self.__LineEquationUnknownY(
            lineEnd, borderIntercept, gradient)

         return borderIntercept

      else:
         borderIntercept.x = self.__LineEquationUnknownX(
            lineEnd, borderIntercept, gradient)

         return borderIntercept

   def __GetBoundaryCoordinates(self, boundary_constant):
      """
      returns the coordinates for a point on boundary_constant.
      :param boundary_constant: constant for up/down/left/right boundary
      :return: Point containing a border x/y coordinate and a zeroed x/y
               placeholder value

      e.g. if boundary_constant is kOutXLowerBounds,
           then get_boundary_coordinates returns Point(xLowerBoundValue, None)
      """
      point = Point()
      point.x = None
      point.y = None

      if boundary_constant == self.kOutXLowerBounds:
         point.x = self.XAxis.lowerBound

      elif boundary_constant == self.kOutXUpperBounds:
         point.x = self.XAxis.upperBound

      elif boundary_constant == self.kOutYLowerBounds:
         point.y = self.YAxis.lowerBound

      elif boundary_constant == self.kOutYUpperBounds:
         point.y = self.YAxis.upperBound

      return point

   @staticmethod
   def __LineEquationUnknownY(pKnown, pUnknown, gradient):
      """
      returns calculated y value for pUnknown using point slope line equation
      :param pKnown: Point on line with known x and y values
      :param pUnknown: Point on line with unknown y value
      :param gradient: gradient of line
      :return: y value of pUnknown
      """
      y = D(D(gradient) * D(pUnknown.x - pKnown.x)) + D(pKnown.y)
      return int(y.to_integral_value(rounding=decimal.ROUND_HALF_UP))

   @staticmethod
   def __LineEquationUnknownX(pKnown, pUnknown, gradient):
      """
      returns calculated x value for pUnknown using point slope line equation
      :param pKnown: Point on line with known x and y values
      :param pUnknown: Point on line with unknown x value
      :param gradient: gradient of line
      :return: x value of pUnknown
      """
      x = (D(pUnknown.y) -
           D(pKnown.y) +
           (D(gradient) * D(pKnown.x))) / D(gradient)
      return int(x.to_integral_value(rounding=decimal.ROUND_HALF_UP))

   @staticmethod
   def __CalculateGradientFromPoints(startPoint, stopPoint):
      """
      returns the gradient of the line that starts from "startPoint" and ends
      at "stopPoint"
      This method uses the slope equation (y2 - y1)/ (x2 - x1). Fractional
      values are rounded up if fraction is 0.5 or greater

      :param startPoint: Point representing start of line
      :param stopPoint: Point representing end of line
      :return: gradient of the line the crosses both startPoint and stopPoint
      """

      return D(
         (D(stopPoint.y) - D(startPoint.y))
         / (D(stopPoint.x) - D(startPoint.x))
      )

   @staticmethod
   def __CalculateDistanceFromPoints(start, end):
      """
      returns the distance of the line between start and end Points
      :param start: Point where line starts
      :param end: Point where line ends
      :return: distance of line between start and end Points

      :raises decimal.InvalidOperation if squared_sum is negative
      """
      xDiff = D(end.x) - D(start.x)
      yDiff = D(end.y) - D(start.y)
      squareSum = D_cxt().power(xDiff , 2) + D_cxt().power(yDiff, 2)

      return squareSum.sqrt(
         D_cxt()
      )

   @staticmethod
   def __NumberInRange(num1, num2, number):
      return number in range(num1, num2) or number in range(num2, num1)