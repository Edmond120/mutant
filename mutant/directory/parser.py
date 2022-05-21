"""
Module for parsing files in a mutant directory.
"""

from mutant import m4core

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
