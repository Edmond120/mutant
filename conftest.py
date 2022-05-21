import pytest
import shutil
import pathlib
import subprocess
import mutant

def apply_overlay(overlay, target):
	if not ( overlay.exists() and target.exists() ):
		raise FileNotFoundError('unable to apply overlay')
	if overlay.is_dir():
		if not target.is_dir():
			raise NotADirectoryError('target is not a directory')
		for item in overlay.iterdir():
			apply_overlay(item, target.joinpath(item.name))
	else: # overlay is a file
		if not target.is_file():
			raise IsADirectoryError('target is not a file')
		shutil.copyfile(overlay, target)

def init_git_repo(path):
	commands = (
		('git', 'init'),
		('git', 'add', '-A'),
		('git', 'commit', '-m', 'First commit'),
	)
	for command in commands:
		subprocess.run(command, cwd=path)

def setup_repos(repos_path):
	for repo in repos_path.iterdir():
		init_git_repo(repo)

@pytest.fixture()
def create_testdir(tmp_path, monkeypatch):
	"""
	Creates a test mutant directory and overlays another
	directory tree on top of it.

	Tests that request this fixture will have their current
	working directory changed to the newly created temporary
	directory.
	"""
	def create_dir_func(overlay):
		overlay_dir = pathlib.Path('testdata/overlays').joinpath(overlay)
		dotfiles = tmp_path.joinpath('dotfiles')
		mutant.directory.creator.create_mutant_dir(dotfiles)

		apply_overlay(overlay_dir, tmp_path)
		tmp_repos_path = tmp_path.joinpath('repos')
		shutil.copytree(pathlib.Path('testdata/repos'), tmp_repos_path)
		setup_repos(tmp_repos_path)

		monkeypatch.chdir(tmp_path)
		return tmp_path
	return create_dir_func
