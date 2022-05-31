ifdef(`@include[mutant_core/definemethod.m4]', `', `dnl
define(`@include[mutant_core/definemethod.m4]')dnl
include(`mutant_core/changequote.m4')dnl
include(`mutant_core/divert.m4')dnl
divert(`-1')

# Variable to hold the output of a macro
define(`@macro_output')

# Discard arguments and output @macro_output instead
define(`@print_based_output()', `changequote`'dnl
pushdef(`func', defn(`@macro_output'))dnl
func`'dnl
popdef(`func')dnl
popdef(`@macro_output')dnl
restorequote()dnl
')

define(`@print()', `changequote
	pushdef(`@temp', defn(`@macro_output'))
	popdef(`@macro_output')
	pushdef(`@macro_output', defn(`@temp')`$1')
	popdef(`@temp')
	restorequote()
')

define(`@printnl()', `changequote
	pushdef(`@temp', defn(`@macro_output'))
	popdef(`@macro_output')
	pushdef(`@macro_output', defn(`@temp')`$1
')
	restorequote
')

# Method specs
#   - Output is ignored except for first argument in print()
#   - Quotes are `'
#   - No unquoted dangling parentheses (due to implementation)
define(`definemethod', `changequote`'dnl
define(`$1', `changequote`'dnl
dnl
pushdef(`print', defn(`@print()'))dnl
pushdef(`printnl', defn(`@printnl()'))dnl
pushdef(`func', defn(`@print_based_output()'))dnl
pushdef(`@macro_output')dnl
func(popdef(`func')
$2
)dnl
popdef(`print')dnl
popdef(`printnl')dnl
dnl
restorequote()dnl
')dnl
restorequote()dnl
')

restoredivert()dnl
')dnl
