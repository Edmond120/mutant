from pathlib import Path
from mutant.directory import parser
from mutant.exceptions import ConfigFileError

class TestParser:
	def test_read_options(self):
		options_file = Path('testdata/files/options.m4')
		assert options_file.is_file()
		assert parser.read_options(options_file) == [
			'fish_1', 'fish_2', 'fish_3',
			'cats_1', 'cats_2', 'cats_3',
			'dogs_1', 'dogs_2', 'dogs_3',
		]

	def test_read_provides(self):
		provides_file = Path('testdata/files/provides.m4')
		assert provides_file.is_file()
		assert parser.read_provides(provides_file) == [
			{
				'conditions' : ['one', 'two', 'three'],
				'provides' : ['four']
			},
			{
				'conditions' : ['five', 'six', 'seven'],
				'provides' : ['eight', 'nine'],
			},
			{
				'conditions' : [],
				'provides' : ['ten', 'eleven']
			}
		]

	def test_read_repos(self):
		repos_file = Path('testdata/files/config_repos')
		assert repos_file.is_file()
		assert parser.read_repos(repos_file) == [
			{
				'name': 'zsh',
				'url' : 'git@example.com:zsh_config',
			},
			{
				'name': 'bash',
				'url' : 'git@example.com:bash_config',
			},
		]

	def test_read_repos_fail(self, create_testdir):
		repos_file = Path('testdata/files/config_repos_invalid')
		assert repos_file.is_file()
		try:
			parser.read_repos(repos_file)
		except ConfigFileError:
			pass
