"""
define commands and their parameter methods
"""


import logging

from vectdraw.helpers import chunker
from vectdraw.draw.board import Board
from vectdraw.draw.plane import Point


logger = logging.getLogger(__name__)


class Command(object):
   commandByte = ""
   method = None

   def PrepareParameters(self, *args):
      """
      receives a list of decoded bytes and prepares them for method
      raises exception if unable to prepare parameters

      :param args: list of decoded bytes
      :return: converted parameter for method
      """
      return args


class ClearCommand(Command):
   commandByte = "F0"
   method = 'clear'


class PenUpDownCommand(Command):
   commandByte = "80"
   method = 'ChangePenPosition'


class SetColourCommand(Command):
   commandByte = "A0"
   method = 'SetColour'

   def PrepareParameters(self, r, g, b, a):
      """
      packs r, g, b, a int parameters into tuple
      :param r: decoded byte
      :param g: decoded byte
      :param b: decoded byte
      :param a: decoded byte
      :return: tuple(r, g, b, a)
      """
      return r, g, b, a


class MovePen(Command):
   commandByte = "C0"
   method = 'MovePen'

   def PrepareParameters(self, *args):
      """
      convert list of decoded bytes to list of Points
      if args is an uneven length, the last byte is ignored.
      :param args: list of decoded bytes
      :return: list of Points
      """
      if len(args) % 2 != 0:
         logger.warning("Bytes passed to {} are of odd length: {}"
                        .format(self.__class__.__name__, args))

      points = []
      for pair in chunker(args, 2):
         if len(pair) == 2:
            points.append(Point(pair[0], pair[1]))

      return [points]
