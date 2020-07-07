
"""
script methods for encoding/decoding
"""
import sys

from sixteen14encoding import __script_names
from sixteen14encoding.codec.sixteen14hex import Sixteen14Codec


def encode():
    """
    parses command line arguments and attempts to encode
    the parsed argument. Meant to be used with setuptools'
    entrypoint. The returned value/exception is printed to
    stderr
    """
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg is None:
        return "Usage:{0} Integer".format(__script_names["encode"])

    try:
        return Sixteen14Codec.encode(arg)
    except (TypeError, ValueError) as e:
        return str(e)


def decode():
    """
    parses command line arguments and attempts to decode
    the parsed argument. Meant to be used with setuptools'
    entrypoint. The returned value/exception is printed to
    stderr
    """
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg is None:
        return "Usage:{0} Integer".format(__script_names["decode"])

    try:
        return str(Sixteen14Codec.decode(arg))
    except (TypeError, ValueError) as e:
        return str(e)