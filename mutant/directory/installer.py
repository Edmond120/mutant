from pathlib import Path
from mutant.utils import stow
from mutant.directory import parser

def install(mutant_dir):
	"""
	Setups the symlinks in mutant_dir's stow directory to the
	rest of the filesystem
	Args:
		mutant_dir is of type MutantDirectory
	"""
	repo_configs = parser.read_repos(mutant_dir.config_dir.joinpath('repos'))
	for repo in repo_configs:
		src = mutant_dir.stow_dir.joinpath(repo['name'])
		if not src.is_dir():
			continue
		if 'path' not in repo:
			continue
		dst = _into_path(mutant_dir.path, repo['path'])
		stow.overwrite_link(src, dst)

def uninstall(mutant_dir):
	"""
	Undos the effects of install()
	"""
	repo_configs = parser.read_repos(mutant_dir.config_dir.joinpath('repos'))
	for repo in repo_configs:
		if 'path' not in repo:
			continue
		link = _into_path(mutant_dir.path, repo['path'])
		stow.remove_link(link, mutant_dir.stow_dir.joinpath(repo['name']))

def _into_path(cwd, path):
	if type(path) is str:
		path = Path(path)
	if not path.is_absolute():
		path = cwd.joinpath(path)
	path = path.expanduser()
	return path
