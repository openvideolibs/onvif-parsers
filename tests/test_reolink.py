import datetime

import pytest

from . import util

pytestmark = pytest.mark.asyncio


async def test_reolink_package():
    """Tests reolink package event."""
    event = await util.get_event(
        {
            "SubscriptionReference": None,
            "Topic": {
                "_value_1": "tns1:RuleEngine/MyRuleDetector/Package",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": None,
            "Message": {
                "_value_1": {
                    "Source": {
                        "SimpleItem": [{"Name": "Source", "Value": "000"}],
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
                        2025, 3, 12, 9, 54, 27, tzinfo=datetime.timezone.utc
                    ),
                    "PropertyOperation": "Initialized",
                    "_attr_1": {},
                }
            },
        }
    )

    assert event is not None
    assert event.name == "Package Detection"
    assert event.platform == "binary_sensor"
    assert event.device_class == "occupancy"
    assert event.value
    assert event.uid == (f"{util.TEST_UID}_tns1:RuleEngine/MyRuleDetector/Package_000")
