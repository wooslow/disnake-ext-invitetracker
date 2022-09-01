import collections

from .invite_logger import *

_VersionInfo = collections.namedtuple("_VersionInfo", "major minor micro release serial")

version = "0.0.2"
version_info = _VersionInfo(0, 0, 2, "final", 0)