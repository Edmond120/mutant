import pytest
import shutil
import pathlib
import subprocess

def init_git_repo(path):
	commands = (
		('git', 'init'),
		('git', 'add', '-A'),
		('git', 'commit', '-m', 'First commit'),
	)
	for command in commands:
		subprocess.run(command, cwd=path)

@pytest.fixture()
def testdir(tmp_path, monkeypatch):
	"""
	Copies testdata/ into a temporary directory and initializes
	git repos as necessary.

	Tests that request this fixture will have their current
	working directory changed to the newly created temporary
	directory.
	"""
	testdata = pathlib.Path('testdata')
	for item in testdata.iterdir():
		shutil.copytree(item, tmp_path.joinpath(item.name))

	dotfiles_config = tmp_path.joinpath('dotfiles/config')
	init_git_repo(dotfiles_config)

	for repo in tmp_path.joinpath('repos').iterdir():
		init_git_repo(repo)

	monkeypatch.chdir(tmp_path)
	return tmp_path

@pytest.fixture()
def repo_names():
	return ( 'zsh', )
