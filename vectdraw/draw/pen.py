

"""
Class representing the pen
"""

from vectdraw.draw.colour import Colour


class Pen(object):

   __kDefaultColour = Colour()

   # determines the position of pen. False is Up, True is Down
   __isDown = False

   # Current colour of the pen (red, green, blue, alpha)
   __colour = __kDefaultColour

   def ChangeColour(self, rgba):
      if isinstance(rgba, Colour):
         self.__colour = rgba

      else:
         raise TypeError(
            "Expected board.Colour instance"
            "Received {}".format(str(rgba)))

   def lift(self):
      """
      sets the pen position to up
      """
      self.__isDown = False

   def colour(self):
      return self.__colour

   def down(self):
      """
      sets the pen position to down
      """
      self.__isDown = True

   def reset(self):
      self.lift()
      self.ChangeColour(self.__kDefaultColour)

   def IsPenDown(self):
      return self.__isDown
