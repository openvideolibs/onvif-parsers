import typing
from collections.abc import Callable

from . import model

# Type alias for a parser callable. It should be an async function.
# Args:
#  str: The uid of the entity.
#  Any: The raw event data. zeep.xsd.ComplexType or zeep.xsd.AnySimpleType.
#       TODO: could we make this zeep.Type or zeep.AnyType?
# Returns:
#  Awaitable[model.EventEntity]: The parsed EventEntity.
ParserCallable: typing.TypeAlias = Callable[
    [str, typing.Any], typing.Awaitable[model.EventEntity | None]
]


class Registry:
    """A registry of parsers."""

    def __init__(self):
        self.registry: dict[str, ParserCallable] = {}

    def register(self, key: str, f: ParserCallable) -> None:
        """Register a parser function under a given key."""
        if key in self.registry:
            raise ValueError(f"Key {key} already registered")

        self.registry[key] = f

    def get(self, key: str) -> Callable | None:
        """Get a parser function by key."""
        return self.registry.get(key)


_REGISTRY = Registry()


def register(topic: str) -> Callable[[ParserCallable], ParserCallable]:
    """Register an onvif parser callable with the given topic."""

    def wrapper(func: ParserCallable) -> ParserCallable:
        _REGISTRY.register(topic, func)
        return func

    return wrapper


def get_parser(topic: str) -> ParserCallable | None:
    """Get a parser callable for the given topic."""
    return _REGISTRY.get(topic)
