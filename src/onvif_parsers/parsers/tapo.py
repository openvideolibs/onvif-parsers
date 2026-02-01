import dataclasses
import typing

from onvif_parsers import model, registry, util

_TAPO_EVENT_TEMPLATES: dict[str, model.EventEntity] = {
    "IsVehicle": model.EventEntity(
        uid="",
        name="Vehicle Detection",
        platform="binary_sensor",
        device_class="motion",
    ),
    "IsPeople": model.EventEntity(
        uid="", name="Person Detection", platform="binary_sensor", device_class="motion"
    ),
    "IsPet": model.EventEntity(
        uid="", name="Pet Detection", platform="binary_sensor", device_class="motion"
    ),
    "IsLineCross": model.EventEntity(
        uid="",
        name="Line Detector Crossed",
        platform="binary_sensor",
        device_class="motion",
    ),
    "IsTamper": model.EventEntity(
        uid="", name="Tamper Detection", platform="binary_sensor", device_class="tamper"
    ),
    "IsIntrusion": model.EventEntity(
        uid="",
        name="Intrusion Detection",
        platform="binary_sensor",
        device_class="safety",
    ),
}


@registry.register("tns1:RuleEngine/CellMotionDetector/Intrusion")
@registry.register("tns1:RuleEngine/CellMotionDetector/LineCross")
@registry.register("tns1:RuleEngine/CellMotionDetector/People")
@registry.register("tns1:RuleEngine/CellMotionDetector/Tamper")
@registry.register("tns1:RuleEngine/CellMotionDetector/TpSmartEvent")
@registry.register("tns1:RuleEngine/PeopleDetector/People")
@registry.register("tns1:RuleEngine/TPSmartEventDetector/TPSmartEvent")
async def async_parse_tplink_detector(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing tapo events."""
    video_source = ""
    video_analytics = ""
    rule = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "VideoSourceConfigurationToken":
            video_source = util.normalize_video_source(source.Value)
        if source.Name == "VideoAnalyticsConfigurationToken":
            video_analytics = source.Value
        if source.Name == "Rule":
            rule = source.Value

    for item in payload.Data.SimpleItem:
        event_template = _TAPO_EVENT_TEMPLATES.get(item.Name, None)
        if event_template is None:
            continue

        return dataclasses.replace(
            event_template,
            uid=f"{uid}_{topic}_{video_source}_{video_analytics}_{rule}",
            value=item.Value == "true",
        )

    return None
