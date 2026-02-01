import datetime

import pytest

from . import util

pytestmark = pytest.mark.asyncio


async def test_line_detector_crossed():
    """Tests tns1:RuleEngine/LineDetector/Crossed."""
    event = await util.get_event(
        {
            "SubscriptionReference": {
                "Address": {"_value_1": None, "_attr_1": None},
                "ReferenceParameters": None,
                "Metadata": None,
                "_value_1": None,
                "_attr_1": None,
            },
            "Topic": {
                "_value_1": "tns1:RuleEngine/LineDetector/Crossed",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": {
                "Address": {
                    "_value_1": "xx.xx.xx.xx/onvif/event/alarm",
                    "_attr_1": None,
                },
                "ReferenceParameters": None,
                "Metadata": None,
                "_value_1": None,
                "_attr_1": None,
            },
            "Message": {
                "_value_1": {
                    "Source": {
                        "SimpleItem": [
                            {
                                "Name": "VideoSourceConfigurationToken",
                                "Value": "video_source_config1",
                            },
                            {
                                "Name": "VideoAnalyticsConfigurationToken",
                                "Value": "analytics_video_source",
                            },
                            {"Name": "Rule", "Value": "MyLineDetectorRule"},
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [{"Name": "ObjectId", "Value": "0"}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(2020, 5, 24, 7, 24, 47),
                    "PropertyOperation": "Initialized",
                    "_attr_1": {},
                }
            },
        }
    )

    assert event is not None
    assert event.name == "Line Detector Crossed"
    assert event.platform == "sensor"
    assert event.value == "0"
    assert event.uid == (
        f"{util.TEST_UID}_tns1:RuleEngine/LineDetector/"
        "Crossed_video_source_config1_analytics_video_source_MyLineDetectorRule"
    )
