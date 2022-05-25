import resource
from mutant import m4core
from mutant.exceptions import M4Error

class TestM4core:
	sample_input = '\n'.join((
		"define(`swap', `$2 $1')dnl",
		"swap(`two', `one')",
		"swap(`four', `three')",
		"swap(`six', `five')",
	))

	sample_correct_output = '\n'.join((
		'one two',
		'three four',
		'five six',
	))

	def test_M4_pipe(self):
		m4 = m4core.M4()
		output_str = m4.pipe(self.sample_input)
		assert output_str == self.sample_correct_output

	def test_M4_pipe_file(self, tmp_path):
		test_file = tmp_path.joinpath('test.m4')
		with open(test_file, 'w') as file:
			file.write(self.sample_input)
		m4 = m4core.M4()
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
		input_str = "include(`test.m4')`'TEST"
		assert m4.pipe(input_str) == 'true'

	def test_M4_rlimits(self):
		rlimits = (
			(resource.RLIMIT_STACK, 1024 * 8),
		)
		m4 = m4core.M4(rlimits=rlimits)
		input_str = 'hello world'
		try:
			m4.pipe(input_str)
			assert False
		except BrokenPipeError:
			pass

	def test_M4_fatal_warnings(self):
		m4 = m4core.M4()
		input_str = "include(`file_that_does_not_exist.txt')"
		try:
			m4.pipe(input_str)
			assert False
		except M4Error:
			pass
