import sys
import mutant
from mutant.exceptions import InvalidMutantDirectoryError

def main(): # pragma: nocover
	try:
		mutant.cli.run_command(sys.argv[1:])
	except InvalidMutantDirectoryError as e:
		print(e)
		sys.exit(1)
