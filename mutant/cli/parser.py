import argparse
from pathlib import Path
from mutant.cli import commands
from mutant.cli import arg_types

def run_command(args):
	parsed_args = main_parser.parse_args(args)
	parsed_args.command_func(parsed_args)

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
			get_mutant_dir = get_mutant_directory,
		)
		self.parser = parser

	def add_argument(self, *args, **kwargs):
		self.parser.add_argument(*args, **kwargs)
		return self

def get_mutant_directory():
	match_func = lambda path: path.is_file() and path.name == '.mutant'
	return _bubble_search(Path.cwd(), match_func)

def _bubble_search(base_path, match_func):
	return _bubble_search_helper(base_path.absolute(), match_func)

def _bubble_search_helper(base_path, match_func):
	if base_path == Path('/'):
		return None # pragma: nocover
	if any(filter(match_func, base_path.iterdir())):
		return base_path
	return _bubble_search_helper(base_path.parent, match_func)

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
	.add_argument('directory', type=arg_types.non_existent_file)
)
