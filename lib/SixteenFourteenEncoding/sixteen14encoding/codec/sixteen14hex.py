
"""
codec class for Sixteen Fourteen Hex Encoding
"""

from sixteen14encoding.codec.basicbit import BaseBitCodec


class Sixteen14Codec(BaseBitCodec):
    """
    Implements Sixteen Fourteen Hex encoding

    Sixteen14Codec contains two public methods for encoding 14 bit integers
    and decoding the 16 bit hexadecimal result
    """

    # used to shift 14bit signed integers to an unsigned integer and vice versa
    _SIGNED_UNSIGNED_CONVERTER = 8192

    # used to mask the bits from the least significant bit to the 7th bit (2^7 place), inclusive
    _LEAST_SIGNIFICANT_BIT_TO_7TH_MASK = 127

    # used to mask the bits from 16th bit(2^16 place) to the 9th bit (2^9 place), inclusive
    _16TH_BIT_TO_9TH_ENCODING_MASK = 65280

    # used to mask the bits from 16th bit(2^16 place) to the 8th bit (2^8 place), inclusive
    _16TH_BIT_TO_8TH_DECODING_MASK = 65408

    _ENCODING_DOMAIN = [-8192, 8191]

    _DECODING_DOMAIN = [0x0000, 0x7f7f]

    @classmethod
    def encode(cls, integer):
        """
        encodes a 14bit signed integer using Sixteen Fourteen Encoding

        :param integer: 14bit int or string representation of a 14bit int
        :return: a 16bit encoded hex string
        """
        try:
            converted_int = int(integer)
        except (TypeError, ValueError):
            raise TypeError("Expected 14 bit int, got unsupported value {0}"
                            .format(integer))

        if not cls.is_within_domain(converted_int, cls._ENCODING_DOMAIN):
            raise ValueError("Argument {0} is outside supported domain {1}"
                             .format(integer, cls._ENCODING_DOMAIN))

        return hex(cls._encode(converted_int))

    @classmethod
    def decode(cls, hexadecimal):
        """
        decodes an 16 bit hexadecimal string encoded with Sixteen Fourteen Encoding
        into a 14bit signed integer

        :param hexadecimal: 16bit hexadecimal string
        :return: a 14bit decoded int
        """
        try:
            converted_int = int(hexadecimal, 16)
        except ValueError:
            raise TypeError(
                "Expected 16 bit hexadecimal, got unsupported value {0}"
                 .format(hexadecimal))

        if not cls.is_within_domain(converted_int, cls._DECODING_DOMAIN):
            raise ValueError("Argument {0} is outside supported domain {1}"
                             .format(hexadecimal, cls._DECODING_DOMAIN))

        return cls._decode(converted_int)

    @staticmethod
    def is_within_domain(arg, domain):
        """
        returns false if arg is not within domain
        """
        if arg < domain[0] or arg > domain[1]:
            return False

        return True

    @classmethod
    def _encode(cls, number):
        """
        unpacks a 14bit integer into a 16bit integer, each byte with
        their highest significant bit cleared

        :param number: signed 14 bit number within the _ENCODING_DOMAIN
        :return: 16bit integer within the _DECODING_DOMAIN

        example:
        given 00111111 11111011 _encode would return 01111111 01111011
        """
        number_unsigned = number + cls._SIGNED_UNSIGNED_CONVERTER

        masked_first_seven_bits = cls.mask(
            number_unsigned, cls._LEAST_SIGNIFICANT_BIT_TO_7TH_MASK)

        partially_encoded = cls.leftshift(number_unsigned, 1)

        partially_encoded = cls.mask(
            partially_encoded, cls._16TH_BIT_TO_9TH_ENCODING_MASK)

        return cls.mergebits(partially_encoded, masked_first_seven_bits)

    @classmethod
    def _decode(cls, number):
        """
        packs the 2 byte integer into a 14 byte integer by reversing the
        process defined in _encode

        :param number: 16bit integer within the _DECODING_DOMAIN
        :return: signed 14 bit number within the _ENCODING_DOMAIN

        example:
        given 01111111 01111011 _edecode would return 00111111 11111011
        """

        masked_first_seven_bits = cls.mask(
            number, cls._LEAST_SIGNIFICANT_BIT_TO_7TH_MASK)

        partially_decoded = cls.rightshift(number, 1)

        partially_decoded = cls.mask(
            partially_decoded, cls._16TH_BIT_TO_8TH_DECODING_MASK)

        partially_decoded = cls.mergebits(
            partially_decoded, masked_first_seven_bits)

        return partially_decoded - cls._SIGNED_UNSIGNED_CONVERTER