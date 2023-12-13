"""
It was originally planned to use GNU stow to handle the symlinks,
which is why this file is named stow.
"""

from mutant.exceptions import NotASymlinkError

def overwrite_link(src, dst):
	"""
	Symlinks src to dst. src and dst are both pathlike objects.
	"""
	if dst.is_symlink():
		dst.unlink()
	if dst.exists():
		raise NotASymlinkError(f'{dst.as_posix()} is not a symlink')
	dst.symlink_to(src)

def remove_link(link, target):
	"Removes link if it is a symlink that points to target"
	if not link.is_symlink():
		return # pragma: no cover
	if link.readlink().samefile(target):
		link.unlink()
