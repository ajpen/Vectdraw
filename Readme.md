# VectDraw

Vectdraw is a command line vector drawing application. vectdraw takes commands and Sixteen Fourteen encoded arguments for drawing on a vector plane via standard input or file, and outputs to standard out or file. 

Currently vectdraw only outputs the interpretation of the command. 

### Installation

1. clone or download and extract repository.
2. run  `python setup.py install`  It is recommended to install the package in a `virtualenv` or to install it locally using `python setup.py install --user`

### Usage

`usage: vectdraw [-h] [-f [F]] [-o [O]]`

vectdraw without specifying arguments waits for byte commands from standard input. vectdraw exits after reading newline characters, so all input command bytes and arguments should be given before return is pressed. Vectdraw then parses each command and decodes any arguments before printing the result.

e.g.

```bash
vectdraw
F0A04000417F4000417FC040004000804001C05F205F20804000
=======================================================
CLR;
CO 0 255 0 255;
MV (0, 0);
PEN DOWN;
MV (4000, 4000);
PEN UP;
```



vectdraw can consume commands from a file. Files can have newline or space characters. They will be ignored. To specify the input file, use the `-f` argument followed by the file.  

```
vectdraw -f line.txt (assume line.txt contains the below string: F0A04000417F4000417FC040004000804001C05F205F20804000
=======================================================
CLR;
CO 0 255 0 255;
MV (0, 0);
PEN DOWN;
MV (4000, 4000);
PEN UP;
```



vectdraw also has the ability to write the result to file instead of the console using the argument `-o`. 

run `vectdraw --help` for more info

### Compatibility

Compatible with python 3+.