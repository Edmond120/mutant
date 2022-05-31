ifdef(`@include[mutant_core/changequote.m4]', `', `dnl
define(`@include[mutant_core/changequote.m4]')dnl
divert(-1)

# This is a m4 library to use a stack for changing quotes.
# By using a stack for quotes in your macro definitions,
# you can change quotes without having to worry about
# switching back before calling your macros to avoid
# breaking them.

# stack:
#   description:
#     Pushed using "changequote".
#     Popped using "restorequote".
#   values:
#     @quotestack[start]
#     @quotestack[end]
#     @quotestack[defaultquote()]
#     @quotestack[isdefault]

# defaultquote:
#   Sets the quotes back to `' but does not pop the stack.
#   If you want to switch back to the default quotes, it is
#   better to just use changequote with no arguments and/or
#   restorequote.
define(`defaultquote')

# changequote:
#   Calls the builtin changequote and pushes to the stack.
#   Takes the same arguments as the builtin changequote but
#   only accepts either 0 or 2 non-void arguments.
#   The ability to disable quoting is not allowed.

define(`changequote', `defaultquote`'dnl
dnl
ifelse(`$#', `0', `dnl
pushdef(`@quotestack[start]')dnl
pushdef(`@quotestack[end]')dnl
pushdef(`@quotestack[defaultquote()]')dnl
pushdef(`@quotestack[isdefault]', `true')dnl
define(`defaultquote')dnl
builtin(`changequote')dnl
',
`$#', `1', `errprint(
`ERROR: '__program__:__file__:__line__:`
	mutant changequote requires 0 or 2 arguments
')m4exit(1)',
len(`$1'), `0', `errprint(
`ERROR: '__program__:__file__:__line__:`
	mutant changequote does not except void arguments
')m4exit(1)',
len(`$2'), `0', `errprint(
`ERROR: '__program__:__file__:__line__:`
	mutant changequote does not except void arguments
')m4exit(1)',
`dnl
define(`defaultquote', `dnl
builtin($1changequote$2)dnl
define(`defaultquote')dnl
')dnl
pushdef(`@quotestack[start]', `$1')dnl
pushdef(`@quotestack[end]', `$2')dnl
pushdef(`@quotestack[defaultquote()]', defn(`defaultquote'))dnl
pushdef(`@quotestack[isdefault]', `false')dnl
dnl
builtin(`changequote', `$1', `$2')dnl
')dnl
')

# restorequote:
#   Pops the stack and changes the quotes to the ones that are
#   now on the top of the stack.
define(`restorequote', `defaultquote`'dnl
ifdef(`@quotestack[start]', `dnl
popdef(`@quotestack[start]')dnl
popdef(`@quotestack[end]')dnl
popdef(`@quotestack[defaultquote()]')dnl
popdef(`@quotestack[isdefault]')dnl
ifdef(`@quotestack[start]', `dnl
ifelse(defn(`@quotestack[isdefault]'), `false', `dnl
define(`defaultquote', defn(`@quotestack[defaultquote()]'))dnl
pushdef(@, defn(`@quotestack[start]'))dnl
pushdef(@@, defn(`@quotestack[end]'))dnl
builtin(`changequote', defn(@), defn(@@))dnl
popdef(@)dnl
popdef(@@)dnl
', `dnl
define(`defaultquote')dnl
builtin(`changequote')dnl
')dnl
')dnl
')dnl
')

divert(0)dnl
')dnl
