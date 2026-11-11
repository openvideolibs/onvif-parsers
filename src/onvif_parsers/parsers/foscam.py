import dataclasses
import typing

from onvif_parsers import model, registry, util

# Foscam reuses the VideoSource SimpleItem to carry the alarm type rather than a
# video source token, e.g. VideoSource=HUMAN_DETECTION_ALARM.
_FOSCAM_ALARM_TEMPLATES: dict[str, model.EventEntity] = {
    "HUMAN_DETECTION_ALARM": model.EventEntity(
        uid="",
        name="Person Detection",
        platform="binary_sensor",
        device_class="motion",
    ),
    "CAR_DETECTION_ALARM": model.EventEntity(
        uid="",
        name="Vehicle Detection",
        platform="binary_sensor",
        device_class="motion",
    ),
    "SOUND_DETECTION_ALARM": model.EventEntity(
        uid="",
        name="Detected Sound",
        platform="binary_sensor",
        device_class="sound",
    ),
}


@registry.register("tns1:Device/Trigger/MotionDetector")
async def async_parse_foscam_motion_detector(
    uid: str, msg: typing.Any
) -> list[model.EventEntity]:
    """Handle parsing Foscam motion detector events."""
    alarm_type = ""
    topic, payload = util.extract_message(msg)

    for source in payload.Source.SimpleItem:
        if source.Name == "VideoSource":
            alarm_type = source.Value

    event_template = _FOSCAM_ALARM_TEMPLATES.get(alarm_type)
    if event_template is None:
        return []

    for item in payload.Data.SimpleItem:
        if item.Name == "State":
            return [
                dataclasses.replace(
                    event_template,
                    uid=f"{uid}_{topic}_{alarm_type}",
                    value=item.Value == "true",
                )
            ]

    return []
