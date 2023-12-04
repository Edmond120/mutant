include(`mutant_core.m4')dnl
m4package(`mutant_options.m4', `

namespacemethod(`*', `
	printq(`option')
')

namespacemethod(`option', `
	load_options
	ifdef(format(``option:%s'', `$1'),
		`print(`$2')',
		`print(`$3')'
	)
')

namespacemethod(`load_options', `
	ifelse(defn(`@is_options_loaded'), `true', `return')
	ifelse($#, 0, `print(`load_options(0)') return',
		`$1', `', `print(`load_options(0)') return')

	var(`index', `$1')
	var(`item', format(``option[%d]'', index))
	ifdef(defn(`item'), `
		define(format(``option:%s'', defn(defn(`item'))))
		printf(`load_options(%d)', incr(index))
	', `
		namespacedef(`@is_options_loaded', `true')
	')
')

namespacedef(`@is_options_loaded', `false')

')dnl
