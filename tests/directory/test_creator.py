import configparser
from mutant.directory import creator

class TestCreator:
	def test_create_mutant_dir(self, tmp_path):
		mutant_dir = tmp_path.joinpath('dotfiles')
		creator.create_mutant_dir(mutant_dir)
		is_directory = lambda x: x.is_dir()
		is_file = lambda x: x.is_file()
		files = (
			( 'config'           , is_directory ),
			( 'config/.git'      , is_directory ),
			( 'config/repos'     , is_file      ),
			( 'config/options.m4', is_file      ),
			( 'repos'            , is_directory ),
			( 'stow'             , is_directory ),
			( 'build'            , is_directory ),
		)

		for path, test in files:
			assert test(mutant_dir.joinpath(path))

	def test_clone_repos(self, create_testdir):
		testdir = create_testdir('clone')
		dotfiles = testdir.joinpath('dotfiles')
		repos = dotfiles.joinpath('repos')
		creator.clone_repos(dotfiles)
		cloned_repos = set(dotfiles.joinpath('repos').iterdir())
		repo_names = (
			'zsh',
		)
		for name in repo_names:
			repo = repos.joinpath(name)
			assert repo in cloned_repos

	def helper_create_mutation_dir(self, mutation_dir, *, remote=''):
		if remote:
			creator.create_mutation_dir(mutation_dir, remote=remote)
		else:
			creator.create_mutation_dir(mutation_dir)
		is_directory = lambda x: x.is_dir()
		is_file = lambda x: x.is_file()
		files = (
			( '.git'      , is_directory ),
			( 'src'       , is_directory ),
			( 'resources' , is_directory ),
			( 'genes.conf', is_file      ),
		)

		for path, test in files:
			assert test(mutation_dir.joinpath(path))

	def test_create_mutation_dir(self, tmp_path):
		mutation_dir = tmp_path.joinpath('my_config_repo')
		self.helper_create_mutation_dir(mutation_dir)

	def test_create_mutation_dir__remote(self, tmp_path):
		mutation_dir = tmp_path.joinpath('my_config_repo')
		self.helper_create_mutation_dir(
			mutation_dir,
			remote='git@example.local',
		)
		git_config = configparser.ConfigParser()
		git_config.read(mutation_dir.joinpath('.git/config'))
		remote = git_config['remote "origin"']
		assert remote['url'] == 'git@example.local'
		assert remote['fetch'] == '+refs/heads/*:refs/remotes/origin/*'
