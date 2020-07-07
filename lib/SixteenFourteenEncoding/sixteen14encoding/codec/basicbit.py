
"""
base codec class with helpers for Sixteen Fourteen Hex Encoding
"""


class BaseBitCodec(object):

    @staticmethod
    def mask(num, masker):
        """
        preserves only the bits of num that are set by the masker

        :param num: integer to be masked
        :param masker: integer whose bits indicate which bits to preserve
        :return: result of num AND masker


        Example, assume num=1240, masker=127
        num in binary is    10011011000
        masker in binary is 00001111111
        num AND masker 		00001011000

        mask(num, masker) would return 88
        """
        return num & masker

    @staticmethod
    def leftshift(num, n):
        """
        returns the result of num shifted to the left n times

        :param num: integer to be shifted
        :param n: number of times to shift. Must be a whole number
        :return: returns the result of shifting the bits of num
        "n" times to the left

        Example, assume num=1240, by=2
        num in binary is:     0010011011000
        num after left shift" 1001101100000

        leftshift(num, shift_by) would return 4960
        """
        return num << n

    @staticmethod
    def rightshift(num, n):
        """
        returns the result of num shifted to the right n times

        :param num: integer to be shifted
        :param n: number of times to shift. Must be a whole number
        :return: returns the result of shifting the bits of num
        "n" times to the right

        Example, assume num=1240, by=2
        num in binary is:     0010011011000
        num after left shift" 0000110110010

        rightshift(1240, 2) would return 434
        """
        return num >> n

    @staticmethod
    def mergebits(x, y):
        """
        merges the bits of x and y together

        :param x: integer to be merged
        :param y: integer to be merged
        :return: result of x OR y

        Example, assume x=218, y=36
        x in binary is:  11011010
        y in binary is:  00100100
        mergebits(x, y): 11111110
        """
        return x | y
