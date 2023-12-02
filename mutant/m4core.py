"""
Module for interacting with m4
"""

import subprocess
import resource
import shutil
import mutant.paths
from mutant.utils.process import LimitedProcess
from mutant.exceptions import M4Error

def _megabytes(n):
	return int(n * 1024 ** 2)

def _kilobytes(n):
	return int(n * 1024)

class M4:
	"""
	Wrapper class for running m4.

	The instance variables listed below are just lists and are
	safe to modify using functions that are not part of this class.

	Instance variables:
		flags:
			List of strings that will be passed as arguments to m4.
		rlimits:
			List of tuples that are in the form of (RLIMIT, VALUE).
			RLIMIT is a resource type from the "resource" module
			of the standard python library.
			VALUE represents the soft limit that will be set for
			m4.
		preclude:
			string that is prepended to what is piped to m4.
	"""

	default_flags = (
		'--nesting-limit=1024',
		f'--include={mutant.paths.data_dir.joinpath("m4")}',
		'--fatal-warnings', # two fatal warnings means to stop execution
		'--fatal-warnings', # at the first error
	)

	default_rlimits = (
		(resource.RLIMIT_DATA,  _megabytes(512)),
		(resource.RLIMIT_STACK, _kilobytes(8192)),
	)

	def __init__(self, *, flags=default_flags, rlimits=default_rlimits,
			size_limit=(-1, -1), preclude=''):
		self.flags = list(flags)
		self.rlimits = list(rlimits)
		self.size_limit = size_limit
		self.preclude = preclude

	def __pipe(self, string, *, cwd=None):
		"""
		Pipes a string through m4 and returns the output.
		"""
		args = [ shutil.which('m4') ]
		args.extend(self.flags)
		process = LimitedProcess(
			args,
			rlimits = self.rlimits,
			stdin = string,
			output_limits = self.size_limit,
			cwd = cwd,
		)
		process.start()
		if process.returncode != 0:
			raise M4Error('\n'.join((
				f'm4 returncode: {process.returncode}',
				f'm4 stderr: {process.stderr}',
			)))
		return (process.stdout, process.stderr)

	def pipe(self, string, *, stdout_only=True, cwd=None):
		string = self.preclude + string
		if stdout_only:
			return self.__pipe(string, cwd=cwd)[0]
		else:
			return self.__pipe(string, cwd=cwd)

	def pipe_file(self, path):
		"""
		Pipes a file through m4 and returns the output.

		Arguments:
			path: string that is the path to a file.
		"""
		with open(path, 'r') as file:
			return self.pipe(file.read(), cwd=path.parent)
