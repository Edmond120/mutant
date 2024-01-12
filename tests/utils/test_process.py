import shutil
import resource
from mutant.utils.process import LimitedProcess
from mutant.exceptions import LimitExceededError

class TestProcess:
	def test_limited_process_run(self):
		args = (
			shutil.which('python'),
			'-c',
			'from resource import *; print(getrlimit(RLIMIT_DATA))',
		)
		lp = LimitedProcess(args)
		lp.start()
		assert lp.stdout == '(-1, -1)\n'
		assert lp.stderr == ''
		assert lp.returncode == 0
		assert isinstance(lp.pid, int)
		assert len(lp.errors) == 0

	def test_limited_process_rlimit(self):
		args = (
			shutil.which('python'),
			'-c',
			'from resource import *; print(getrlimit(RLIMIT_DATA))',
		)
		data_soft_limit = 512 * 1024 ** 2
		lp = LimitedProcess(
			args,
			rlimits=(
				(resource.RLIMIT_DATA, data_soft_limit),
			)
		)
		lp.start()
		assert lp.stdout == f'({data_soft_limit}, -1)\n'
		assert lp.stderr == ''

	def test_limited_process_rlimit_capped(self):
		"""
		Should set softlimit to hardlimit if target softlimit
		is greater than the hardlimit.
		"""
		args = (
			shutil.which('python'),
			'-c',
			'from resource import *; print(getrlimit(RLIMIT_NOFILE))',
		)
		data_soft_limit = resource.RLIM_INFINITY
		lp = LimitedProcess(
			args,
			rlimits=(
				(resource.RLIMIT_NOFILE, data_soft_limit),
			)
		)
		hardlimit = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
		if hardlimit != resource.RLIM_INFINITY or hardlimit > 2048:
			hardlimit = 2048
			resource.setrlimit(resource.RLIMIT_NOFILE, (2048, 2048))
		lp.start()
		assert lp.stdout == f'({hardlimit}, {hardlimit})\n'
		assert lp.stderr == ''

	def test_limited_process_stdin(self):
		args = (
			shutil.which('python'),
			'-c',
			'print(input().upper())',
		)
		input_string = 'hello world'
		lp = LimitedProcess(args, stdin=input_string)
		lp.start()
		assert lp.stdout == 'HELLO WORLD\n'
		assert lp.stderr == ''

	def test_limited_process_broken_pipe(self):
		# Deprecated test
		# There is no guarantee that this setup will cause a
		# broken pipe error in every environment.
		args = (
			shutil.which('true'),
		)
		input_string = 'hello world'
		lp = LimitedProcess(args, stdin=input_string)
		try:
			lp.start()
			# assert False
		except BrokenPipeError:
			pass
		assert lp.stdout == ''
		assert lp.stderr == ''

	def test_limited_process_output_limit(self):
		args = ( shutil.which('cat'), )
		input_string = '\n'.join(( str(n) * 4 for n in range(10)))
		lp = LimitedProcess(
			args,
			stdin=input_string,
			output_limits=( 25, -1 )
		)
		try:
			lp.start() # should throw error
			assert False
		except LimitExceededError:
			assert lp.stdout == input_string[:25]
			assert lp.stderr == ''

		lp2 = LimitedProcess(
			args,
			stdin=input_string,
			output_limits=( -1, 1 )
		)
		lp2.start()
		assert lp2.stdout == input_string
		assert lp2.stderr == ''

		lp3_args = (
			shutil.which('sh'),
			'-c',
			'cat >&2',
		)
		lp3 = LimitedProcess(
			lp3_args,
			stdin=input_string,
			output_limits=( -1, 25 )
		)
		try:
			lp3.start() # should throw error
			assert False
		except LimitExceededError:
			assert lp3.stderr == input_string[:25]
			assert lp3.stdout == ''
