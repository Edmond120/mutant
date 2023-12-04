ifdef(`@include[mutant_core/namespace.m4]', `', `dnl
define(`@include[mutant_core/namespace.m4]')dnl
include(`mutant_core/changequote.m4')dnl
include(`mutant_core/divert.m4')dnl
include(`mutant_core/definemethod.m4')dnl
divert(`-1')

# If @thisnamespace is an empty string then the current namespace is
# the global namespace. All methods defined here are "public".
define(`@thisnamespace')

define(`namespacedef', `changequote`'dnl
ifelse(eval(`$# == 1'), `1',
`namespacedef(defn(`@thisnamespace'), `$1', `')',
eval(`$# == 2'), `1',
`namespacedef(defn(`@thisnamespace'), `$1', `$2')',
dnl
`pushdef(`namespace', `$1')dnl
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
`dnl
ifdef(format(``%s:%s'', defn(`namespacemacro'), defn(`macroname')),
`popdef(defn(`macroname'))')dnl
pushdef(defn(`macroname'), defn(`definition'))dnl
')dnl
dnl
popdef(`namespace')dnl
popdef(`macroname')dnl
popdef(`definition')dnl
popdef(`namespacemacro')dnl
restorequote()dnl
')')

define(`namespacemethod', `changequote`'dnl
ifelse(eval(`$# == 2'), `1',
`namespacemethod(defn(`@thisnamespace'), `$1', `$2')',
`definemethod(`@namespacemethod_temp', `$3')dnl
namespacedef(`$1', `$2', defn(`@namespacemethod_temp'))dnl
undefine(`@namespacemethod_temp')dnl
restorequote()dnl
')')

define(`@namespace_loop', `dnl
dnl # $1 = namespace
dnl # $2 = index
dnl # $3 = operation
ifelse(eval(`$2 > 0'), `1', `dnl
pushdef(`macroname',
    defn(format(``@namespace[%s][%d]'', `$1', `$2')))dnl
pushdef(`macrodefinition',
	defn(format(``@namespace[%s]:%s'', `$1', defn(`macroname'))))dnl
$3(defn(`macroname'), defn(`macrodefinition'))dnl
popdef(`macrodefinition')dnl
popdef(`macroname')dnl
indir(`@namespace_loop', `$1', decr(`$2'), `$3')')')

define(`@applynamespace', `dnl
indir(
	`@namespace_loop',
    `$1',
    defn(format(``@namespace[%s]'', `$1')),
    `pushdef')`'dnl
')

define(`@removenamespace', `dnl
indir(
	`@namespace_loop',
    `$1',
    defn(format(``@namespace[%s]'', `$1')),
    `popdef')`'dnl
')

define(`enternamespace', `changequote`'dnl
ifelse(`$#', `0', ``enternamespace'',
       eval(`$# > 1'), `1', `errprint(`too many arguments for enternamespace')m4exit(1)')dnl
ifelse(`$1', `', `',
    `ifdef(format(``@namespace[%s]'', `$1'),
         `',
        `dnl # create namespace if it does not exist
define(format(``@namespace[%s]'', `$1'), `0')')')dnl
dnl
pushdef(`pushdef_leavenamespace', defn(`@pushdef_leavenamespace'))dnl
ifelse(
defn(`@thisnamespace'), `$1',
`dnl # same namespace -> do nothing
pushdef_leavenamespace(`', `')dnl
',
defn(`@thisnamespace'), `',
`dnl # coming from global namespace -> push new namespace macros
pushdef(`applynamespace', defn(`@applynamespace'))dnl
applynamespace(popdef(`applynamespace')`$1')dnl
pushdef_leavenamespace(`$1', `')dnl
',
`$1', `',
`dnl # going to global namespace -> pop old namespace macros
pushdef(`removenamespace', defn(`@removenamespace'))dnl
removenamespace(popdef(`removenamespace')defn(`@thisnamespace'))dnl
pushdef_leavenamespace(`', defn(`@thisnamespace'))dnl
',
`dnl # different namespace -> pop old namespace macros, push new namespace macros
pushdef(`removenamespace', defn(`@removenamespace'))dnl
removenamespace(popdef(`removenamespace')defn(`@thisnamespace'))dnl
pushdef(`applynamespace', defn(`@applynamespace'))dnl
applynamespace(popdef(`applynamespace')`$1')dnl
pushdef_leavenamespace(`$1', defn(`@thisnamespace'))dnl
dnl
')dnl
pushdef(`@thisnamespace', `$1')dnl
dnl
popdef(`pushdef_leavenamespace')dnl
restorequote()dnl
')

define(`@pushdef_leavenamespace', `dnl
dnl # $1 = namespace to pop, do not pop if empty string
dnl # $2 = namespace to push, do not push if empty string
format(`dnl
pushdef(`leavenamespace', `changequote`'dnl
popdef(`leavenamespace')dnl
%s`'dnl
%s`'dnl
popdef(`@thisnamespace')dnl
restorequote()dnl
')dnl
',
ifelse(`$1', `', `',
``pushdef(`removenamespace', defn(`@removenamespace'))dnl
removenamespace(popdef(`removenamespace')`$1')dnl
''),
ifelse(`$2', `', `',
``pushdef(`applynamespace', defn(`@applynamespace'))dnl
applynamespace(popdef(`applynamespace')`$2')dnl
''))')

define(`leavenamespace')

restoredivert()dnl
')dnl
