zsh_option_A
zsh_option_B
provided_C provided_zsh_AB zsh_m4_option_AB -> zsh_option_C

option_A -> provided_A
option_B option_B -> provided_B
option_C -> provided_C provided_C

option_A ->

-> provided_D

option_A option_B -> provided_AB

zsh_option_A zsh_option_B -> provided_zsh_AB

unavailable_option -> unprovided_option

definemethod(`make_options', `
	printqln(`zsh_m4_option_A zsh_m4_option_B -> zsh_m4_option_AB')
	printqln(`zsh_m4_option_A')
	printqln(`zsh_m4_option_A -> zsh_m4_option_B')
')

make_options

# should not detect cycles
cycle_A -> cycle_B
cycle_B -> cycle_A
