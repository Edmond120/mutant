from pathlib import Path
from mutant.directory import manager
from mutant.directory.manager import MutantDirectory

class TestManager:
	def test_new_manager(self, tmp_path):
		mutant_dir_path = tmp_path.joinpath('dotfiles')
		mutant_dir = MutantDirectory.create(mutant_dir_path)
		assert isinstance(mutant_dir, MutantDirectory)

	def test_new_manager_errors(self, tmp_path):
		mutant_dir_path = tmp_path.joinpath('dotfiles')
		try:
			MutantDirectory(mutant_dir_path)
			assert False
		except FileNotFoundError:
			pass

		mutant_dir_path.open(mode='w').close()
		try:
			MutantDirectory(mutant_dir_path)
			assert False
		except NotADirectoryError:
			pass

	def test_manager_wrapper_clone_repos(self, create_testdir):
		testdir = create_testdir('clone')
		mutant_dir_path = testdir.joinpath('dotfiles')
		mutant_dir = MutantDirectory(mutant_dir_path)
		mutant_dir.clone_repos()
		cloned_repos = set(mutant_dir_path.joinpath('repos').iterdir())
		repo_names = (
			'zsh',
		)
		for name in repo_names:
			repo = mutant_dir.path.joinpath('repos').joinpath(name)
			assert repo in cloned_repos
