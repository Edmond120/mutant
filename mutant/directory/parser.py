"""
Module for parsing files in a mutant directory.
"""

import configparser
from mutant import m4core
from mutant.exceptions import ConfigFileError

def read_options(path):
	"""
	Runs an options.m4 file through m4 and returns a list containing each
	option.

	Comments are lines starting with '#'.
	There can only be one option per line.
	Options must not contain whitespace.

	Arguments:
		path: a pathlib.Path object that represents an options.m4 file.
	"""
	m4 = m4core.M4()
	data = m4.pipe_file(path)

	lines = filter(len, map(lambda s: s.strip(), data.split('\n')))
	options = []
	for line in lines:
		if line[0] == '#':
			continue
		words = line.split()
		option = words[0]
		options.append(option)
	return options

def read_repos(path):
	"""
	Reads a repos file and returns a list of directories with values
	'name' and 'url'.

	The repos files is an ini file.

	Arguments:
		path: a pathlib.Path object that represents a repos file.
	"""
	config = configparser.ConfigParser()
	config.read(path)

	repos = []
	for section in config.sections():
		if 'url' not in config[section]:
			message = f'Url missing in repo config for: {section}'
			raise ConfigFileError(message)
		repos.append({
			'name': section,
			'url' : config[section]['url'],
		})
	return repos
