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
