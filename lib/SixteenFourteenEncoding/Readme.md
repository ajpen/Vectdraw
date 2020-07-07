# Sixteen Fourteen Hex Codec

Sixteen Fourteen Hex Codec contains methods for encoding 14 bit signed integers into 16 bit hexadecimals and vice versa.

Sixteen Fourteen Hex Codec or `sixteen14encoding` contains both a CLI application for encoding/decoding and a class exposing `encode/decode` methods.

### Installation

1. clone or download and extract repository.
2. run  `python setup.py install`  It is recommended to install the package in a `virtualenv` or to install it locally using `python setup.py install --user`



### Usage

#### CLI Commands

`hex_encode 14bit_integer` - returns an encoded 16 bit hexadecimal number 

`hex_decode 16bit_hexadecimal`  - returns a decoded signed 14 bit integer

*NOTE: both commands output values to stderr. To output to stdout on *nix, append stderr to stdout by appending `2>&1` to the command* 

**Example**:

`hex_encode 6141` outputs  `0x6f7d`

`hex_decode 0x6f7d` outputs `6141`

### `Sixteen14Codec` Class

The `Sixteen14Codec` class can be found in the module `sixteen14encoding.codec.alhex` and exposes `encode` and `decode` class methods that implements the Sixteen Fourteen Hex encoding. Instantiation isn't necessary for usage. 

 `Sixteen14Codec.encode` accepts a 14 bit int and returns an encoded hexadecimal string. 

`Sixteen14Codec.decode` accepts a 16 bit hexadecimal string and returns a decoded 14 bit int.



### Compatibility

Compatible with python 3+.