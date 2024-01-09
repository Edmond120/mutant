"""
The modules in here are all command line subcommands.

Each module has a main function that is passed in an argparse
namespace object.
"""

from .mutation import main as mutation
