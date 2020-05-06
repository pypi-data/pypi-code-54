from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

#
# Excluded from coverage in .coveragerc
#
try:
    # Change here if project is renamed and does not equal the package name
    dist_name = 'sphinxcontrib-git-context'  # pylint: disable=invalid-name
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound
