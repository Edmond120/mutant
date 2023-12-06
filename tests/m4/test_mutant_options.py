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
			define(`two', `TWO')dnl
			option(`myoption', ```one''')
			changequote(`[',`]')dnl
			option([myoption], [`two'])
			option([myoption], [[two]])
			option([myotheroption], [`three'])
		"""
		output_str = """
			`one'
			`TWO'
			two
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

	def test_option_recursive(self):
		input_str = """
		namespaceimport(`mutant_options.m4', `*')dnl
		define(`option[0]', `alternative(ls,eza)')dnl
		option(
			`alternative(ls,exa)', `alias ls=exa',
			`alternative(ls,eza)', `alias ls=eza',
			`alternative(ls,lsd)', `alias ls=lsd',
			`default')
		"""
		output_str = """
			alias ls=eza
		"""
		assert self.m4_match(input_str, output_str)
