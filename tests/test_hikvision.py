import datetime

import pytest

from . import util

pytestmark = pytest.mark.asyncio


async def test_hikvision_alarm():
    """Tests hikvision camera alarm event."""
    event = await util.get_event(
        {
            "SubscriptionReference": None,
            "Topic": {
                "_value_1": "tns1:Device/Trigger/tnshik:AlarmIn",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": None,
            "Message": {
                "_value_1": {
                    "Source": {
                        "SimpleItem": [{"Name": "AlarmInToken", "Value": "AlarmIn_1"}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [{"Name": "State", "Value": "true"}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(
                        2025, 3, 13, 22, 57, 26, tzinfo=datetime.UTC
                    ),
                    "PropertyOperation": "Initialized",
                    "_attr_1": {},
                }
            },
        }
    )

    assert event is not None
    assert event.name == "Motion Alarm"
    assert event.platform == "binary_sensor"
    assert event.device_class == "motion"
    assert event.value
    assert event.uid == (
        f"{util.TEST_UID}_tns1:Device/Trigger/tnshik:AlarmIn_AlarmIn_1"
    )
