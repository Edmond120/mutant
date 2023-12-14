ifdef(`@include[mutant_core/changequote.m4]', `', `dnl
define(`@include[mutant_core/changequote.m4]')dnl
divert(-1)

dnl # This is a m4 library to use a stack for changing quotes.
dnl # By using a stack for quotes in your macro definitions,
dnl # you can change quotes without having to worry about
dnl # switching back before calling your macros to avoid
dnl # breaking them.

dnl # stack:
dnl #   description:
dnl #     Pushed using "changequote".
dnl #     Popped using "restorequote".
dnl #   values:
dnl #     @quotestack[start]
dnl #     @quotestack[end]
dnl #     @quotestack[defaultquote()]
dnl #     @quotestack[isdefault]
define(`@init_quotestack', `dnl
define(`@quotestack[start]')
define(`@quotestack[end]')
define(`@quotestack[defaultquote()]')
define(`@quotestack[isdefault]', `true')
')
indir(`@init_quotestack')

dnl # defaultquote:
dnl #   Sets the quotes back to `' but does not pop the stack.
dnl #   If you want to switch back to the default quotes, it is
dnl #   better to just use changequote with no arguments and/or
dnl #   restorequote.
define(`defaultquote')

dnl # changequote:
dnl #   Calls the builtin changequote and pushes to the stack.
dnl #   Takes the same arguments as the builtin changequote but
dnl #   only accepts either 0 or 2 non-void arguments.
dnl #   The ability to disable quoting is not allowed.

define(`changequote', `defaultquote`'dnl
ifelse(`$#', `0', `indir(`@changequote_0arg')',
`$#', `1', `indir(`@changequote_1arg')',
len(`$1'), `0', `indir(`@changequote_empty_arg')',
len(`$2'), `0', `indir(`@changequote_empty_arg')',
`indir(`@changequote_2arg', `$1', `$2')')dnl
')

define(`@changequote_0arg',
`pushdef(`@quotestack[start]')dnl
pushdef(`@quotestack[end]')dnl
pushdef(`@quotestack[defaultquote()]')dnl
pushdef(`@quotestack[isdefault]', `true')dnl
define(`defaultquote')dnl
builtin(`changequote')dnl
')

define(`@changequote_1arg', `errprint(
`ERROR: '__program__:__file__:__line__:`
	mutant changequote requires 0 or 2 arguments
')m4exit(1)')

define(`@changequote_empty_arg', `errprint(
`ERROR: '__program__:__file__:__line__:`
	mutant changequote does not except void arguments
')m4exit(1)')

define(`@changequote_2arg', `dnl
define(`defaultquote', `dnl
builtin($1changequote$2)dnl
define(`defaultquote')dnl
')dnl
pushdef(`@quotestack[start]', `$1')dnl
pushdef(`@quotestack[end]', `$2')dnl
pushdef(`@quotestack[defaultquote()]', defn(`defaultquote'))dnl
pushdef(`@quotestack[isdefault]', `false')dnl
builtin(`changequote', `$1', `$2')dnl
')

dnl # restorequote:
dnl #   Pops the stack and changes the quotes to the ones that are
dnl #   now on the top of the stack.
define(`restorequote', `defaultquote`'dnl
popdef(`@quotestack[start]')dnl
popdef(`@quotestack[end]')dnl
popdef(`@quotestack[defaultquote()]')dnl
popdef(`@quotestack[isdefault]')dnl
ifdef(`@quotestack[start]', `dnl
ifelse(defn(`@quotestack[isdefault]'), `false',
`indir(`@restorequote_nondefault')',
`dnl
define(`defaultquote')dnl
builtin(`changequote')dnl
')dnl
', `indir(`@init_quotestack')')dnl
')

define(`@restorequote_nondefault', `dnl
define(`defaultquote', defn(`@quotestack[defaultquote()]'))dnl
builtin(`changequote',
defn(`@quotestack[start]'),
defn(`@quotestack[end]'))dnl
')

divert(0)dnl
')dnl
