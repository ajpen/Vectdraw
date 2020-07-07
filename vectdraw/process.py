

"""
Reads a stream of vector command bytes and executes the
respective board methods
"""

import collections.abc
import logging

from vectdraw.hexstreamreader import HexStreamReader
from vectdraw.draw.board import Board
from vectdraw.commands.default import Command
from vectdraw.commands.errors import DuplicateCommandCodeError


class VectorCommandStreamProcessor(object):

   kMaxUnsignedBitVal = 255
   kMostSignificantBitShift = 7

   streamreader = None
   encoding_class = None
   vectorBoard = None

   def __init__(self, reader, encodingClass, board, commands):
      if not isinstance(reader, HexStreamReader):
         raise TypeError("reader argument must be of type {}"
                         .format(type(HexStreamReader)))

      if (not hasattr(encodingClass, 'decode') or
          not callable(encodingClass.decode)):

         raise TypeError("encoding_class argument not a valid type: "
                         "missing attribute method 'decode'")

      if not isinstance(board, Board):
         raise TypeError("board argument must be of type {}"
                         .format(type(Board)))

      self.registeredCommands = {}
      self.streamreader = reader
      self.encoding_class = encodingClass
      self.vectorBoard = board
      self.__RegisterCommands(commands)

      self.logger = logging.getLogger(self.__class__.__name__)

   def run(self):
      """
      Iterates over streamreader, executing methods specified by reeived
      command bytes. Unrecognized bytes are logged and discarded.
      All runtime exceptions are propagated upwards and should be handled
      by the caller

      Note that Iteration also happens in get_args().

      NOTE: This is definitely not the best way to do this. A better method is
      needed
      """

      try:
         while self.streamreader.currentByte or next(self.streamreader):
            byte = self.streamreader.currentByte

            if self.IsCommandByte(byte):
               command = self.registeredCommands.get(byte, None)
               if command is None:
                  self.logger.warning("Received unrecognized command byte {}"
                                      .format(byte))
                  next(self.streamreader)

               else:
                  args = self.GetArgs()
                  prepped_args = command.PrepareParameters(*args)
                  getattr(self.vectorBoard, command.method)(*prepped_args)
            else:
               next(self.streamreader)

      except StopIteration:
         return

   def IsCommandByte(self, byte):
      """
      shifts byte to the right by 7 to get the value of the 8th bit
      :param byte: hexadecimal string representation of a byte
      :return: True if byte is command byte (MSB set), else false
      """
      if not byte.strip():
         return False

      byte = int(byte, 16)
      if byte > self.kMaxUnsignedBitVal:
         raise ValueError("expected single unsigned byte for byte "
                          "argument (0-255), received {}".format(byte))

      return byte >> self.kMostSignificantBitShift

   def GetArgs(self):
      """
      iterate over streamreader, extracting and decoding encoded argument
      values until command byte is read
      :return: list of decoded byte arguments
      """
      byte_pair = list()
      decodedArgs = []
      for arg in self.streamreader:
         if self.IsCommandByte(arg):
            break

         else:
            byte_pair.append(arg)

         if len(byte_pair) == 2:
            decodedArgs.append(
               self.encoding_class.decode(''.join(byte_pair)))

            byte_pair = list()

      return decodedArgs

   def __RegisterCommands(self, commands):

      if (not isinstance(commands, collections.abc.Sequence) or
            isinstance(commands, str)):

         raise TypeError("commands argument must be a non string sequence "
                         "containing instances of {}".format(type(Command)))

      for command in commands:
         if not issubclass(command, Command):
            raise TypeError("commands argument must be a non string sequence "
                         "containing instances of {}".format(type(Command)))

         if self.registeredCommands.get(command.commandByte, None) is None:
            self.registeredCommands[command.commandByte] = command()

         else:
            raise DuplicateCommandCodeError(
               "attempted to register {com_byte} to {comm}, "
               "which is already registered by {reg_comm}"
               .format(com_byte=command.commandByte, comm=command,
                       reg_comm=self.registeredCommands[command.commandByte]))
