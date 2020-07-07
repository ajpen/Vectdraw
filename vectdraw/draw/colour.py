

"""
Class for rgba colour representation
"""


class Colour(object):
   red = 0
   green = 0
   blue = 0
   alpha = 255

   def __init__(self, rgba=None):
      """
      Returns a colour instance. If nothing is passsed, the default
      is 0,0, 0, 255 for red, green, blue and alpha respectively

      :param rgba: a tuple containing numbers between 0-255 for red, green,
                   blue and alpha respectively
      """
      if rgba:
         self.SetColour(rgba)

   def SetColour(self, rgba):
      if not isinstance(rgba, tuple) and len(rgba) != 4:
         raise TypeError(
            "Unexpected type given. Expected tuple of size 4 "
            "(int, int, int, int), received {}".format(type(rgba)))

      for c in rgba:
         if c > 255 or c < 0:
            raise ValueError(
               "Colour values are outside of the domain (0-255)")

      self.red, self.green, self.blue, self.alpha = rgba

   def __eq__(self, other):
      if isinstance(other, self.__class__):
         return (self.red == other.red and
                 self.green == other.green and
                 self.blue == other.blue and
                 self.alpha == other.alpha)
      else:
         raise NotImplemented