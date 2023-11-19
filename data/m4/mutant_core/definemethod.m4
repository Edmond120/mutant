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
	print(`$1
')restorequote()')

define(`@printq()', `changequote
	pushdef(`@temp', defn(`@macro_output'))
	popdef(`@macro_output')
	pushdef(`@macro_output',
		defn(`@temp')$`'1`$1'$`'2)
	popdef(`@temp')
	restorequote()
')

define(`@printqln()', `changequote
	printq(`$1
')restorequote()')

# variables used in @define_var
# -----------------------------
# arrays are indexed starting at 1
# @definemethod_layer = recursion depth
# @definemethod_var[<n>] = var_array length, n specifies array,
#                        arrays are created up to the recursion depth
# @definemethod_var[<n>][<m>] = var name, m is index
# @definemethod_var[<n>]:<name> = macro definition given name

define(`@definemethod_layer', 0)
define(`@definemethod_var[0]', 0)

define(`@define_var', `changequote
	ifelse(`$1', `', `
		errprint(`empty variable name for macro `var'')
		m4exit(1)
	')

	ifdef(
		format(``@definemethod_var[%d]:%s'',
			defn(`@definemethod_layer'),
			`$1'),
		`
		# if variable is already defined
		define(
			format(``@definemethod_var[%d]:%s'',
				defn(`@definemethod_layer'),
				`$1'),
			`$2')
		popdef(`$1')
		pushdef(`$1', `$2')
		',`
		# if variable is undefined
		pushdef(`array',
			format(``@definemethod_var[%s]'',
				defn(`@definemethod_layer')))
		pushdef(`length', defn(defn(`array')))
		pushdef(`index', eval(defn(`length') + 1))
		pushdef(`varname', format(``%s[%d]'', defn(`array'), index))
		pushdef(`vardef', format(``%s:%s'', defn(`array'), `$1'))
		define(defn(`array'), index)
		define(defn(`varname'), `$1')
		define(defn(`vardef'), `$2')

		popdef(`vardef')
		popdef(`varname')
		popdef(`index')
		popdef(`length')
		popdef(`array')

		pushdef(`$1', `$2')
	')
	restorequote
')

# Method specs
#   - Output is ignored except for first argument in print()
#   - Quotes are `'
#   - No unquoted dangling parentheses (due to implementation)
#   - Print buffer is a macro and will be called with args 1 & 2
#     being the start and end quotes of the scope where the method
#     is called.
define(`definemethod', `changequote`'dnl
define(`$1', `changequote`'dnl
pushdef(`print', defn(`@print()'))dnl
pushdef(`println', defn(`@println()'))dnl
pushdef(`printq', defn(`@printq()'))dnl
pushdef(`printqln', defn(`@printqln()'))dnl
pushdef(`var', defn(`@define_var'))dnl
pushdef(`@macro_output')dnl
indir(`@remove_method_vars()')dnl
define(`@definemethod_layer', incr(defn(`@definemethod_layer')))dnl
format(`define(`@definemethod_var[%s]', 0)',
	defn(`@definemethod_layer'))dnl
indir(`@method_return()',
$2
restorequote
)')dnl
restorequote()dnl
')

define(`@apply_method_vars()', `dnl
indir(`@method_vars_loop()', defn(`@definemethod_layer'),
	format(`defn(`@definemethod_var[%d]')', defn(`@definemethod_layer')),
	`pushdef')dnl
')

define(`@remove_method_vars()', `dnl
indir(`@method_vars_loop()', defn(`@definemethod_layer'),
	format(`defn(`@definemethod_var[%d]')', defn(`@definemethod_layer')),
	`popdef')dnl
')

define(`@method_vars_loop()', `dnl
dnl # $1 = n of @definemethod_var[<n>]
dnl # $2 = m of @definemethod_var[<n>][<m>]
dnl # $3 = action (pushdef|popdef)
ifelse(eval(`$2 > 0'), 1, `dnl
ifelse(`$3', `pushdef', `dnl
pushdef(
	defn(`@definemethod_var[$1][$2]'),
	format(`defn(`@definemethod_var[$1]:%s')',
		defn(`@definemethod_var[$1][$2]')))dnl
', `$3', `popdef', `dnl
popdef(defn(`@definemethod_var[$1][$2]'))dnl
')dnl
indir(`@method_vars_loop()', `$1', decr(`$2'), `$3')')')

# Discard arguments and output @macro_output instead
# Quotes from the outside scope are passed as arguments
# to the output macro.
define(`@method_return()', `defaultquote`'dnl
pushdef(`quote_isdefault', defn(`@quotestack[isdefault]'))dnl
ifelse(defn(`quote_isdefault'), `true', `dnl
builtin(`changequote', `[', `]')dnl
pushdef([quote_start], [`])dnl
pushdef([quote_end], ['])dnl
builtin([changequote], [`], ['])dnl
',`dnl
pushdef(`quote_start', defn(`@quotestack[start]'))dnl
pushdef(`quote_end', defn(`@quotestack[end]'))dnl
')dnl
changequote`'dnl
indir(`@remove_method_vars()')dnl
dnl
indir(`@clean_definemethod_var()', defn(`@definemethod_layer'),
	format(`defn(`@definemethod_var[%d]')',
		defn(`@definemethod_layer')))dnl
define(`@definemethod_layer', decr(defn(`@definemethod_layer')))dnl
indir(`@apply_method_vars()')dnl
pushdef(`func', defn(`@macro_output'))dnl
dnl
func(
ifelse(defn(`quote_isdefault'), `true', `dnl
changequote(`[',`]')dnl
defn([quote_start]),
defn([quote_end]),
',`dnl
format(`dnl
changequote(`!'defn(`quote_start'), `!'defn(`quote_end'))dnl
defn(%squote_start%s),
defn(%squote_end%s),
',
`!'defn(`quote_start'), `!'defn(`quote_end'),
`!'defn(`quote_start'), `!'defn(`quote_end'),
)')dnl

	restorequote
	popdef(`func')
	popdef(`@macro_output')
	popdef(`quote_start')
	popdef(`quote_end')
	popdef(`quote_isdefault')
	popdef(`print')
	popdef(`println')
	popdef(`printq')
	popdef(`printqln')
	popdef(`var')
	restorequote,
)')

define(`@clean_definemethod_var()', `dnl
ifelse(eval(`$2 > 0'), 1, `dnl
pushdef(`name',
	format(`defn(`@definemethod_var[%d][%d]')', `$1', `$2'))dnl
undefine(format(``@definemethod_var[%d]:%s'', `$1', defn(`name')))dnl
undefine(format(``@definemethod_var[%d][%d]'', `$1', `$2'))dnl
popdef(`name')dnl
dnl
pushdef(`macro', format(``@definemethod_var[%d]'', `$1'))dnl
define(defn(`macro'), decr(defn(defn(`macro'))))dnl
ifelse(format(`eval(%s == 0)', defn(defn(`macro'))), 1, `dnl
undefine(defn(`macro'))dnl
')dnl
popdef(`macro')dnl
indir(`@clean_definemethod_var()', `$1', decr(`$2'))')')


restoredivert()dnl
')dnl
