from pathlib import Path
from argparse import ArgumentTypeError

def non_existent_file(string):
	path = Path(string)
	if path.exists():
		raise ArgumentTypeError(f'"{path}" exists')
	return path
