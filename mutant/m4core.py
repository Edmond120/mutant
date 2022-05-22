"""
Module for interacting with m4
"""

import subprocess

class M4:
	default_flags = (
		'--nesting-limit=1024',
	)

	def __init__(self, flags=default_flags):
		self.flags = list(flags)

	def append_flag(self, flag):
		self.flags.append(flag)

	def extend_flags(self, flags):
		for flag in flags:
			self.append_flag(flag)

	def pipe(self, string):
		"""
		Pipes a string through m4 and returns the output.
		"""
		args = ['m4']
		args.extend(self.flags)
		return subprocess.run(
			args,
			input=string,
			text=True,
			stdout=subprocess.PIPE,
		).stdout

	def pipe_file(self, path):
		"""
		Pipes a file through m4 and returns the output.

		Arguments:
			path: string that is the path to a file.
		"""
		with open(path, 'r') as file:
			return self.pipe(file.read())
