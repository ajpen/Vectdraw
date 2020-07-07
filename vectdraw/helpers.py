

"""
commonly used helper methods
"""


# chunking recipe from https://stackoverflow.com/a/434328/3044418
def chunker(seq, size):
   """
   returns a generator yielding chunks of size "size" contianing seq items.
   Supports any iterator of any size
   :param seq: iterator to chunk
   :param size: size of each chunk
   :return: generator yielding chunks of size "size"
   """
   return (seq[pos:pos + size] for pos in range(0, len(seq), size))