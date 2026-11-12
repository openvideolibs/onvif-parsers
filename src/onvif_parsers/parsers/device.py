import typing

from onvif_parsers import model, registry, util


# The ONVIF Core spec only defines sub-topics of tns1:Device/HardwareFailure
# (FanFailure, PowerSupplyFailure, StorageFailure, TemperatureCritical), but some
# cameras send the bare topic with a "Source" source item and a "State" data item.
@registry.register("tns1:Device/HardwareFailure")
async def async_parse_hardware_failure(
    uid: str, msg: typing.Any
) -> list[model.EventEntity]:
    """Handle parsing generic hardware failure events."""
    topic, payload = util.extract_message(msg)

    source = None
    for item in payload.Source.SimpleItem:
        if item.Name == "Source":
            source = item.Value
    if source is None:
        return []

    for item in payload.Data.SimpleItem:
        if item.Name == "State":
            return [
                model.EventEntity(
                    uid=f"{uid}_{topic}_{source}",
                    name="Hardware Failure",
                    platform="binary_sensor",
                    device_class="problem",
                    value=item.Value == "true",
                    entity_category="diagnostic",
                )
            ]

    return []
