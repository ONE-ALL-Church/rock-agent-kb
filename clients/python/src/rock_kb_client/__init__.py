from importlib.metadata import PackageNotFoundError, version

__all__ = ["__version__"]

try:
    __version__ = version("rock-kb")
except PackageNotFoundError:  # Direct source-tree imports are not installed packages.
    __version__ = "0+unknown"
