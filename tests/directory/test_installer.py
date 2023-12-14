from mutant.directory.manager import MutantDirectory
from mutant.directory import installer

class TestInstaller:
	def test_install_uninstall(self, create_testdir):
		tmpdir = create_testdir('install')
		target_dir = tmpdir.joinpath('target')
		repos = ( 'zsh', 'bash', 'fish' )

		mutant_dir = MutantDirectory(tmpdir.joinpath('dotfiles'))
		installer.install(mutant_dir)
		for repo in repos:
			assert target_dir.joinpath(repo).is_symlink()

		installer.uninstall(mutant_dir)
		for repo in repos:
			assert not target_dir.joinpath(repo).is_symlink()
