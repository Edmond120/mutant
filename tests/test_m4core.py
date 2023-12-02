import resource
from pathlib import Path
from mutant import m4core
from mutant.exceptions import M4Error

class TestM4core:
	sample_preclude = "hello world\n"

	sample_input = '\n'.join((
		"define(`swap', `$2 $1')dnl",
		"swap(`two', `one')",
		"swap(`four', `three')",
		"swap(`six', `five')",
	))

	sample_correct_output = '\n'.join((
		'hello world',
		'one two',
		'three four',
		'five six',
	))

	def test_M4_pipe(self):
		m4 = m4core.M4(preclude=self.sample_preclude)
		output_str = m4.pipe(self.sample_input)
		assert output_str == self.sample_correct_output

	def test_M4_pipe_file(self, tmp_path):
		test_file = tmp_path.joinpath('test.m4')
		with open(test_file, 'w') as file:
			file.write(self.sample_input)
		m4 = m4core.M4(preclude=self.sample_preclude)
		output_str = m4.pipe_file(test_file)
		assert output_str == self.sample_correct_output

	def test_M4_extend_flags(self):
		m4 = m4core.M4()
		flags = [ '--define=one=1', '--define=two=2' ]
		m4.flags.extend(flags)
		assert m4.flags == list(m4core.M4.default_flags) + flags
		assert m4.pipe(self.sample_input) == '\n'.join((
			'1 2',
			'three four',
			'five six',
		))

	def test_M4_include_path(self):
		m4 = m4core.M4()
		input_str = "include(`mutant_core.m4')"
		assert m4.pipe(input_str) == ''

	def test_M4_rlimits(self):
		limit = resource.getrlimit(resource.RLIMIT_STACK)
		softlimit = 1024 * 1024 * 7 if limit[0] == resource.RLIM_INFINITY else limit[0] - 1
		rlimits = (
			(resource.RLIMIT_STACK, softlimit),
		)
		m4 = m4core.M4(rlimits=rlimits)
		input_str = f'syscmd(python -c "import resource; print(resource.getrlimit(\"resource.RLIMIT_STACK\")[0])")'
		assert m4.pipe(input_str) == f'{softlimit}\n'

	def test_M4_fatal_warnings(self):
		m4 = m4core.M4()
		input_str = "include(`file_that_does_not_exist.txt')"
		try:
			m4.pipe(input_str)
			assert False
		except M4Error:
			pass

	def test_M4_pipe_get_stderr(self):
		m4 = m4core.M4()
		input_str = "syscmd(`echo this is stderr >&2')"
		stderr = m4.pipe(input_str, stdout_only=False)[1]
		assert stderr == 'this is stderr\n'

	def test_M4_file_relative_cwd(self):
		m4 = m4core.M4()
		testfile = Path('testdata/files/relative_cwd.m4')
		assert m4.pipe_file(testfile) == "hello world\n"
