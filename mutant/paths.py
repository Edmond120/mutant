"""
Contains the paths to related directories that are installed outside of
the module.
"""

import pathlib
import sys
import mutant

module_dir = pathlib.Path(mutant.__file__).parent.resolve(strict=True)
is_installed = any(map(
	lambda site_package: module_dir.is_relative_to(site_package),
	filter(
		lambda p: p.name == 'site-packages',
		map(
			lambda s: pathlib.PurePath(s),
			sys.path
		)
	)
))

if is_installed: #pragma: nocover
	data_dir = pathlib.Path(sys.prefix).joinpath('share/mutant').resolve(strict=True)
else:
	data_dir = module_dir.parent.joinpath('data/m4').resolve(strict=True)
