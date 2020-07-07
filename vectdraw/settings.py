

"""
   Contains internal application configuration

   Command classes added to the REGISTERED_COMMANDS are added to the list of
   commands available to the main method
   Valid command classes should have a defined command byte, a method function
   of Board and a PrepareParameters method

   see vectdraw.commands.default.Command
"""

from vectdraw.commands import *

REGISTERED_COMMANDS = [
   ClearCommand,
   PenUpDownCommand,
   SetColourCommand,
   MovePen
]