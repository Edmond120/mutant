ifdef(`@include[mutant_core/definemethod.m4]', `', `dnl
define(`@include[mutant_core/definemethod.m4]')dnl
include(`mutant_core/changequote.m4')dnl
include(`mutant_core/divert.m4')dnl
divert(`-1')

changequote(`[',`]')
	define([@default_start_quote], [`])
	define([@default_end_quote], ['])
restorequote

# Variable to hold the output of a macro
define(`@macro_output')

define(`@print()', `
	pushdef(`@temp', defn(`@macro_output'))
	popdef(`@macro_output')
	pushdef(`@macro_output', defn(`@temp')`$1')
	popdef(`@temp')
')

define(`@printq()', `
	pushdef(`@temp', defn(`@macro_output'))
	popdef(`@macro_output')
	pushdef(`@macro_output',
		defn(`@temp')$`'1`$1'$`'2)
	popdef(`@temp')
')

# variables used in @var()
# -----------------------------
# arrays are indexed starting at 1
# @definemethod_layer = recursion depth
# @definemethod_var[<n>] = var_array length, n specifies array,
#                        arrays are created up to the recursion depth
# @definemethod_var[<n>][<m>] = var name, m is index
# @definemethod_var[<n>]:<name> = macro definition given name

define(`@definemethod_layer', 0)
define(`@definemethod_var[0]', 0)

define(`@var()', `
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
')

# Method specs
#   - Output is ignored except for first argument in print()
#   - Quotes are `'
#   - No unquoted dangling parentheses (due to implementation)
#   - Print buffer is a macro and will be called with args 1 & 2
#     being the start and end quotes of the scope where the method
#     is called.
define(`@definemethod_count', `0')

define(`definemethod', `changequote`'dnl
dnl
dnl # setup indir
dnl
define(`@definemethod_count', incr(defn(`@definemethod_count')))dnl
define(`$1', format(``indir(changequote`@definemethod_method[%d]'restorequote,$%s)'', defn(`@definemethod_count'), `@'))dnl
dnl
dnl # definemethod
dnl
define(format(``@definemethod_method[%d]'',defn(`@definemethod_count')), `changequote`'dnl
indir(`@method_macros')dnl
pushdef(`@macro_output')dnl
indir(`@remove_method_vars()')dnl
define(`@definemethod_layer', incr(defn(`@definemethod_layer')))dnl
format(`define(`@definemethod_var[%s]', 0)',
	defn(`@definemethod_layer'))dnl
indir(`@method_return()',
$2
return
'indir(`@default_end_quote')`
restorequote
)')dnl
restorequote()dnl
')

define(`@method_macros', `dnl
pushdef(`return', `indir(`@default_start_quote')')dnl
pushdef(`print',  `changequote`'indir(`@print()',' $`'@`)restorequote()')dnl
pushdef(`printq', `changequote`'indir(`@printq()','$`'@`)restorequote()')dnl
pushdef(`var',    `changequote`'indir(`@var()','   $`'@`)restorequote()')dnl
pushdef(`println', format(``changequote`'print(`$%d
')restorequote()'',`1'))dnl
pushdef(`printqln', format(``changequote`'printq(`$%d
')restorequote()'',`1'))dnl
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
	restorequote
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
