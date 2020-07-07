import unittest
import sys

from unittest.mock import patch
from io import StringIO

from vectdraw.cli import ParseArgs


class TestCLIParser(unittest.TestCase):
   """
   parse_cli_args should throw an exception on UI related issues
   (FileNotFound, PermissionDenied, etc)

   it should default to sys.stdout/sys.stdin if no args are passed

   and should successfully open the file given with the correct permissions
   """

   def setUp(self):
      self.bad_path_param = ['-f', 'qweqenasnaisd2123123.txtt',
                             '-o', 'asdasdn332i3j.txtt']

      self.good_path_param = ['-f', 'tests/__init__.py', '-o',
                              'tests/__init__.py']
      self.args = None

   @patch('sys.stderr', new_callable=StringIO)
   def test_bad_arguments(self, mock_stderr):
      # parser.parse_args() raises SystemExit on error and writes to stderr
      # stderr is patched to suppress output and test exceptions raised

      with self.assertRaises(SystemExit):
         with patch('sys.argv', new=[sys.argv[0]] + self.bad_path_param):
            ParseArgs()

         # Ensures the right exception was raised
         self.assertRegexpMatches(mock_stderr.getvalue(), r"IOError")

   def test_defaults(self):
      with patch('sys.argv', new=[sys.argv[0]]):
         args = ParseArgs()
      self.assertEqual(args["f"].name, "<stdin>")
      self.assertEqual(args["o"].name, "<stdout>")

   def test_good_arguments(self):
      with patch('sys.argv', new=[sys.argv[0]] + self.good_path_param):
         self.args = ParseArgs()
         self.assertEqual(self.args["f"].name, "tests/__init__.py")
         self.assertEqual(self.args["o"].name, "tests/__init__.py")

      for k, v in self.args.items():
         v.close()
