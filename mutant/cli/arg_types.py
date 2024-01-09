from pathlib import Path
from argparse import ArgumentTypeError
from mutant.directory.manager import MutantDirectory

def non_existent_file(string):
	path = Path(string)
	if path.exists():
		raise ArgumentTypeError(f'"{path}" exists')
	return path

def mutant_directory(string):
	path = Path(string)
	if path.is_dir() and path.joinpath('.mutant').is_file():
		return MutantDirectory(path)
	raise ArgumentTypeError(f'"{path}" is not a mutant directory')
