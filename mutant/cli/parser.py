import argparse
from mutant.cli import commands

def run_command(args):
	parsed_args = main_parser.parse_args(args)
	return parsed_args.command_func(parsed_args)

class Command_parser:
	"""
	Simple class to deal with the shared features of subparsers
	for the program's subcommands.

	Class functions are mostly just wrappers to argparse that allow
	for chaining.
	"""

	def __init__(self, subparser_group, *, command_name, command_func):
		parser = subparser_group.add_parser(command_name)
		parser.set_defaults(
			command_name = command_name,
			command_func = command_func,
		)
		self.parser = parser

	def add_argument(self, *args, **kwargs):
		self.parser.add_argument(*args, **kwargs)
		return self

main_parser = argparse.ArgumentParser(
	prog = 'Mutant',
	description = 'Generate configuration files with maximal features',
)

subparsers = main_parser.add_subparsers(
	title = 'Commands'
)


# Subcommand specifications

(
	Command_parser(subparsers,
		command_name = 'create',
		command_func = commands.create,
	)
	.add_argument('directory')
)
