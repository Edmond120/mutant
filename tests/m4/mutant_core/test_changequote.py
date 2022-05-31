from .core_tester import MutantCoreTester

class TestMutantCoreChangequote(MutantCoreTester):
	include_file = 'changequote.m4'

	def test_changequote(self):
		input_str = """
			define(`test', ``double quoted'')dnl
			test
			changequote(`[',`]')dnl
			test
			[test]
		"""
		correct_output = """
			double quoted
			`double quoted'
			test
		"""
		assert self.m4_match(input_str, correct_output)

	def test_defaultquote(self):
		input_str = """
			define(`test')dnl
			changequote(`[',`]')dnl
			[test]
			defaultquote`'dnl
			`test'
		"""
		correct_output = """
			test
			test
		"""
		assert self.m4_match(input_str, correct_output)

	def test_restorequote(self):
		input_str = """
			define(`test', ``double quoted'')dnl
			changequote(`[',`]')dnl
			test
			restorequote`'dnl
			test
		"""
		correct_output = """
			`double quoted'
			double quoted
		"""
		assert self.m4_match(input_str, correct_output)

	def test_quotestack(self):
		input_str = """
			define(`test_default_quote', ``double quoted'')dnl
			define(`test_bracket_quote', `[double quoted]')dnl
			define(`test_triangle_quote', `<double quoted>')dnl
			test_default_quote
			changequote(`[',`]')dnl
			test_bracket_quote
			changequote([<],[>])dnl
			test_triangle_quote
			restorequote()dnl
			test_bracket_quote
			restorequote()dnl
			test_default_quote
		"""
		correct_output = """
			double quoted
			double quoted
			double quoted
			double quoted
			double quoted
		"""
		assert self.m4_match(input_str, correct_output)
