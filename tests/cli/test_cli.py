import pytest
from pathlib import Path
from mutant.cli import run_command
from mutant.cli import commands

# For testing private functions
from mutant.cli import parser

class TestCli:
	def test_command_create(self, tmp_path, monkeypatch):
		monkeypatch.chdir(tmp_path)
		run_command(['create', 'dotfiles'])
		assert Path('dotfiles').is_dir()

	def test_command_create_fail(self, tmp_path, monkeypatch):
		monkeypatch.chdir(tmp_path)
		run_command(['create', 'dotfiles'])
		try:
			run_command(['create', 'dotfiles'])
			assert False
		except SystemExit:
			pass

	def test_command_clone(self, create_testdir, monkeypatch):
		testdir = create_testdir('repo_clone')
		monkeypatch.chdir(testdir)
		run_command(['--mutant-dir', 'dotfiles', 'clone'])
		assert testdir.joinpath('dotfiles', 'repos', 'zsh').is_dir()

	def test_command_clone_fail(self, create_testdir, monkeypatch):
		testdir = create_testdir('repo_clone')
		monkeypatch.chdir(testdir)
		try:
			run_command(['--mutant-dir', 'invalid_path', 'clone'])
			assert False
		except SystemExit:
			pass

class TestCliPrivate:
	def test_main_parser_command_create(self):
		args = parser.main_parser.parse_args(['create', 'dotfiles'])
		assert args.command_name == 'create'
		assert args.command_func == commands.create
		assert args.directory == Path('dotfiles')

	def test_get_mutant_directory(self, tmp_path, monkeypatch):
		monkeypatch.chdir(tmp_path)
		run_command(['create', 'dotfiles'])
		monkeypatch.chdir(tmp_path.joinpath('dotfiles/config'))
		assert parser._get_mutant_directory().path.resolve() == Path('..').resolve()
