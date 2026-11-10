import datetime as dt

import pytest

from . import util

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(("state", "expected"), [("true", True), ("false", False)])
async def test_foscam_motion_human(state: str, expected: bool) -> None:
    """Tests tns1:Device/Trigger/MotionDetector - Human detection."""
    events = await util.get_events(
        {
            "SubscriptionReference": None,
            "Topic": {
                "_value_1": "tns1:Device/Trigger/MotionDetector",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": None,
            "Message": {
                "_value_1": {
                    "Source": {
                        "SimpleItem": [
                            {"Name": "VideoSource", "Value": "HUMAN_DETECTION_ALARM"}
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [{"Name": "State", "Value": state}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": dt.datetime(
                        2026, 11, 9, 8, 37, 20, tzinfo=dt.timezone.utc
                    ),
                    "PropertyOperation": "Changed",
                    "_attr_1": {},
                }
            },
        }
    )

    assert events is not None
    assert isinstance(events, list)
    assert len(events) == 1
    event = events[0]

    assert event.name == "Person Detection"
    assert event.platform == "binary_sensor"
    assert event.device_class == "motion"
    assert event.value is expected
    assert event.uid == (
        f"{util.TEST_UID}_tns1:Device/Trigger/MotionDetector_HUMAN_DETECTION_ALARM"
    )
