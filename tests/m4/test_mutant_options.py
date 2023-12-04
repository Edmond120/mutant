from testlib import M4Tester

class TestMutantOptions(M4Tester):
	include_file = 'mutant_options.m4'

	def test_option(self):
		input_str = """
			namespaceimport(`mutant_options.m4', `*')dnl
			define(`option[0]', `myoption')dnl
			define(`option[1]', `myotheroption')dnl
			define(`fish', `hello')dnl
			option(`myoption', `fish world')
			option(`notmyoption', `', ``not fish world'')
			option(`myotheroption', `one')
		"""
		output_str = """
			hello world
			not fish world
			one
		"""
		assert self.m4_match(input_str, output_str)

	def test_option_different_quotes(self):
		input_str = """
			namespaceimport(`mutant_options.m4', `*')dnl
			define(`option[0]', `myoption')dnl
			define(`option[1]', `myotheroption')dnl
			define(`two', `three')dnl
			changequote(`[',`]')dnl
			option([myoption], [`one'])
			option([myotheroption], [`two'])
		"""
		output_str = """
			`one'
			`three'
		"""
		assert self.m4_match(input_str, output_str)

	def test_option_do_not_handle_equal_sign(self):
		input_str = """
			namespaceimport(`mutant_options.m4', `*')dnl
			define(`option[0]', `foo=bar')dnl
			define(`option[1]', `myoption')dnl
			option(`foo=bar', `hello world')
			option(`myoption', `fish')
		"""
		output_str = """
			hello world
			fish
		"""
		assert self.m4_match(input_str, output_str)
