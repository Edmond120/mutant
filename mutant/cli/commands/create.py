from sys import stderr
from pathlib import Path
from mutant.directory.manager import MutantDirectory

def main(args):
	directory = Path(args.directory)
	if directory.exists():
		print(f'Error: file({args.directory}) exists', file=stderr)
		return 1
	mutant_dir = MutantDirectory.create(directory)
	return 0
