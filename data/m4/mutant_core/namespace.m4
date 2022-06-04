ifdef(`@include[mutant_core/namespace.m4]', `', `dnl
define(`@include[mutant_core/namespace.m4]')dnl
include(`mutant_core/changequote.m4')dnl
include(`mutant_core/divert.m4')dnl
divert(`-1')

# namespace method specs:
#   Macros defined within a namespace is supposed to be "private".
#   "public" methods should be protected by changequote, but
#   namespaced methods should not. This is to allow namespaced
#   methods to be optimized by tail-recursion, since adding a
#   restorequote at the end of a macro ruins it.

# If @thisnamespace is an empty string then the current namespace is
# the global namespace. All methods defined here are "public".
define(`@thisnamespace')

define(`namespacemethod', `changequote`'dnl
pushdef(`namespace', `$1')dnl
pushdef(`macroname', `$2')dnl
pushdef(`definition', `$3')dnl
pushdef(`namespacemacro', format(``@namespace[%s]'', defn(`namespace')))dnl
dnl
dnl # Error checking
pushdef(`namespaceerror', `ERROR: invalid namespacemethod call, empty namespace arg')dnl
pushdef(`macronameerror', `ERROR: invalid namespacemethod call, empty macroname arg')dnl
ifelse(defn(`namespace'), `', `errprint(defn(`namespaceerror'))m4exit(1)',
       defn(`macroname'), `', `errprint(defn(`macronameerror'))m4exit(1)')dnl
popdef(`namespaceerror')dnl
popdef(`macronameerror')dnl
dnl
dnl # Create namespace if it does not exist
ifdef(defn(`namespacemacro'), `', `define(defn(`namespacemacro'), `0')')dnl
dnl
dnl # Append to namespace macro array
pushdef(`length', incr(defn(defn(`namespacemacro'))))dnl
define(defn(`namespacemacro'), defn(`length'))dnl
define(
	format(``%s[%d]'',
		defn(`namespacemacro'),
		defn(`length')),
	defn(`macroname'))dnl
popdef(`length')dnl
dnl # Append definition
format(`define(`%s:%s', `%s')',
	defn(`namespacemacro'),
	defn(`macroname'),
	defn(`definition'))dnl
ifelse(defn(`@thisnamespace'), defn(`namespace'),
`pushdef(defn(`macroname'), defn(`definition'))')dnl
dnl
popdef(`namespace')dnl
popdef(`macroname')dnl
popdef(`definition')dnl
popdef(`namespacemacro')dnl
restorequote()dnl
')

restoredivert()dnl
')dnl
