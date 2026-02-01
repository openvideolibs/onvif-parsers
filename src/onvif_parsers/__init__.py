import typing

from . import errors, model, registry
from .parsers import (
    hikvision,  # noqa: F401
    reolink,  # noqa: F401
    tapo,  # noqa: F401
    uncategorized,  # noqa: F401
)

__version__ = "1.1.0"

__all__ = ["parse"]


async def parse(topic: str, uid: str, msg: typing.Any) -> model.EventEntity | None:
    """
    Parse an ONVIF event notification message.

    Args:
        topic: The topic string of the ONVIF event notification.
        uid: Unique identifier for the entity.
        msg: The raw event data. zeep.xsd.ComplexType or zeep.xsd.AnySimpleType.

    Returns:
        The parsed EventEntity or None if parsing failed.

    Raises:
        UnknownTopicError: If the topic is not registered in the parser registry.
        AttributeError: If the message structure is invalid.
        KeyError: If expected keys are missing in the message.

    """
    parser = registry.get_parser(topic)
    if parser is None:
        raise errors.UnknownTopicError(f"No parser registered for topic: {topic}")

    return await parser(uid, msg)
