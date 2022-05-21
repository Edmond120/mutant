"""
Module for interacting with m4
"""

import subprocess

class M4:
	def pipe(self, string):
		"""
		Pipes a string through m4 and returns the output.
		"""
		args = ('m4',)
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
