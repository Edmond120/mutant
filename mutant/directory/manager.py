from mutant.directory import creator
from mutant.directory import parser

class MutantDirectory:
	"""
	A class where all interactions with a Mutant directory should be
	done through.
	"""

	@classmethod
	def create(cls, path):
		creator.create_mutant_dir(path)
		return cls(path)

	def __init__(self, path):
		self.path = path

		path_str = path.absolute().as_posix()
		if not path.exists():
			raise FileNotFoundError(f'Mutant directory not found: {path_str}')
		if not path.is_dir():
			raise NotADirectoryError(f'Error: {path_str} is not a directory')

	def clone_repos(self):
		creator.clone_repos(self.path)

	def create_mutation(self, name, *, remote=''):
		mutation_dir_path = self.path.joinpath('repos', name)
		creator.create_mutation_dir(mutation_dir_path, remote=remote)

	def eval_options(self):
		options_file = self.path.joinpath('config/options.m4')
		options = set(parser.read_options(options_file))

		repos = self.path.joinpath('repos')
		provide_rules = []
		for repo in repos.iterdir():
			rules = parser.read_provides(repo.joinpath('provides.m4'))
			provide_rules.extend(rules)

		options.update(
			self.__solve_provide_rules(
				provide_rules,
				starting_options=options
			)
		)

		return options

	@staticmethod
	def __solve_provide_rules(provide_rules, starting_options=tuple()):
		options = set(starting_options)
		graph = {}

		for rule in provide_rules:
			if len(rule['conditions']) == 0:
				for option in rule['provides']:
					options.add(option)
				continue
			for option in rule['conditions']:
				if option in graph:
					graph[option].append(rule)
				else:
					graph[option] = [rule]

		changed = True
		fresh_options = list(options)
		fresh_options_next = []
		while changed:
			changed = False
			for condition in fresh_options:
				if condition not in graph:
					continue
				for rule in graph[condition]:
					rule['conditions'].remove(condition)
					if len(rule['conditions']) > 0:
						continue
					for option in rule['provides']:
						options.add(option)
						fresh_options_next.append(option)
					changed = True
				del graph[condition]
			fresh_options, fresh_options_next = fresh_options_next, fresh_options
			fresh_options_next.clear()

		return options
