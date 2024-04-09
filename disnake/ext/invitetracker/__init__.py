import collections

from .invite_tracker import *

_VersionInfo = collections.namedtuple("_VersionInfo", "major release serial")

version = "1.0"
version_info = _VersionInfo(1, 0, "final", 0)
