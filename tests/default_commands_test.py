import unittest
from unittest import mock

from vectdraw.commands.default import *
from vectdraw.draw.plane import Point


class TestMovePenCommand(unittest.TestCase):

   def setUp(self):
      self.params = [255, 255, 255, 255, 88, 97, 98, 99, 99, 99]
      self.params_odd = [255, 255, 255, 255, 88, 97, 98, 99, 99]
      self.expected = [[
         Point(255, 255), Point(255, 255), Point(88, 97),
         Point(98, 99), Point(99, 99)
      ]]

      self.expected_odd = [[
         Point(255, 255), Point(255, 255), Point(88, 97),
         Point(98, 99)
      ]]

   def test_even_PrepareParameters(self):
      params_received = MovePen().PrepareParameters(*self.params)
      self.assertListEqual(self.expected, params_received)

   def test_odd_PrepareParameters(self):

      logger = logging.getLogger('vectdraw.commands.default')
      with mock.patch.object(logger, 'warning') as mock_warning:

         params_received = MovePen().PrepareParameters(*self.params_odd)
         self.assertListEqual(self.expected_odd, params_received)

         mock_warning.assert_called_once_with(
            "Bytes passed to {} are of odd length: {}"
               .format(MovePen.__name__, tuple(self.params_odd)))