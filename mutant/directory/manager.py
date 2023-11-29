from mutant.directory import creator
from mutant.directory import parser

class MutantDirectory:
	"""
	A class where all interactions with a Mutant directory should be
	done through.
	"""

	@classmethod
	def create(cls, path):
		creator.create_mutant_dir(path)
		return cls(path)

	def __init__(self, path):
		self.path = path

		path_str = path.absolute().as_posix()
		if not path.exists():
			raise FileNotFoundError(f'Mutant directory not found: {path_str}')
		if not path.is_dir():
			raise NotADirectoryError(f'Error: {path_str} is not a directory')
