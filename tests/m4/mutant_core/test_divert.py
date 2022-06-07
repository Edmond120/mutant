from testlib import MutantCoreTester

class TestMutantCoreDivert(MutantCoreTester):
	include_file = 'divert.m4'

	def test_divert(self):
		input_str = """
			should appear
			divert(-1)
			should not appear
		"""
		correct_output = "should appear\n"
		assert self.m4_match(input_str, correct_output)

	def test_restoredivert(self):
		input_str = """
			should appear
			divert(-1)
			should not appear
			restoredivert()dnl
			restored
		"""
		correct_output = "should appear\nrestored\n"
		assert self.m4_match(input_str, correct_output)

	def test_divertstack(self):
		input_str = """
			undiverted
			divert(5)dnl
			layer 5 front
			divert(4)dnl
			layer 4 front
			divert(3)dnl
			layer 3 front
			divert(2)dnl
			layer 2 front
			divert(1)dnl
			layer 1
			restoredivert()dnl
			layer 2 back
			restoredivert()dnl
			layer 3 back
			restoredivert()dnl
			layer 4 back
			restoredivert()dnl
			layer 5 back
		"""
		correct_output = """
			undiverted
			layer 1
			layer 2 front
			layer 2 back
			layer 3 front
			layer 3 back
			layer 4 front
			layer 4 back
			layer 5 front
			layer 5 back
		"""
		assert self.m4_match(input_str, correct_output)
