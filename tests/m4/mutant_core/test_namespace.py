from .core_tester import MutantCoreTester

class TestMutantCoreNamespace(MutantCoreTester):
	include_file = 'namespace.m4'

	def test_namespacemethod(self):
		input_str = """
		namespacemethod(`testspace', `greeting', `hello world')dnl
		defn(`@namespace[testspace]')
		defn(`@namespace[testspace][1]')
		defn(`@namespace[testspace]:greeting')
		"""
		correct_output = """
		1
		greeting
		hello world
		"""
		assert self.m4_match(input_str, correct_output)

	def test_namespacemethod_when_in_namespace(self):
		input_str = """
		namespacemethod(`testspace', `greeting', `hello world')dnl
		greeting
		pushdef(`@thisnamespace', `arcade')dnl
		namespacemethod(`arcade', `ping', `pong')dnl
		ping
		"""
		correct_output = """
		greeting
		pong
		"""
		assert self.m4_match(input_str, correct_output)

	def test_namespacemethod_fail_empty_namespace(self):
		input_str = """
		namespacemethod(`', `greeting', `hello world')dnl
		"""
		assert self.m4_fail(input_str)

	def test_namespacemethod_fail_empty_macroname(self):
		input_str = """
		namespacemethod(`testspace', `', `hello world')dnl
		"""
		assert self.m4_fail(input_str)
