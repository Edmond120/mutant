import pathlib
import mutant.paths

class TestPaths:
	"""
	This class assumes that the module is not installed
	"""

	@staticmethod
	def is_paths_equal(a, b):
		a = a.resolve(strict=True)
		b = b.resolve(strict=True)
		return a == b

	def test_is_installed(self):
		assert mutant.paths.is_installed == False

	def test_module_dir(self):
		assert mutant.paths.module_dir.is_absolute()
		assert self.is_paths_equal(
			pathlib.Path('mutant'),
			mutant.paths.module_dir
		)

	def test_data_dir(self):
		assert mutant.paths.module_dir.is_absolute()
		assert self.is_paths_equal(
			pathlib.Path('data/m4'),
			mutant.paths.data_dir
		)
