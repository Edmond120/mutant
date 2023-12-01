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

	def test_mutant_directory_wrapper_clone_repos(self, create_testdir, monkeypatch):
		testdir = create_testdir('clone')
		monkeypatch.chdir(testdir)
		mutant_dir_path = testdir.joinpath('dotfiles')
		mutant_dir = MutantDirectory(mutant_dir_path)
		mutant_dir.clone_repos()
		cloned_repos = set(mutant_dir_path.joinpath('repos').iterdir())
		repo_names = (
			'zsh',
		)
		for name in repo_names:
			repo = mutant_dir.path.joinpath('repos', name)
			assert repo in cloned_repos

	def test_mutant_directory_wrapper_create_mutation(self, tmp_path):
		mutant_dir = MutantDirectory.create(tmp_path.joinpath('dotfiles'))
		mutant_dir.create_mutation('my_config_repo')
		repo = mutant_dir.path.joinpath('repos/my_config_repo')
		assert repo.joinpath('resources').is_dir()
		assert repo.joinpath('src').is_dir()
		assert repo.joinpath('provides.m4').is_file()
		assert repo.joinpath('.git').is_dir()
