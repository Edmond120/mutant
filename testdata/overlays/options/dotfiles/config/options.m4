definemethod(`prefix', `
	ifelse(eval($# > 1), 0, `return')
	ifelse(`$2', `', `return')
	printqln(`$1$2')
	println(`prefix(`$1',shift(shift($@)))')
')

prefix(`option_', A, B, C)
