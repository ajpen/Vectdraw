"""

"""

import sys

from sixteen14encoding.codec.sixteen14hex import Sixteen14Codec
from vectdraw.cli import ParseArgs
from vectdraw.process import VectorCommandStreamProcessor
from vectdraw.draw.board import Board, Pen
from vectdraw.hexstreamreader import HexStreamReader
from vectdraw.settings import REGISTERED_COMMANDS


def main(debug=False):
   """
   gets cli parameters initializes and runs command processor
   if debug is given, cleanup is left for handling by the caller
   :param debug: performs cleanup if False
   """
   cliParams = ParseArgs()
   streamReader = HexStreamReader(cliParams.get('f', sys.stdin))
   output = cliParams.get('o', sys.stdout)
   board = Board(Pen(), outputStream=output)

   processor = VectorCommandStreamProcessor(
      streamReader, Sixteen14Codec(), board, REGISTERED_COMMANDS)

   processor.run()

   if not debug:
      if not streamReader.closed:
         streamReader.close()
      if output is not sys.stdout and not output.closed:
         output.close()
