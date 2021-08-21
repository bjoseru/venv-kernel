import pkg_resources
try:
    __version__ = pkg_resources.get_distribution('venv-kernel').version
except pkg_resources.DistributionNotFound:
    __version__ = "development version"
