import pytest
from pathlib import Path
from mutant.cli.parser import main_parser
from mutant.cli import run_command
from mutant.cli import commands

class TestCli:
	def test_parser(self):
		args = main_parser.parse_args(['create', 'dotfiles'])
		assert args.command_name == 'create'
		assert args.command_func == commands.create
		assert args.directory == Path('dotfiles')

	def test_command_create(self, tmp_path, monkeypatch):
		monkeypatch.chdir(tmp_path)
		run_command(['create', 'dotfiles'])
		assert Path('dotfiles').is_dir()
