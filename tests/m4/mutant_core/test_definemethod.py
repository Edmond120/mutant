from testlib import MutantCoreTester

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

	def test_definemethod_println(self):
		input_str = """
			definemethod(`mymethod', `
				println(`hello world')
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

	def test_definemethod_var_internal(self):
		input_str = """
		definemethod(`test', `
			var(`greeting', `hello world')
			format(
				`
				println(``%s'')
				println(``%s'')
				println(``%s'')
				println(``%s'')
				println(``%s'')
				',
				defn(`greeting'),
				defn(`@definemethod_layer'),
				defn(`@definemethod_var[1]'),
				defn(`@definemethod_var[1][1]'),
				defn(`@definemethod_var[1]:greeting'))
		')dnl
		test`'dnl
		"""
		output_str = """
		hello world
		1
		1
		greeting
		hello world
		"""
		assert self.m4_match(input_str, output_str)

	def test_definemethod_var(self):
		input_str = """
		definemethod(`first', `
			var(`greeting', ``hello world'')
			println(greeting)
			print(second)
			println(greeting)
		')dnl
		definemethod(`second', `
			println([defn(`greeting')]) # greeting should not be defined
			var(`greeting', ``HELLO WORLD'')
			println(greeting)
		')dnl
		first`'dnl
		"""
		output_str = """
		hello world
		[]
		HELLO WORLD
		hello world
		"""
		assert self.m4_match(input_str, output_str)

	def test_definemethod_nested_call(self):
		input_str = """
		definemethod(`first', `
			var(`one', `ONE')
			print(`layer 1')
		')dnl
		definemethod(`second', `
			println(one)
			var(`two', first)
			print(two)
		')dnl
		first
		second
		"""
		output_str = """
			layer 1
			one
			layer 1
		"""
		assert self.m4_match(input_str, output_str)
