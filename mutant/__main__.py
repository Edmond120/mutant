import sys
import argparse
import mutant
from mutant.exceptions import InvalidMutantDirectoryError

try:
	mutant.cli.run_command(sys.argv[1:])
except InvalidMutantDirectoryError as e:
	print(e)
