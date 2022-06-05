from mutant.m4core import M4
from mutant.exceptions import M4Error

class MutantCoreTester:
	"""
	Class for testing m4 files.
	M4 input and correct output  are formatted in a particular way
	to make it easier to encode as python strings.

	First and last lines are removed if they contain only whitespace.
	All left whitespace that present in each remaining lines are
	removed.
	"""
	include_file = ''

	@staticmethod
	def __uniform_list(lst):
		"checks if everything in the list is the same"
		if len(lst) < 2:
			return True
		for i in range(len(lst) - 1):
			if lst[i] != lst[i+1]:
				return False
		return True

	@classmethod
	def __get_include_str(cls):
		if isinstance(cls.include_file, str):
			return f"include(`mutant_core/{cls.include_file}')dnl\n"
		include_str = ''
		for file in cls.include_file:
			include_str += f"include(`mutant_core/{file}')dnl\n"
		return include_str

	@classmethod
	def format_str(cls, string):
		lines = string.split('\n')
		if len(lines) and not len(lines[0].lstrip()):
			lines.pop(0)
		if len(lines) and not len(lines[-1].lstrip()):
			lines.pop(-1)

		if len(lines) <= 1:
			line = '\n'.join(map(lambda s: s.lstrip(), lines))
			return line.rstrip() + '\n'

		left_shave = 0
		for i in range(min(map(len, lines))):
			left_shave = i
			lst = list(map(lambda l: l[i], lines))
			if any(map(lambda c: len(c.strip()), lst)):
				break
			if not cls.__uniform_list(lst):
				break

		for i in range(len(lines)):
			lines[i] = lines[i][left_shave:]

		lines = '\n'.join(lines)
		if len(lines):
			lines = lines.rstrip() + '\n'
		return lines

	@classmethod
	def m4_match(cls, input_str, correct_output):
		assert len(cls.include_file)
		input_str = cls.format_str(input_str)
		correct_output = cls.format_str(correct_output)
		include_str = cls.__get_include_str()
		input_str = include_str + input_str
		m4 = M4()
		output, stderr = m4.pipe(input_str, stdout_only=False)
		print(f'correct output: {correct_output}')
		print(f'output: {output}')
		print(f'stderr: {stderr}')
		return output == correct_output

	@classmethod
	def m4_fail(cls, input_str):
		assert len(cls.include_file)
		input_str = cls.format_str(input_str)
		include_str = cls.__get_include_str()
		input_str = include_str + input_str
		m4 = M4()
		try:
			m4.pipe(input_str, stdout_only=False)
			return False
		except M4Error:
			return True
