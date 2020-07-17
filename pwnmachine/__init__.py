import os
from . import cli
from . import PwnMachine


version_file = os.path.join(os.path.dirname(__file__), "version.txt")
with open(version_file, "r") as f:
    __version__ = f.read().strip()


__all__ = ["cli", "PwnMachine", "__version__"]
