"""
Contains the paths to related directories that are installed outside of
the module.
"""

import sys
import mutant
from pathlib import Path

module_dir = Path(mutant.__file__).parent.resolve(strict=True)
m4_dir = module_dir.joinpath('m4')
