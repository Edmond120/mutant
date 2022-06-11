ifdef(`@include[mutant_core/definemethod.m4]', `', `dnl
define(`@include[mutant_core/definemethod.m4]')dnl
include(`mutant_core/changequote.m4')dnl
include(`mutant_core/divert.m4')dnl
divert(`-1')

# Variable to hold the output of a macro
define(`@macro_output')

define(`@print()', `changequote
	pushdef(`@temp', defn(`@macro_output'))
	popdef(`@macro_output')
	pushdef(`@macro_output', defn(`@temp')`$1')
	popdef(`@temp')
	restorequote()
')

define(`@println()', `changequote
	pushdef(`@temp', defn(`@macro_output'))
	popdef(`@macro_output')
	pushdef(`@macro_output', defn(`@temp')`$1
')
	popdef(`@temp')
	restorequote()
')

# Method specs
#   - Output is ignored except for first argument in print()
#   - Quotes are `'
#   - No unquoted dangling parentheses (due to implementation)
define(`definemethod', `changequote`'dnl
define(`$1', `changequote`'dnl
pushdef(`print', defn(`@print()'))dnl
pushdef(`println', defn(`@println()'))dnl
pushdef(`func', defn(`@method_return()'))dnl
pushdef(`@macro_output')dnl
func(popdef(`func')
$2
restorequote
)')dnl
restorequote()dnl
')

# Discard arguments and output @macro_output instead
define(`@method_return()', `changequote`'dnl
pushdef(`func', defn(`@macro_output'))dnl
func(
popdef(`func')
popdef(`@macro_output')
popdef(`print')
popdef(`println')
restorequote
)')


restoredivert()dnl
')dnl
