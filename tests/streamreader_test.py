import unittest
import io

from vectdraw.hexstreamreader import HexStreamReader


class TestStreamReader(unittest.TestCase):

   def setUp(self):
      self.stream = HexStreamReader(io.StringIO("123456789"))

   def tearDown(self):
      self.stream.close()

   def test_constructor(self):
      with self.assertRaises(TypeError):
         HexStreamReader('2')

   def test_stream_reader_buffer(self):
      self.assertIsNone(self.stream.currentByte)
      self.assertEqual(next(self.stream), '12')
      self.assertEqual(self.stream.currentByte, '12')

      self.assertEqual(next(self.stream), '34')
      self.assertEqual(self.stream.currentByte, '34')

      self.assertEqual(next(self.stream), '56')
      self.assertEqual(self.stream.currentByte, '56')

      self.assertEqual(next(self.stream), '78')
      self.assertEqual(self.stream.currentByte, '78')

      self.assertEqual(next(self.stream), '9')
      self.assertEqual(self.stream.currentByte, '9')


   def test_stream_reader(self):
      correct_vals = ['12', '34', '56', '78', '9']

      for index, hex_b in enumerate(self.stream):
         self.assertEqual(hex_b, correct_vals[index])

      with self.assertRaises(StopIteration):
         next(self.stream)