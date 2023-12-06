import pytest
from pathlib import Path
from mutant.directory import manager
from mutant.directory.manager import MutantDirectory

@pytest.fixture()
def create_mutant_dir(create_testdir):
	def func(overlay):
		return MutantDirectory(
			create_testdir(overlay)
			.joinpath('dotfiles')
		)
	return func

class TestMutantDirectory:
	def test_new(self, tmp_path):
		mutant_dir_path = tmp_path.joinpath('dotfiles')
		mutant_dir = MutantDirectory.create(mutant_dir_path)
		assert isinstance(mutant_dir, MutantDirectory)

	def test_new_errors(self, tmp_path):
		mutant_dir_path = tmp_path.joinpath('dotfiles')
		try:
			MutantDirectory(mutant_dir_path)
			assert False
		except FileNotFoundError:
			pass

		mutant_dir_path.open(mode='w').close()
		try:
			MutantDirectory(mutant_dir_path)
			assert False
		except NotADirectoryError:
			pass

	def test_wrapper_clone_repos(self, create_testdir, monkeypatch):
		testdir = create_testdir('repo_clone')
		monkeypatch.chdir(testdir)
		mutant_dir_path = testdir.joinpath('dotfiles')
		mutant_dir = MutantDirectory(mutant_dir_path)
		mutant_dir.clone_repos()
		cloned_repos = set(mutant_dir_path.joinpath('repos').iterdir())
		repo_names = (
			'zsh',
		)
		for name in repo_names:
			repo = mutant_dir.path.joinpath('repos', name)
			assert repo in cloned_repos

	def test_wrapper_create_mutation(self, tmp_path):
		mutant_dir = MutantDirectory.create(tmp_path.joinpath('dotfiles'))
		mutant_dir.create_mutation('my_config_repo')
		repo = mutant_dir.path.joinpath('repos/my_config_repo')
		assert repo.joinpath('resources').is_dir()
		assert repo.joinpath('src').is_dir()
		assert repo.joinpath('provides.m4').is_file()
		assert repo.joinpath('.git').is_dir()

	def test_eval_options(self, create_mutant_dir):
		mutant_dir = create_mutant_dir('options')

		options = mutant_dir.eval_options()
		valid_set = set((
			'option_A',
			'option_B',
			'option_C',
			'zsh_option_A',
			'zsh_option_B',
			'zsh_option_C',
			'provided_A',
			'provided_B',
			'provided_C',
			'provided_D',
			'provided_AB',
			'provided_zsh_AB',
			'zsh_m4_option_A',
			'zsh_m4_option_B',
			'zsh_m4_option_AB',
		))
		assert len(options.symmetric_difference(valid_set)) == 0

	def test_eval_template(self, create_mutant_dir):
		mutant_dir = create_mutant_dir('template')

		assert mutant_dir.eval_template(
			"definemethod(`mymacro', `printq(`hello world')')mymacro"
		) == "hello world"

	def test_eval_template_options(self, create_mutant_dir):
		mutant_dir = create_mutant_dir('template')

		# options are obtained by mutant_dir.eval_options
		tests = (
			( "option(`optionA', 1)" , '1' ),
			( "option(`optionB', 2)", '2' ),
			( "option(`ignore_equal_sign=foo', 3)", '3' ),
			( "option(`bar', 4)", '4' ),
		)
		test_str = '\n'.join(map(lambda x: x[0], tests))
		result_str = '\n'.join(map(lambda x: x[1], tests))
		assert mutant_dir.eval_template(test_str) == result_str

	def test_eval_template_option_array(self, create_mutant_dir):
		mutant_dir = create_mutant_dir('template')

		options = mutant_dir.eval_options()
		assert mutant_dir.eval_template(
			"""definemethod(`option_array_length', `
				var(`index', `$1')
				ifelse(index, `', `var(`index', 0)')
				ifdef(format(``option[%d]'', index), `
					print(format(``option_array_length(`%d')'',
						eval(index + 1)))
				', `
					print(index)
				')
			')option_array_length"""
		) == str(len(options))

	def test_eval_template_file_errors(self, create_mutant_dir):
		mutant_dir = create_mutant_dir('template')

		repos_path = mutant_dir.path.joinpath('repos')
		invalid_paths = [
			Path('/'), # not in mutant dir
			mutant_dir.path.joinpath('config'), # not in a repo
			repos_path.joinpath('non_existant/file'),
			repos_path.joinpath('burb/provides.m4'), # invalid template path
		]
		for path in invalid_paths:
			try:
				mutant_dir.eval_template_file(path)
				assert False
			except ValueError:
				pass


	def test_eval_template_file(self, create_mutant_dir):
		mutant_dir = create_mutant_dir('template')
		src_dir = mutant_dir.path.joinpath('repos/burb/src')

		filepath = src_dir.joinpath('simple.m4')
		output = mutant_dir.eval_template_file(filepath)
		assert output == "hello world\n"

		filepath = src_dir.joinpath('settings.m4')
		output = mutant_dir.eval_template_file(filepath)
		assert output == '{\n\t"myoption": "A",\n\t"experimental_feature": false,\n}\n'

	def test_eval_template_cwd(self, create_mutant_dir):
		mutant_dir = create_mutant_dir('template')
		filepath = mutant_dir.path.joinpath('repos/burb/src/include.m4')
		output = mutant_dir.eval_template_file(filepath)
		assert output == 'from plain.txt\nfrom res.txt\n'

	def test_eval_options_alternative_options(self, create_mutant_dir):
		mutant_dir = create_mutant_dir('options')
		assert 'unprovided_option' in mutant_dir.eval_options(('unavailable_option',))

	def test_build_configs(self, create_mutant_dir):
		mutant_dir = create_mutant_dir('build')
		build_dir = mutant_dir.path.joinpath('build')
		mutant_dir.build_configs()

		directories = map(lambda name: build_dir.joinpath(name),
			(
				'bat', 'lf',
				'zsh', 'zsh/settings', 'zsh/settings/a/b/c',
			)
		)
		for directory in directories:
			assert directory.is_dir()

		filepath_content_pairs = (
			( 'zsh/zshrc.m4', "alias cat=bat\nalias l=lf\nalias ls=eza\n" ),
			( 'zsh/settings/options', None ),
			( 'zsh/settings/a/b/c/obscure.txt', "hello world\n" ),
			( 'zsh/settings/a/b/m4_test.m4', "hello world\n" ),
			( 'lf/lfrc.m4', 'map i $bat --paging always "$f"\n'),
		)
		for filepath, contents in filepath_content_pairs:
			file = build_dir.joinpath(filepath)
			assert file.is_file()
			if contents is None:
				continue
			with file.open() as f:
				assert f.read() == contents
