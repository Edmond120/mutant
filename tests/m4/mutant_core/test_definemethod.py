from .core_tester import MutantCoreTester

class TestMutantCoreDefinemethod(MutantCoreTester):
	include_file = 'definemethod.m4'

	def test_definemethod(self):
		input_str = """
			definemethod(`mymethod', `
				this output should not appear
				print(`Yes this is m4')
				this output should not appear
			')dnl
			mymethod
		"""
		output_str = """
		Yes this is m4
		"""
		assert self.m4_match(input_str, output_str)

	def test_definemethod_printnl(self):
		input_str = """
			definemethod(`mymethod', `
				printnl(`hello world')
			')dnl
			mymethod()dnl
		"""
		output_str = """
			hello world
		"""
		assert self.m4_match(input_str, output_str)

	def test_definemethod_example(self):
		input_str = """
			definemethod(`loop123', `
				ifelse(eval(`$1 > 0'), 1, `
					print(`$1,loop123(eval(`$1 - 1'))')
				')
			')dnl
			loop123(10)
		"""
		output_str = """
			10,9,8,7,6,5,4,3,2,1,
		"""
		assert self.m4_match(input_str, output_str)
