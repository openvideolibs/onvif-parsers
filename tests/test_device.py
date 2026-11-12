import datetime as dt
import typing

import pytest

from . import util

pytestmark = pytest.mark.asyncio


def _hardware_failure_event(
    data_items: list[dict[str, str]],
) -> dict[str, typing.Any]:
    """Build a tns1:Device/HardwareFailure event as sent at subscription time."""
    return {
        "SubscriptionReference": None,
        "Topic": {
            "_value_1": "tns1:Device/HardwareFailure",
            "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
            "_attr_1": {},
        },
        "ProducerReference": None,
        "Message": {
            "_value_1": {
                "Source": {
                    "SimpleItem": [{"Name": "Source", "Value": "HardwareId"}],
                    "ElementItem": [],
                    "Extension": None,
                    "_attr_1": None,
                },
                "Key": None,
                "Data": {
                    "SimpleItem": data_items,
                    "ElementItem": [],
                    "Extension": None,
                    "_attr_1": None,
                },
                "Extension": None,
                "UtcTime": dt.datetime(2026, 11, 12, 13, 9, 5, tzinfo=dt.timezone.utc),
                "PropertyOperation": "Initialized",
                "_attr_1": {},
            }
        },
    }


@pytest.mark.parametrize(("state", "expected"), [("true", True), ("false", False)])
async def test_device_hardware_failure(state: str, expected: bool) -> None:
    """Tests tns1:Device/HardwareFailure."""
    events = await util.get_events(
        _hardware_failure_event([{"Name": "State", "Value": state}])
    )

    assert events is not None
    assert isinstance(events, list)
    assert len(events) == 1
    event = events[0]
    assert event.name == "Hardware Failure"
    assert event.platform == "binary_sensor"
    assert event.device_class == "problem"
    assert event.entity_category == "diagnostic"
    assert event.value is expected
    assert event.uid == f"{util.TEST_UID}_tns1:Device/HardwareFailure_HardwareId"


async def test_device_hardware_failure_without_state() -> None:
    """Tests tns1:Device/HardwareFailure without a State data item."""
    events = await util.get_events(
        _hardware_failure_event([{"Name": "Other", "Value": "true"}])
    )

    assert events == []
