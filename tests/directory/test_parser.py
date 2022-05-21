import pytest
from pathlib import Path
from mutant.directory import parser

class TestParser:
	def test_read_options(self, create_testdir):
		tmpdir = create_testdir('parse_options')
		options_file = Path('dotfiles/config/options.m4')
		assert options_file.is_file()
		assert parser.read_options(options_file) == [
			'fish_1', 'fish_2', 'fish_3',
			'cats_1', 'cats_2', 'cats_3',
			'dogs_1', 'dogs_2', 'dogs_3',
		]
