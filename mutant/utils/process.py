import subprocess
import resource
import threading
from mutant.exceptions import LimitExceededError
from mutant.exceptions import LPBrokenPipeError

class LimitedProcess:
	"""
	Class that lets you create a process with specific resource
	limits.
	Instance variable "rlimit" is safe to modify.
	Format is the same as the instance variable
	mutant.m4core.M4.rlimits. (RLIMIT, VALUE)

	The instance variable "errors" is a list that contains all
	errors that are caught during process execution.

	This are all the possible errors that can appear in the list:
		LPBrokenPipeError
		LimitExceededError
	"""

	def __init__(self, args, *, rlimits=(), stdin=None, output_limits=(-1, -1), cwd=None):
		"""
		Arguments:
			args: iterable of strings
			rlimits: (RLIMIT, VALUE)
			output_limits: (STDOUT_BYTES, STDERR_BYTES)
			stdin: string

		If STDOUT_BYTES or STDERR_BYTES is -1 then that means no limit.
		If the output of the process exceeds output_limits then the process
		will be terminated and LimitExceededError will be placed into
		self.errors.
		"""
		self.args = args
		self.rlimits = []
		self.rlimits.extend(rlimits)
		self.stdout_limit = output_limits[0]
		self.stderr_limit = output_limits[1]
		self.stdin = stdin
		self.stdout = None
		self.stderr = None
		self.pid = None
		self.returncode = None
		self.errors = []
		self.cwd = cwd

	def start(self):
		process = subprocess.Popen(
			self.args,
			stdin=subprocess.PIPE if self.stdin else None,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True,
			preexec_fn=lambda: self._set_limits(),
			cwd=self.cwd,
		)
		self.pid = process.pid
		self._communicate(process)
		if self.errors:
			raise self.errors[0]
		process.wait()
		self.returncode = process.returncode

	def _communicate(self, process):
		"""
		Protected method that pipes in input and collects the output
		from the argument "process" and sets self.stdout and
		self.stderr.
		"""
		thread_functions = [
			self.__thread_stdout_read,
			self.__thread_stderr_read,
		]
		if self.stdin:
			thread_functions.append(self.__thread_stdin_write)
		threads = []

		for function in thread_functions:
			thread = threading.Thread(
				target=function,
				args=(process,),
			)
			thread.start()
			threads.append(thread)

		for thread in threads:
			thread.join()

	def __thread_stdin_write(self, process):
		try:
			process.stdin.write(self.stdin)
			process.stdin.close()
		except BrokenPipeError as e:
			self.errors.append(LPBrokenPipeError('LimitedProcess pipe broken'))

	def __thread_stdout_read(self, process):
		self.stdout = process.stdout.read(self.stdout_limit)
		if process.stdout.read(1):
			process.terminate()
			message = 'stdout output is too long'
			self.errors.append(LimitExceededError(message))
		process.stdout.close()

	def __thread_stderr_read(self, process):
		self.stderr = process.stderr.read(self.stderr_limit)
		if process.stderr.read(1):
			process.terminate()
			message = 'stderr output is too long'
			self.errors.append(LimitExceededError(message))
		process.stderr.close()

	def _set_limits(self): #pragma: nocover
		"""
		Protected method for setting rlimit.
		This method is the keyword argument "preexec_fn" of
		subprocess.Popen.
		"""
		for rlimit, softlimit in self.rlimits:
			hardlimit = resource.getrlimit(rlimit)[1]
			if hardlimit == resource.RLIM_INFINITY:
				resource.setrlimit(rlimit, (softlimit, hardlimit))
			elif softlimit == resource.RLIM_INFINITY:
				resource.setrlimit(rlimit, (hardlimit, hardlimit))
			elif softlimit <= hardlimit:
				resource.setrlimit(rlimit, (softlimit, hardlimit))
			else:
				resource.setrlimit(rlimit, (hardlimit, hardlimit))
