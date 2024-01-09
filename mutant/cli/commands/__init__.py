"""
The modules in here are all command line subcommands.

Each module has a main function that is passed in an argparse
namespace object.
"""

from .create import main as create
from .clone import main as clone
