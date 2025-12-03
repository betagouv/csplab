"""List ipython kernels as defined in the pyproject.toml configuration.

Note: all dependency group is considered as a kernel except for the `dev` group.
"""

from pathlib import Path

import tomllib

pyproject = tomllib.load(Path("./pyproject.toml").open("rb"))
kernels = [k for k in pyproject["dependency-groups"] if k != "dev"]

for kernel in kernels:
    print(kernel)
