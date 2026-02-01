from . import registry
from .parsers import (
    hikvision,  # noqa: F401
    reolink,  # noqa: F401
    tapo,  # noqa: F401
    uncategorized,  # noqa: F401
)

__version__ = "1.1.0"

__all__ = ["get"]

get = registry.get_parser
