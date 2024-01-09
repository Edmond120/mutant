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
