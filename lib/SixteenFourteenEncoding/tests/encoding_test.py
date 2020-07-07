
import unittest

from unittest.mock import patch


class TestEncoderFunctions(unittest.TestCase):
    def setUp(self):

        self.encoding_samples = {
            "0": "0x4000",
            "-8192": "0x0",
            "8191": "0x7f7f",
            "2048": "0x5000",
            "-4096": "0x2000"
        }

    def test_domains(self):
        from sixteen14encoding.codec.sixteen14hex import Sixteen14Codec

        with self.assertRaises(TypeError):
            Sixteen14Codec.encode("1aaaq")

        with self.assertRaises(ValueError):
            Sixteen14Codec.encode(10000000000)

    def test_encode(self):
        from sixteen14encoding.scripts import encode
        from sixteen14encoding.codec.sixteen14hex import Sixteen14Codec

        for unencoded_int, encoded_hex in self.encoding_samples.items():
            self.assertEqual(
                Sixteen14Codec.encode(int(unencoded_int)), encoded_hex)

            with patch("sys.argv", new=["prog", unencoded_int]):
                self.assertEqual(encode(), encoded_hex)


class TestDecoderFunctions(unittest.TestCase):
    def setUp(self):
        self.decoding_samples = {
            "0x4000": "0",
            "0x0": "-8192",
            "0x7f7f": "8191",
            "0x5000": "2048",
            "0x2000": "-4096"
        }

    def test_domains(self):
        from sixteen14encoding.codec.sixteen14hex import Sixteen14Codec
        with self.assertRaises(TypeError):
            Sixteen14Codec.decode("S0")

        with self.assertRaises(ValueError):
            Sixteen14Codec.decode('0x989680')

    def test_decode(self):
        from sixteen14encoding.scripts import decode
        from sixteen14encoding.codec.sixteen14hex import Sixteen14Codec

        for encoded_hex, decoded_int in self.decoding_samples.items():
            self.assertEqual(Sixteen14Codec.decode(encoded_hex), int(decoded_int))

            with patch("sys.argv", new=["prog", encoded_hex]):
                self.assertEqual(decode(), decoded_int)
