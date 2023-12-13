"""
Module for creating a mutant project directory.
"""
import subprocess
from mutant.directory import parser
from mutant.utils import git

def create_mutant_dir(path):
	"""
	Creates a mutant directory in the given path.

	A mutant directory is the main directory managed by mutant.
	It contains all your git repos.

	Arguments:
		path: a pathlib.Path object
	"""
	path.mkdir()
	mkdir = lambda p: p.mkdir()
	touch = lambda x: x.open('x').close()

	tasks = (
		( 'config'           , mkdir                ),
		( 'config/repos'     , _make_config_repos   ),
		( 'config/options.m4', _make_config_options ),
		( 'config'           , _to_repo             ),
		( 'repos'            , mkdir                ),
		( 'stow'             , mkdir                ),
		( 'build'            , mkdir                ),
		( '.mutant'          , touch                ),
	)

	for filename, func in tasks:
		func(path.joinpath(filename))

def _to_repo(repo_path, *, remote=''):
	repo = git.Repo(repo_path)
	repo.init()

	if remote:
		repo.remote_add('origin', remote)

def _make_config_repos(path):
	with path.open('x') as file:
		data = """
			# example
			# [my_git_repo]
			# url = git@mygitserver.com/my_git_repo
		"""
		data = map(lambda s: s.strip(), data.split('\n'))
		next(data)
		file.write('\n'.join(data))

def _make_config_options(path):
	with path.open('x') as file:
		data = """
			# Each option name is on a newline.
			# Whitespace act as delimiters.
			# This file will be run through m4.
			# One use of m4 is to get generate options
			# based on installed packages.
			# Ex. (for gentoo)
			#     syscmd(`qlist -I')
			# I perfer to prefix generated options.
			# Ex.
			#     syscmd(`qlist -I | sed "s/^/package:/"')
		"""
		data = map(lambda s: s.strip(), data.split('\n'))
		next(data)
		file.write('\n'.join(data))

def clone_repos(mutant_dir):
	"""
	Reads config/repos and clones all the repos that are not
	present in repos/.
	This function is expected to be used in a directory created
	by create().

	Arguments:
		mutant_dir: a pathlib.Path object
	"""
	repos = mutant_dir.joinpath('repos')
	repos_config_file = mutant_dir.joinpath('config/repos')
	repos_config = parser.read_repos(repos_config_file)

	for config in repos_config:
		if 'url' not in config:
			continue #pragma: nocover
		name = config['name']
		url = config['url']
		dest = repos.joinpath(name)
		if dest.exists():
			continue #pragma: nocover
		git.Repo.clone(url, dest)

def create_mutation_dir(path, *, remote=''):
	"""
	Creates a mutation directory in the given path.

	A program configuration aka "dotfile" repo managed by mutant is
	called a mutation.

	Arguments:
		path: a pathlib.Path object
		remote: upstream url for git repo
	"""
	path.mkdir()
	mkdir = lambda x: x.mkdir()
	touch = lambda x: x.open('x').close()
	to_repo = lambda x: _to_repo(x, remote=remote)

	tasks = (
		( 'provides.m4', touch   ),
		( 'src'        , mkdir   ),
		( 'resources'  , mkdir   ),
		( '.'          , to_repo ),
	)

	for filename, func in tasks:
		func(path.joinpath(filename))
