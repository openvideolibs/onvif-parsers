import typing

from onvif_parsers import model, registry, util


@registry.register("tns1:VideoSource/MotionAlarm")
@registry.register("tns1:Device/Trigger/tnshik:AlarmIn")
async def async_parse_motion_alarm(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing hikvision alarm detection."""
    topic, payload = util.extract_message(msg)
    source = payload.Source.SimpleItem[0].Value
    return model.EventEntity(
        f"{uid}_{topic}_{source}",
        "Motion Alarm",
        "binary_sensor",
        "motion",
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )
