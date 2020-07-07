import unittest
import io

from vectdraw.process import VectorCommandStreamProcessor
from vectdraw.process import DuplicateCommandCodeError
from vectdraw.draw.board import Board, Pen
from vectdraw.settings import REGISTERED_COMMANDS
from vectdraw.commands.default import Command, MovePen
from vectdraw.hexstreamreader import HexStreamReader


from sixteen14encoding.codec.sixteen14hex import Sixteen14Codec


class TestCommand(Command):

   commandByte = "80"
   method = 'clear'

   def PrepareParameters(self, *args):
      return args


class TestStreamProcessor(unittest.TestCase):

   def setUp(self):
      self.out = io.StringIO()
      self.stream = HexStreamReader(io.StringIO(
         "F0A0417F40004000417FC067086708804001C0670840004000187818784000"
         "804000"))

      self.encoding = Sixteen14Codec
      self.board = Board(Pen(), outputStream=self.out)
      self.commands = REGISTERED_COMMANDS

   def test_constructor(self):

      with self.assertRaises(TypeError):
         VectorCommandStreamProcessor('', '', '', '')

      with self.assertRaises(TypeError):
         VectorCommandStreamProcessor(self.stream, '', '', '')

      with self.assertRaises(TypeError):
         VectorCommandStreamProcessor(self.stream, self.encoding, '', '')

      with self.assertRaises(TypeError):
         VectorCommandStreamProcessor(
            self.stream, self.encoding, self.board, '')

      with self.assertRaises(TypeError):
         VectorCommandStreamProcessor(
            self.stream, self.encoding, self.board, [''])

      VectorCommandStreamProcessor(
         self.stream, self.encoding, self.board, self.commands)


   def test_register_commands(self):
      commands = [Command, Command]

      with self.assertRaises(DuplicateCommandCodeError):
         VectorCommandStreamProcessor(
         self.stream, self.encoding, self.board, commands)

   def test_get_args(self):
      stream = HexStreamReader(
         io.StringIO('C067086708804001C0670840004000187818784000'))

      processor = VectorCommandStreamProcessor(
         stream, self.encoding, self.board, self.commands)

      next(stream)
      self.assertListEqual(processor.GetArgs(), [5000, 5000])

   def test_run(self):

      stream = HexStreamReader(
         io.StringIO('8080'))
      commands = [TestCommand]
      processor = VectorCommandStreamProcessor(
         stream, self.encoding, self.board, commands)

      processor.run()
      self.assertEqual(self.out.getvalue(), "CLR;\nCLR;\n")


   def test_run_with_args(self):

      stream = HexStreamReader(
         io.StringIO('C067086708'))
      commands = [TestCommand, MovePen]
      processor = VectorCommandStreamProcessor(
         stream, self.encoding, self.board, commands)

      processor.run()
      self.assertEqual(self.out.getvalue(), "MV (5000, 5000);\n")