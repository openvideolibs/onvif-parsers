import typing


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
