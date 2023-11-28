"""
Module for parsing files in a mutant directory.
"""

import configparser
from mutant import m4core
from mutant.exceptions import ConfigFileError

def _get_valid_lines(data):
	return filter(
		lambda l: len(l) > 0 and l[0] != '#',
		map(lambda s: s.strip(), data.split('\n'))
	)

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
	m4 = m4core.M4(preclude="include(`mutant_core.m4')dnl")
	data = m4.pipe_file(path)

	options = []
	for line in _get_valid_lines(data):
		words = line.split()
		option = words[0]
		options.append(option)
	return options

def read_provides(path):
	"""
	Runs a provides.m4 file through m4 containing provide rules.
	Returns a list in the form of
		{
			'conditions': [<option>, ...],
			'provides': [<option>, ...]
		}
	Provide rules are in the form of "<options> -> <options>" where
	<options> are whitespace separated options. Options to the left
	are conditions where when satisfied will enable the options to
	the right. If there is no arrow then the options are assumed
	to be to the right of an arrow.

	Ex. one two -> three

	Arguments:
		path: a pathlib.Path object that represents a provides.m4 file.
	"""
	m4 = m4core.M4(preclude="include(`mutant_core.m4')dnl")
	data = m4.pipe_file(path)

	entries = []
	for line in _get_valid_lines(data):
		words = line.split()
		if '->' in words:
			arrow = words.index('->')
			conditions = words[:arrow]
			provides = words[arrow+1:]
			entries.append({
				'conditions' : conditions,
				'provides' : provides,
			})
		else:
			entries.append({
				'conditions' : [],
				'provides' : words
			})
	return entries

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
