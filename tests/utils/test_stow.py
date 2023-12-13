import pytest
import os
from pathlib import Path
from mutant.utils import stow
from mutant.exceptions import NotASymlinkError

@pytest.fixture()
def stow_test_setup(create_testdir):
	def func():
		os.environ['BASH_DIR'] = 'bash'
		testdir = create_testdir('stow')
		stowdir = testdir.joinpath('dotfiles', 'stow')
		targetdir = testdir.joinpath('target')
		return ( testdir, stowdir, targetdir )
	return func

class TestStow:
	def test_overwrite_link(self, stow_test_setup):
		testdir, stowdir, targetdir = stow_test_setup()
		def test_package(package):
			src = stowdir.joinpath(package)
			dst = targetdir.joinpath(package)
			stow.overwrite_link(src,dst)
			assert dst.is_symlink()
			assert dst.readlink().samefile(src)

		targetdir.joinpath('zsh') \
		.symlink_to(targetdir.joinpath('fish'))

		test_package('zsh')
		test_package('bash')
		try:
			test_package('fish')
		except NotASymlinkError:
			pass

	def test_remove_link(self, tmp_path):
		target = tmp_path.joinpath('target')
		do_not_delete = tmp_path.joinpath('invalid')
		delete_this = tmp_path.joinpath('valid')

		target.touch()
		tmp_path.joinpath('not_target').touch()
		do_not_delete.symlink_to(tmp_path.joinpath('not_target'))
		delete_this.symlink_to(target)

		stow.remove_link(do_not_delete, target)
		assert do_not_delete.is_symlink()

		stow.remove_link(delete_this, target)
		assert not delete_this.exists()
