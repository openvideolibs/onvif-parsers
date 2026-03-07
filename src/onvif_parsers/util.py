import typing

import zeep.helpers
from lxml import etree


def extract_message(msg: typing.Any) -> tuple[str, typing.Any]:
    """Extract the message content and the topic."""
    return msg.Topic._value_1, msg.Message._value_1


_VIDEO_SOURCE_MAPPING = {
    "vsconf": "VideoSourceToken",
}


def normalize_video_source(source: str) -> str:
    """
    Normalize video source.

    Some cameras do not set the VideoSourceToken correctly so we get duplicate
    sensors, so we need to normalize it to the correct value.
    """
    return _VIDEO_SOURCE_MAPPING.get(source, source)


def event_to_debug_format(data: typing.Any) -> typing.Any:
    """
    Converts an event to a format for debugging.

    This is useful because the default repr for zeep event payload doesn't include the
    body of unknown XML elements. This will convert the unknown XML into strings that
    can then be deserialized back into an event for testing.
    """
    # 1. Check if the object is a Zeep CompoundValue.
    # Using serialize_object strips away the Zeep classes and leaves native dicts/lists.
    if hasattr(data, "__values__"):
        data = zeep.helpers.serialize_object(data)

    if isinstance(data, dict):
        return {k: event_to_debug_format(v) for k, v in data.items()}
    if isinstance(data, list):
        return [event_to_debug_format(i) for i in data]

    if hasattr(data, "tag") and hasattr(data, "text"):
        # It's an lxml Element. Convert the tree to a pretty XML string.
        try:
            return etree.tostring(data, pretty_print=True, encoding="unicode")
        except Exception:
            return repr(data)

    return data
