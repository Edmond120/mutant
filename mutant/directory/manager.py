import shutil
from pathlib import Path
from itertools import chain
from mutant.directory import creator
from mutant.directory import parser
from mutant.m4core import M4
from mutant.utils import git

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

	def eval_options(self, alternative_options=None):
		if alternative_options is None:
			options_file = self.path.joinpath('config/options.m4')
			options = set(parser.read_options(options_file))
		else:
			options = set(alternative_options)

		repos = self.path.joinpath('repos')
		provide_rules = []
		for repo in repos.iterdir():
			provides_file = repo.joinpath('provides.m4')
			if not provides_file.is_file():
				continue
			rules = parser.read_provides(provides_file)
			provide_rules.extend(rules)

		options.update(
			self.__solve_provide_rules(
				provide_rules,
				starting_options=options
			)
		)

		return options

	def eval_template(self, template_string, *, options=None, include_dirs=(), cwd=None):
		if options is None:
			options = self.eval_options()

		option_flags = tuple((
			f'--define=option[{index}]={option}'
			for index, option in enumerate(options)
		))

		include_flags = tuple((
			f'--include={path.absolute().as_posix()}'
			for path in include_dirs
		))

		m4 = M4(
			flags = M4.default_flags + option_flags + include_flags,
			preclude = "include(`mutant_template_toplevel.m4')dnl\n"
		)
		return m4.pipe(template_string, cwd=cwd)

	def eval_template_file(self, filepath, *, options=None):
		repos = self.path.joinpath('repos')
		if not filepath.is_relative_to(repos):
			raise ValueError(f'{filepath.as_posix()} is not relative to {self.path.as_posix}')
		if not filepath.is_file():
			raise ValueError(f'{filepath.as_posix()} does not exist')
		parts = filepath.relative_to(repos).parts
		if not ( parts[1] == 'src' and len(parts) >= 3 ):
			raise ValueError(f'{filepath.as_posix()} is not a valid template path')

		repo = repos.joinpath(parts[0])
		resources = repo.joinpath('resources')

		if resources.is_dir():
			include_dirs=(resources,)
		else:
			include_dirs=()

		with open(filepath, 'r') as file:
			return self.eval_template(
				file.read(),
				include_dirs=include_dirs,
				cwd=filepath.parent,
				options=options,
			)

	def build_configs(self, starting_options=None):
		options = self.eval_options(starting_options)
		build_dir = self.path.joinpath('build')
		repos_dir = self.path.joinpath('repos')
		for repo in repos_dir.iterdir():
			build_repo = build_dir.joinpath(repo.name)
			root = repo.joinpath('src')
			shutil.copytree(root, build_repo,
				symlinks=True,
				ignore=self.__filter_m4_files,
			)
			file_filter = lambda f: f.name.endswith('.m4')
			template_files = self.__depth_first_transversal(root, file_filter)
			for template_file in template_files:
				tail = template_file.relative_to(root)
				dest = build_repo.joinpath(tail)
				self.__build_m4_file(template_file, dest, options)

	def update_stowdir(self):
		build_dir = self.path.joinpath('build')
		stow_dir = self.path.joinpath('stow')
		for dir in stow_dir.iterdir():
			if dir.is_dir() and dir.name == '.git':
				continue
			shutil.rmtree(dir)
		for dir in build_dir.iterdir():
			shutil.copytree(dir, stow_dir.joinpath(dir.name), symlinks=True )
		git.Repo(stow_dir) \
		.add_all() \
		.commit()

	def __build_m4_file(self, filepath, dest, options):
		data = self.eval_template_file(filepath, options=options)
		with dest.open('w') as file:
			shutil.copystat(filepath, dest, follow_symlinks=False)
			file.write(data)

	@staticmethod
	def __depth_first_transversal(dir, file_filter):
		for item in dir.iterdir():
			if item.is_symlink():
				continue # pragma: nocover
			if item.is_dir():
				yield from MutantDirectory.__depth_first_transversal(item, file_filter)
				continue
			if item.is_file() and file_filter(item):
				yield item

	@staticmethod
	def __filter_m4_files(directory, names):
		return filter(lambda name:
			Path(directory).joinpath(name).is_file() and name.endswith('.m4'),
			names
		)

	@staticmethod
	def __solve_provide_rules(provide_rules, starting_options=tuple()):
		options = set(starting_options)
		graph = MutantDirectory.__create_condition_to_rule_map(provide_rules, options)
		return MutantDirectory.__derive_options(options, graph)

	@staticmethod
	def __create_condition_to_rule_map(provide_rules, options):
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
		return graph

	@staticmethod
	def __derive_options(options, graph):
		fresh_options = list(options)
		while len(fresh_options) > 0:
			condition = fresh_options.pop(0)
			if condition not in graph:
				continue
			for rule in graph[condition]:
				rule['conditions'].remove(condition)
				if len(rule['conditions']) > 0:
					continue
				for option in rule['provides']:
					options.add(option)
					if option in graph and option != condition:
						fresh_options.append(option)
			del graph[condition]

		return options
