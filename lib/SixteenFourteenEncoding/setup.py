
import setuptools
from sixteen14encoding.scripts import __script_names

setuptools.setup(
    name="sixteen14encoding",
    version="0.1.0",
    author="Anfernee Jervis",
    description="Encodes a 14bit integer into a 16bit hex string and vice versa.",

    packages=setuptools.find_packages(),

    entry_points={
        "console_scripts": {
            "{0} = sixteen14encoding.scripts:encode".format(__script_names["encode"]),
            "{0} = sixteen14encoding.scripts:decode".format(__script_names["decode"])
        }
    },

    test_suite="tests"
)
