import pytest
from pathlib import Path
from mutant.cli.parser import main_parser
from mutant.cli import run_command
from mutant.cli import commands

class TestCli:
	def test_main_parser_command_create(self):
		args = main_parser.parse_args(['create', 'dotfiles'])
		assert args.command_name == 'create'
		assert args.command_func == commands.create
		assert args.directory == Path('dotfiles')

	def test_command_create(self, tmp_path, monkeypatch):
		monkeypatch.chdir(tmp_path)
		run_command(['create', 'dotfiles'])
		assert Path('dotfiles').is_dir()

	def test_get_mutant_dir(self, tmp_path, monkeypatch):
		monkeypatch.chdir(tmp_path)
		run_command(['create', 'dotfiles'])
		monkeypatch.chdir(tmp_path.joinpath('dotfiles/config'))
		args = main_parser.parse_args(['clone'])
		assert args.get_mutant_dir().resolve() == Path('..').resolve()
