import dataclasses
import typing

from onvif_parsers import model, registry, util

_AJAX_MOTION_TEMPLATE = model.EventEntity(
    uid="",
    name="Motion Detection",
    platform="binary_sensor",
    device_class="motion",
)

_AJAX_OBJECT_TEMPLATES: dict[str, model.EventEntity] = {
    "Human": dataclasses.replace(_AJAX_MOTION_TEMPLATE, name="Person Detection"),
    "Vehicle": dataclasses.replace(_AJAX_MOTION_TEMPLATE, name="Vehicle Detection"),
    "Pet": dataclasses.replace(_AJAX_MOTION_TEMPLATE, name="Pet Detection"),
}

_AJAX_LINE_CROSS_TEMPLATE = model.EventEntity(
    uid="",
    name="Line Detector Crossed",
    platform="event",
    device_class="motion",
)


@registry.register("tns1:RuleEngine/tnsajax:MotionDetector/Detection")
async def async_parse_ajax_motion_detector(
    uid: str, msg: typing.Any
) -> list[model.EventEntity]:
    """Handle parsing AJAX basic motion events."""
    video_source = ""
    rule = ""
    topic, payload = util.extract_message(msg)

    for source in payload.Source.SimpleItem:
        if source.Name == "VideoSourceToken":
            video_source = util.normalize_video_source(source.Value)
        if source.Name == "Rule":
            rule = source.Value

    for item in payload.Data.SimpleItem:
        if item.Name == "Detected":
            return [
                dataclasses.replace(
                    _AJAX_MOTION_TEMPLATE,
                    uid=f"{uid}_{topic}_{video_source}_{rule}",
                    value=item.Value == "true",
                )
            ]

    return []


@registry.register("tns1:RuleEngine/ObjectDetection/Object")
async def async_parse_ajax_object_detector(
    uid: str, msg: typing.Any
) -> list[model.EventEntity]:
    """Handle parsing AJAX AI object detection events."""
    video_source = ""
    rule = ""
    topic, payload = util.extract_message(msg)

    for source in payload.Source.SimpleItem:
        if source.Name == "VideoSourceToken":
            video_source = util.normalize_video_source(source.Value)
        if source.Name == "Rule":
            rule = source.Value

    for item in payload.Data.SimpleItem:
        if item.Name == "ClassTypes":
            detected_classes = set(item.Value.split() if item.Value else [])
            if "Animal" in detected_classes:
                # Treat animal as pet
                detected_classes.add("Pet")
                detected_classes.discard("Animal")

            events = []
            for cls_key, template in _AJAX_OBJECT_TEMPLATES.items():
                is_active = cls_key in detected_classes
                events.append(
                    dataclasses.replace(
                        template,
                        uid=f"{uid}_{topic}_{video_source}_{rule}_{cls_key}",
                        value=is_active,
                    )
                )
            return events

    return []


@registry.register("tns1:RuleEngine/tnsajax:LineDetector/Crossing")
async def async_parse_ajax_line_crossing(
    uid: str, msg: typing.Any
) -> list[model.EventEntity]:
    """Handle parsing AJAX line crossing events."""
    video_source = ""
    rule = ""
    topic, payload = util.extract_message(msg)

    for source in payload.Source.SimpleItem:
        if source.Name == "VideoSourceToken":
            video_source = util.normalize_video_source(source.Value)
        if source.Name == "Rule":
            rule = source.Value

    return [
        dataclasses.replace(
            _AJAX_LINE_CROSS_TEMPLATE,
            uid=f"{uid}_{topic}_{video_source}_{rule}",
        )
    ]
