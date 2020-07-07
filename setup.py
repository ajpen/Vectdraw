
import setuptools
import os


setuptools.setup(
   name="vectdraw",
   version="0.1.0",
   author="Anfernee Jervis",
   description="Vector based drawing system based on an encoded byte system",
   install_requires=['sixteen14encoding==0.1'],
   tests_require=['sixteen14encoding==0.1'],
   dependency_links=[
      'file://' + os.path.join(os.getcwd(),
                               'lib', 'SixteenFourteenEncoding#egg=sixteen14encoding-0.1.0')
   ],
   packages=setuptools.find_packages(),
   test_suite="tests",
   entry_points={
      "console_scripts": {
         "vectdraw = vectdraw.scripts:main"
      }
   },
)
