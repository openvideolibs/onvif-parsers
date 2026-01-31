
from dataclasses import dataclass
from typing import Any


@dataclass
class EventEntity:
    """Represents a ONVIF event entity."""

    # Unique identifier for the entity
    uid: str
    # Human-readable name for the entity
    name: str
    # Type of platform (e.g., sensor, binary_sensor)
    platform: str
    # Optional device class (e.g., motion, alarm, safety). The options vary based on the
    # platform.
    # See https://www.home-assistant.io/integrations/homeassistant/#device-class
    device_class: str | None = None
    # Optional unit of measurement (e.g., percent)
    unit_of_measurement: str | None = None
    # Current value of the entity. Most onvif events are boolean (true/false), but this
    # could be an integer or timestamp or other data types supported as well.
    value: Any = None
    # Optional entity category (e.g., diagnostic, configuration). The default (sensor)
    # does not need to be specified.
    entity_category: str | None = None
    # Indicates whether the entity is enabled by default. Defaults to True.
    entity_enabled: bool = True
