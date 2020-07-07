"""
handle command line arguments
"""


import argparse


__description = """byte encoded vector based drawing system"""
__fParameterDescription = "path to byte command file"
__oParameterDescription = "path to output file"


def ParseArgs():
   """
   parses and validates command line arguments
   any given paths are opened and returned. If not arguments
   are specified, stdin & stdout are used for -f and -o respectively

   Raises file related exceptions (IOError, etc)

   returns args in the format:
   {"f": _io.FileIO, "o": _io.TextIOWrapper}

   :return: dict containing parsed arguments
   """
   parser = argparse.ArgumentParser(description=__description)
   parser.add_argument(
      "-f", nargs="?", default="-", type=argparse.FileType('r'),
      help=__fParameterDescription)

   parser.add_argument(
      "-o", nargs="?", default="-", type=argparse.FileType("w"),
      help=__oParameterDescription)

   return vars(parser.parse_args())