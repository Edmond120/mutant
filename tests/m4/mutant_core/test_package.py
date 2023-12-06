from testlib import MutantCoreTester

class TestMutantPackage(MutantCoreTester):
	include_file = 'package.m4'

	def test_m4globalpackage(self):
		input_str = """
			m4globalpackage(`mypackage', `
				# everything should be diverted
				define(`test_success', `true')
			')dnl
			m4globalpackage(`mypackage', `
				# mypackage is already defined
				# everything here should be ignored
				define(`test_success', `false')
			')dnl
			test_success
			ifdef(`@include[mypackage]', `included')
		"""
		output_str = """
			true
			included
		"""
		assert self.m4_match(input_str, output_str)

	def test_m4package(self):
		input_str = """
			m4package(`mypackage', `
				namespacedef(`test_success', `true')
			')dnl
			ifelse(defn(`@thisnamespace'), `', `global')
			m4package(`mypackage', `
				namespacedef(`test_success', `false')
			')dnl
			ifelse(defn(`@thisnamespace'), `', `global')
			enternamespace(`mypackage')dnl
			test_success
		"""
		output_str = """
			global
			global
			true
		"""
		assert self.m4_match(input_str, output_str)
