ifdef(`@include[mutant_core/divert.m4]', `', `dnl
define(`@include[mutant_core/divert.m4]')dnl
include(`mutant_core/changequote.m4')dnl
builtin(`divert', `-1')

define(`@divertstack', `0')

define(`divert', `changequote`'dnl
ifelse(`$#', `0', `divert(0)', `dnl
pushdef(`@divertstack', `$1')dnl
builtin(`divert', `$1')dnl
')dnl
restorequote()dnl
')

define(`restoredivert', `changequote`'dnl
popdef(`@divertstack')dnl
ifdef(`@divertstack', `', `dnl
define(`@divertstack', `0')dnl
')dnl
builtin(`divert', defn(`@divertstack'))dnl
restorequote()dnl
')

builtin(`divert', `0')dnl
')dnl
