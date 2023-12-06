ifdef(`@include[mutant_core/package.m4]', `', `dnl
define(`@include[mutant_core/package.m4]')dnl
include(`mutant_core/definemethod.m4')dnl
include(`mutant_core/namespace.m4')dnl
divert(`-1')

define(`m4globalpackage',
`changequote`'ifdef(`@include[$1]', `', `dnl
define(`@include[$1]')dnl
divert(`-1')
$2
restoredivert()dnl
restorequote()dnl
')')

define(`m4package',
`m4globalpackage(`$1', `
enternamespace(`$1')
$2
leavenamespace
')')

restoredivert()dnl
')dnl
