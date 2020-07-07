import unittest
import os
import sys

from unittest.mock import patch
from io import StringIO

from vectdraw.scripts import main


class TestEndToEndSTDIO(unittest.TestCase):

   def setUp(self):
      self.mock_stdin = StringIO("F0A04000417F4000417F"
                                "C040004000804001C05F205F20804000")

      self.expected_output = ("CLR;\nCO 0 255 0 255;\nMV (0, 0);\n"
                              "PEN DOWN;\nMV (4000, 4000);\nPEN UP;\n")

   @patch('sys.argv', new=sys.argv[:1])
   def test_e2e_stdio(self):
      with patch('sys.stdin', new=self.mock_stdin):
         with patch('sys.stdout', new_callable=StringIO) as mock_stdout:

            main()
            self.assertEqual(self.expected_output, mock_stdout.getvalue())


class TestEndToEndFile(unittest.TestCase):

   def setUp(self):
      self.input_target = os.path.join('tests', 'box.txt')
      self.output_target = 'test_output.txt'
      self.mock_argv = [
         '-f', self.input_target, '-o', self.output_target]

      self.expected = ("CLR;\nCO 0 0 255 255;\nMV (0, 0);\nPEN DOWN;\n"
                       "MV (4000, 0) (4000, -8000) (-4000, -8000) (-4000, 0) "
                       "(-500, 0);\nPEN UP;\n")

   def tearDown(self):
      if os.path.exists(self.output_target):
         os.remove(self.output_target)

   def test_e2e_file(self):
      with patch('sys.argv', new=sys.argv[:1] + self.mock_argv):
         main()

         with open(self.output_target) as f:
            output = f.read()

         self.assertEqual(self.expected, output)


class TestEndToEndFileBoundary(unittest.TestCase):

   def setUp(self):
      self.input_target = os.path.join('tests', 'boundary.txt')
      self.output_target = 'test_output.txt'
      self.mock_argv = [
         '-f', self.input_target, '-o', self.output_target]

      self.expected = ("CLR;\nCO 255 0 0 255;\nMV (5000, 5000);\nPEN DOWN;\n"
                       "MV (8191, 5000);\nPEN UP;\nMV (8191, 0);\nPEN DOWN;\n"
                       "MV (5000, 0);\nPEN UP;\n")

   def tearDown(self):
      if os.path.exists(self.output_target):
         os.remove(self.output_target)

   def test_e2e_file(self):
      with patch('sys.argv', new=sys.argv[:1] + self.mock_argv):
         main()

         with open(self.output_target) as f:
            output = f.read()

         self.assertEqual(self.expected, output)


class TestEndToEndSTDIOBoundaryExample(unittest.TestCase):

   def setUp(self):
      self.mock_stdin = StringIO("F0A0417F41004000417FC067086708804001C0"
                                 "67082C3C18782C3C804000")

      self.expected_output = ("CLR;\nCO 255 128 0 255;\nMV (5000, 5000);\n"
                              "PEN DOWN;\nMV (8191, 3405);\nPEN UP;\n"
                              "MV (8191, 1596);\nPEN DOWN;\nMV (5000, 0);\n"
                              "PEN UP;\n")

   @patch('sys.argv', new=sys.argv[:1])
   def test_e2e_boundary_stdio(self):
      with patch('sys.stdin', new=self.mock_stdin):
         with patch('sys.stdout', new_callable=StringIO) as mock_stdout:

            main()
            actual_output = mock_stdout.getvalue()
            self.assertEqual(
               self.expected_output, actual_output,
               msg='{}\n!= \n{}'.format(self.expected_output, actual_output))


class TestEndToEndSTDIOSquareExample(unittest.TestCase):

   def setUp(self):
      self.mock_stdin = StringIO("F0A040004000417F417FC04000400090400047684F50"
                                 "57384000804001C05F20400040000140014040004000"
                                 "7E405B2C4000804000")

      self.expected_output = ("CLR;\nCO 0 0 255 255;\nMV (0, 0);\nPEN DOWN;\n"
                              "MV (4000, 0) (4000, -8000) (-4000, -8000) "
                              "(-4000, 0) (-500, 0);\nPEN UP;\n")

   @patch('sys.argv', new=sys.argv[:1])
   def test_e2e_square_stdio(self):
      with patch('sys.stdin', new=self.mock_stdin):
         with patch('sys.stdout', new_callable=StringIO) as mock_stdout:

            main()
            actual_output = mock_stdout.getvalue()
            self.assertEqual(
               self.expected_output, actual_output,
               msg='{}\n!= \n{}'.format(self.expected_output, actual_output))
