from . import registry

__version__ = "1.0.0"

__all__ = ["get"]

get = registry.get_parser
