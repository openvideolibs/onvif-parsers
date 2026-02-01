import typing

from onvif_parsers import model, registry, util


@registry.register("tns1:RuleEngine/MyRuleDetector/Package")
async def async_parse_package_detector(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing reolink package detection."""
    video_source = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "Source":
            video_source = util.normalize_video_source(source.Value)

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}",
        "Package Detection",
        "binary_sensor",
        "occupancy",
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )
