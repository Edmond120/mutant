from testlib import MutantCoreTester
from mutant.exceptions import M4Error

class TestMutantCoreNamespace(MutantCoreTester):
	include_file = 'namespace.m4'

	def test_namespacedef(self):
		input_str = """
		namespacedef(`testspace', `greeting', `hello world')dnl
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

	def test_namespacedef_when_in_namespace(self):
		input_str = """
		namespacedef(`testspace', `greeting', `hello world')dnl
		greeting
		pushdef(`@thisnamespace', `arcade')dnl
		namespacedef(`arcade', `ping', `pong')dnl
		ping
		"""
		correct_output = """
		greeting
		pong
		"""
		assert self.m4_match(input_str, correct_output)

	def test_namespacedef_fail_empty_namespace(self):
		input_str = """
		namespacedef(`', `greeting', `hello world')dnl
		"""
		assert self.m4_fail(input_str)

	def test_namespacedef_fail_empty_macroname(self):
		input_str = """
		namespacedef(`testspace', `', `hello world')dnl
		"""
		assert self.m4_fail(input_str)

	def test_namespacemethod(self):
		input_str = """
		namespacemethod(`testspace', `greeting', `
		# comments will not show up
		pushdef(`output', `hello world')
		print(output)
		popdef(`output')
		')dnl
		define(`greet', defn(`@namespace[testspace]:greeting'))dnl
		greet
		"""
		correct_output = """
		hello world
		"""
		assert self.m4_match(input_str, correct_output)

	def test_enternamespace(self):
		input_str = """
		define(`@namespace[testspace]', `1')dnl
		define(`@namespace[testspace][1]', `greeting')dnl
		define(`@namespace[testspace]:greeting', `hello world')dnl
		enternamespace(`testspace')dnl
		greeting
		"""
		correct_output = """
		hello world
		"""
		assert self.m4_match(input_str, correct_output)

	def test_enternamespace_do_nothing(self):
		input_str = "enternamespace(`')"
		correct_output = ""
		assert(self.m4_match(input_str, correct_output))

	def test_enternamespace_do_not_enter_twice(self):
		input_str = """
		define(`@namespace[testspace]', `1')dnl
		define(`@namespace[testspace][1]', `greeting')dnl
		define(`@namespace[testspace]:greeting', `hello world')dnl
		enternamespace(`testspace')dnl
		enternamespace(`testspace')dnl
		popdef(`greeting')dnl
		greeting
		"""
		correct_output = """
		greeting
		"""
		assert self.m4_match(input_str, correct_output)

	def test_enternamespace_switch_namespaces(self):
		input_str = """
		define(`@namespace[A]', `2')dnl
		define(`@namespace[A][1]', `word')dnl
		define(`@namespace[A][2]', `A_ONLY')dnl
		define(`@namespace[A]:word', `tree')dnl
		define(`@namespace[A]:A_ONLY', `EXPANDED')dnl
		dnl
		define(`@namespace[B]', `1')dnl
		define(`@namespace[B][1]', `word')dnl
		define(`@namespace[B]:word', `grass')dnl
		dnl
		word
		enternamespace(`A')dnl
		word
		A_ONLY
		enternamespace(`B')dnl
		word
		A_ONLY
		"""
		correct_output = """
		word
		tree
		EXPANDED
		grass
		A_ONLY
		"""
		assert self.m4_match(input_str, correct_output)

	def test_enternamespace_return_to_global(self):
		input_str = """
		define(`@namespace[testspace]', `1')dnl
		define(`@namespace[testspace][1]', `greeting')dnl
		define(`@namespace[testspace]:greeting', `hello world')dnl
		greeting
		enternamespace(`testspace')dnl
		greeting
		enternamespace(`')dnl
		greeting
		"""
		correct_output = """
		greeting
		hello world
		greeting
		"""
		assert self.m4_match(input_str, correct_output)

	def test_enternamespace_fail_unknown_namespace(self):
		input_str = """
		enternamespace(`not_created')dnl
		"""
		assert self.m4_fail(input_str)

	def test_enternamespace_fail_too_many_args(self):
		input_str = """
		define(`@namespace[testspace]', `1')dnl
		define(`@namespace[testspace][1]', `greeting')dnl
		define(`@namespace[testspace]:greeting', `hello world')dnl
		enternamespace(`testspace', 0)dnl
		"""
		assert self.m4_fail(input_str)

	def test_leavenamespace(self):
		input_str = """
		define(`@namespace[testspace]', `1')dnl
		define(`@namespace[testspace][1]', `greeting')dnl
		define(`@namespace[testspace]:greeting', `hello world')dnl
		enternamespace(`testspace')dnl
		greeting
		leavenamespace`'dnl
		greeting
		"""
		correct_output = """
		hello world
		greeting
		"""
		assert self.m4_match(input_str, correct_output)

	def test_leavenamespace_do_nothing(self):
		input_str = "enternamespace()leavenamespace()defn(`leavenamespace')"
		correct_output = ""
		assert self.m4_match(input_str, correct_output)

	def test_leavenamespace_multilayer(self):
		input_str = """
		define(`@namespace[A]', `2')dnl
		define(`@namespace[A][1]', `word')dnl
		define(`@namespace[A][2]', `A_ONLY')dnl
		define(`@namespace[A]:word', `tree')dnl
		define(`@namespace[A]:A_ONLY', `EXPANDED')dnl
		dnl
		define(`@namespace[B]', `1')dnl
		define(`@namespace[B][1]', `word')dnl
		define(`@namespace[B]:word', `grass')dnl
		dnl
		word
		# entering A
		enternamespace(`A')dnl
		word
		A_ONLY
		# entering B
		enternamespace(`B')dnl
		word
		A_ONLY
		# entering B again
		enternamespace(`B')dnl
		word
		A_ONLY
		# leaving B, returning to B
		leavenamespace`'dnl
		word
		A_ONLY
		# leaving B, returning to A
		leavenamespace`'dnl
		word
		A_ONLY
		# leaving A, returning to global
		leavenamespace`'dnl
		word
		A_ONLY
		"""
		correct_output = """
		word
		# entering A
		tree
		EXPANDED
		# entering B
		grass
		A_ONLY
		# entering B again
		grass
		A_ONLY
		# leaving B, returning to B
		grass
		A_ONLY
		# leaving B, returning to A
		tree
		EXPANDED
		# leaving A, returning to global
		word
		A_ONLY
		"""
		assert self.m4_match(input_str, correct_output)

	def test_leavenamespace_leaving_global(self):
		input_str = """
		define(`@namespace[testspace]', `1')dnl
		define(`@namespace[testspace][1]', `greeting')dnl
		define(`@namespace[testspace]:greeting', `hello world')dnl
		enternamespace(`testspace')dnl
		enternamespace(`')dnl
		leavenamespace`'dnl
		greeting
		"""
		correct_output = """
		hello world
		"""
		assert self.m4_match(input_str, correct_output)

	def test_namespace_reentry(self):
		input_str = """
		namespacemethod(`testspace', `greeting', `
			print(`hello world')
		')dnl
		greeting
		fishing
		enternamespace(`testspace')dnl
		greeting
		namespacedef(`testspace', `fishing', `tuna')dnl
		fishing
		leavenamespace`'dnl
		enternamespace(`testspace')dnl
		greeting
		fishing
		"""
		correct_output = """
		greeting
		fishing
		hello world
		tuna
		hello world
		tuna
		"""
		assert self.m4_match(input_str, correct_output)
