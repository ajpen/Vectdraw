

"""
stream reader generator
"""


class HexStreamReader(object):
   """
   Reads from a hex string stream byte by byte (2 chars), with local buffering
   An instance of StreamReader acts as a generator, returning
   the newly read byte and also buffering it in self.current_byte

   Any IO exception raised during reading will be left to propagate upwards.
   next() called on an exhausted instance will always raise StopIteration
   """
   currentByte = None

   def __init__(self, stream):
      """
      Initializes StreamReader Instance
      :param stream: an open stream of characters instance (like _io.FileIO)
      """
      if hasattr(stream, 'read'):
         self.stream = stream
      else:
         raise TypeError("Expected object with method 'read', got {}"
                         .format(type(stream)))

      self.closed = False

   def close(self):
      self.stream.close()
      self.closed = True

   def __iter__(self):
      return self

   def __next__(self):
      if self.closed:
         raise StopIteration

      self.currentByte = self.stream.read(2) # 2 characters = 1 hex byte

      if not self.currentByte:
         self.close()
         raise StopIteration

      return self.currentByte