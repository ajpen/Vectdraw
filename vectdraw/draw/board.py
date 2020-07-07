

"""
board class for vector drawing
"""
import sys
import queue

from vectdraw.draw.pen import Pen
from vectdraw.draw.colour import Colour
from vectdraw.draw.plane import VirtualPlane, Point


class Board(VirtualPlane):

   pen = None
   outputStream = None

   def __init__(self, pen, outputStream=sys.stdout, **kwargs):

      super(Board, self).__init__(**kwargs)

      self.currentPenLocation = Point()
      self.lastPenLocation = Point()

      if isinstance(pen, Pen):
         self.pen = pen

      if (outputStream and
            hasattr(outputStream, 'write') and
            hasattr(outputStream, 'flush')):

         self.outputStream = outputStream

   def clear(self):
      """
      Clears the board and prints the command result to the output stream
      """
      self.pen.reset()
      self.currentPenLocation = Point()

      self.__WriteToStream("CLR;\n")

   def ChangePenPosition(self, position):
      """
      changes pen position up or down and prints the command result to the
      output stream

      :param position: up if 0, else down
      """
      if position == 0:
         self.pen.lift()
         self.__WriteToStream("PEN UP;\n")

      else:
         self.pen.down()
         self.__WriteToStream("PEN DOWN;\n")

   def SetColour(self, r, g, b, a):
      """
      sets red, green, blue, alpha attributes for the pen and prints the
      command result to the output stream

      :param r: int between 0-255 representing red hue
      :param g: int between 0-255 representing green hue
      :param b: int between 0-255 representing blue hue
      :param a: int between 0-255 representing alpha
      """
      self.pen.ChangeColour(Colour((r, g, b, a)))

      self.__WriteToStream(
         "CO {} {} {} {};\n".format(r, g, b, a))

   def MovePen(self, points):
      """
      Moves pen to area on board specified by points. Movement is relative to
      the pen's current location on the board. Movement behaviour depends on
      the pen's position.

      If the pen is up, MovePen moves the pen to the calculated final
      destination and prints it to the output stream.

      If pen is down, MovePen calculates the new position for each point and
      prints it to the output stream.

      if the pen moves outside the board boundaries, it is lifted until moved
      back within the boundaries, where it is then placed down again.

      :param points: list of Point instances
      """
      if not self.pen.IsPenDown():
         self.__MoveToFinalDestination(points)

      else:
         self.__draw(points)

   def __MoveToFinalDestination(self, points):
      """
      Calculates the final location of the pen from points, and prints the
      location to the output stream

      if the pen crosses the boundary, it is placed on the boundary at the
      position it crossed
      :param points: list of Point instances
      """
      for point in points:
         self.lastPenLocation = self.currentPenLocation
         self.__MovePenLocation(point)

      boundaryIntercepts = self.GetBoundaryIntercepts(
         self.lastPenLocation, self.currentPenLocation)

      if (boundaryIntercepts and
            not self.__IsPointWithinBoundaries(self.currentPenLocation)):
         self.__WriteToStream("MV {};\n".format(boundaryIntercepts[-1][0]))
      else:
         self.__WriteToStream("MV {};\n".format(self.currentPenLocation))

   def __MovePenLocation(self, by):
      """
      moves pen by the values specified in "by". The method essentially adds
      the point to the pen's current position
      :param by: Point instance
      """
      self.currentPenLocation = self.currentPenLocation + by

   def __draw(self, points):
      """
      MovePen implementation for when the pen is down. It converts points to
      an iterator and moves the pen to the calculated new position per point.

      If the pen moves outside the boards boundaries it is placed on the
      boundary and its position is printed to the output stream. The pen is
      then lifted and moved based on the remaining points until moved within
      the board's boundaries. Then pen is then placed down and this draw
      is called with the remaining points

      For output accuracy, points to be printed are bufferd until a border is
      crossed or no more points are left to print
      :param points: list of Point instances
      """
      outputBuffer = queue.Queue()
      for point in points:

         # Store last location and move point
         self.lastPenLocation = self.currentPenLocation
         self.__MovePenLocation(point)

         # get boundaries, if any
         boundaryIntercepts = self.GetBoundaryIntercepts(
            self.lastPenLocation, self.currentPenLocation)

         # if boundaries crossed, print points leading to crossing then handle
         # the boundary intercept points
         if boundaryIntercepts:
            outputBuffer.put(boundaryIntercepts[0][0])
            self.__PrintMovePointsFromBuffer(outputBuffer)
            self.__HandleCrossedBoundaries(boundaryIntercepts)

         if (self.pen.IsPenDown() and
             self.__IsPointWithinBoundaries(self.currentPenLocation)):

            outputBuffer.put(self.currentPenLocation)

      self.__PrintMovePointsFromBuffer(outputBuffer)

   def __PrintMovePointsFromBuffer(self, buffer):
      """
      pops points from buffer and writes them to stream as a single move command
      :param buffer: queue of Point instances
      """
      outputString = ""
      while True:
         try:
            point = buffer.get_nowait()
         except queue.Empty:
            break
         outputString += " {}".format(point)

      if outputString:
         outputString = "MV" + outputString + ";\n"
         self.__WriteToStream(outputString)

   def __HandleCrossedBoundaries(self, boundaries):
      """
      handles pen movement & output for any boundaries crossed by the pen.
      NOTE: Outputting the first boundary is handled by the caller
      :param boundaries: sorted list of intercept(Point)-distance(Decimal) pairs
      """
      for index, boundary in enumerate(boundaries):
         if index > 0:
            self.__WriteToStream("MV {}\n".format(boundary[index][0]))

         if (not self.pen.IsPenDown() and
               not self.__IsPointWithinBoundaries(self.lastPenLocation)):

            self.ChangePenPosition(1)
         else:
            self.ChangePenPosition(0)

   def __IsPointWithinBoundaries(self, point):
      """
      Returns true if point is within legal space of the plane
      :param point: Point instance in question
      :return: True if point is within board boundaries, else false
      """
      return (
            self.XAxis.lowerBound < point.x <
            self.XAxis.upperBound and

            self.YAxis.lowerBound < point.y <
            self.YAxis.upperBound)

   def __output_current_position(self):
      self.__WriteToStream(" {}".format(self.currentPenLocation))

   def __WriteToStream(self, message):
      self.outputStream.write(message)
      self.outputStream.flush()
