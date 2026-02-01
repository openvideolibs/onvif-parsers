import datetime

import pytest

from . import util

pytestmark = pytest.mark.asyncio


async def test_tapo_line_crossed():
    """Tests tns1:RuleEngine/CellMotionDetector/LineCross."""
    event = await util.get_event(
        {
            "SubscriptionReference": {
                "Address": {
                    "_value_1": "http://CAMERA_LOCAL_IP:2020/event-0_2020",
                    "_attr_1": None,
                },
                "ReferenceParameters": None,
                "Metadata": None,
                "_value_1": None,
                "_attr_1": None,
            },
            "Topic": {
                "_value_1": "tns1:RuleEngine/CellMotionDetector/LineCross",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": {
                "Address": {
                    "_value_1": "http://CAMERA_LOCAL_IP:5656/event",
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
                                "Value": "vsconf",
                            },
                            {
                                "Name": "VideoAnalyticsConfigurationToken",
                                "Value": "VideoAnalyticsToken",
                            },
                            {"Name": "Rule", "Value": "MyLineCrossDetectorRule"},
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [{"Name": "IsLineCross", "Value": "true"}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(
                        2025, 1, 3, 21, 5, 14, tzinfo=datetime.UTC
                    ),
                    "PropertyOperation": "Changed",
                    "_attr_1": {},
                }
            },
        }
    )

    assert event is not None
    assert event.name == "Line Detector Crossed"
    assert event.platform == "binary_sensor"
    assert event.device_class == "motion"
    assert event.value
    assert event.uid == (
        f"{util.TEST_UID}_tns1:RuleEngine/CellMotionDetector/"
        "LineCross_VideoSourceToken_VideoAnalyticsToken_MyLineCrossDetectorRule"
    )


async def test_tapo_tpsmartevent_vehicle():
    """Tests tns1:RuleEngine/TPSmartEventDetector/TPSmartEvent - vehicle."""
    event = await util.get_event(
        {
            "Message": {
                "_value_1": {
                    "Data": {
                        "ElementItem": [],
                        "Extension": None,
                        "SimpleItem": [{"Name": "IsVehicle", "Value": "true"}],
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "Key": None,
                    "PropertyOperation": "Changed",
                    "Source": {
                        "ElementItem": [],
                        "Extension": None,
                        "SimpleItem": [
                            {
                                "Name": "VideoSourceConfigurationToken",
                                "Value": "vsconf",
                            },
                            {
                                "Name": "VideoAnalyticsConfigurationToken",
                                "Value": "VideoAnalyticsToken",
                            },
                            {
                                "Name": "Rule",
                                "Value": "MyTPSmartEventDetectorRule",
                            },
                        ],
                        "_attr_1": None,
                    },
                    "UtcTime": datetime.datetime(
                        2024, 11, 2, 0, 33, 11, tzinfo=datetime.UTC
                    ),
                    "_attr_1": {},
                }
            },
            "ProducerReference": {
                "Address": {
                    "_attr_1": None,
                    "_value_1": "http://192.168.56.127:5656/event",
                },
                "Metadata": None,
                "ReferenceParameters": None,
                "_attr_1": None,
                "_value_1": None,
            },
            "SubscriptionReference": {
                "Address": {
                    "_attr_1": None,
                    "_value_1": "http://192.168.56.127:2020/event-0_2020",
                },
                "Metadata": None,
                "ReferenceParameters": None,
                "_attr_1": None,
                "_value_1": None,
            },
            "Topic": {
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
                "_value_1": "tns1:RuleEngine/TPSmartEventDetector/TPSmartEvent",
            },
        }
    )

    assert event is not None
    assert event.name == "Vehicle Detection"
    assert event.platform == "binary_sensor"
    assert event.device_class == "motion"
    assert event.value
    assert event.uid == (
        f"{util.TEST_UID}_tns1:RuleEngine/TPSmartEventDetector/"
        "TPSmartEvent_VideoSourceToken_VideoAnalyticsToken_MyTPSmartEventDetectorRule"
    )


async def test_tapo_cellmotiondetector_vehicle():
    """Tests tns1:RuleEngine/CellMotionDetector/TpSmartEvent - vehicle."""
    event = await util.get_event(
        {
            "SubscriptionReference": {
                "Address": {
                    "_value_1": "http://CAMERA_LOCAL_IP:2020/event-0_2020",
                    "_attr_1": None,
                },
                "ReferenceParameters": None,
                "Metadata": None,
                "_value_1": None,
                "_attr_1": None,
            },
            "Topic": {
                "_value_1": "tns1:RuleEngine/CellMotionDetector/TpSmartEvent",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": {
                "Address": {
                    "_value_1": "http://CAMERA_LOCAL_IP:5656/event",
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
                                "Value": "vsconf",
                            },
                            {
                                "Name": "VideoAnalyticsConfigurationToken",
                                "Value": "VideoAnalyticsToken",
                            },
                            {"Name": "Rule", "Value": "MyTPSmartEventDetectorRule"},
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [{"Name": "IsVehicle", "Value": "true"}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(
                        2025, 1, 5, 14, 2, 9, tzinfo=datetime.UTC
                    ),
                    "PropertyOperation": "Changed",
                    "_attr_1": {},
                }
            },
        }
    )

    assert event is not None
    assert event.name == "Vehicle Detection"
    assert event.platform == "binary_sensor"
    assert event.device_class == "motion"
    assert event.value
    assert event.uid == (
        f"{util.TEST_UID}_tns1:RuleEngine/CellMotionDetector/"
        "TpSmartEvent_VideoSourceToken_VideoAnalyticsToken_MyTPSmartEventDetectorRule"
    )


async def test_tapo_tpsmartevent_person():
    """Tests tns1:RuleEngine/TPSmartEventDetector/TPSmartEvent - person."""
    event = await util.get_event(
        {
            "Message": {
                "_value_1": {
                    "Data": {
                        "ElementItem": [],
                        "Extension": None,
                        "SimpleItem": [{"Name": "IsPeople", "Value": "true"}],
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "Key": None,
                    "PropertyOperation": "Changed",
                    "Source": {
                        "ElementItem": [],
                        "Extension": None,
                        "SimpleItem": [
                            {
                                "Name": "VideoSourceConfigurationToken",
                                "Value": "vsconf",
                            },
                            {
                                "Name": "VideoAnalyticsConfigurationToken",
                                "Value": "VideoAnalyticsToken",
                            },
                            {"Name": "Rule", "Value": "MyPeopleDetectorRule"},
                        ],
                        "_attr_1": None,
                    },
                    "UtcTime": datetime.datetime(
                        2024, 11, 3, 18, 40, 43, tzinfo=datetime.UTC
                    ),
                    "_attr_1": {},
                }
            },
            "ProducerReference": {
                "Address": {
                    "_attr_1": None,
                    "_value_1": "http://192.168.56.127:5656/event",
                },
                "Metadata": None,
                "ReferenceParameters": None,
                "_attr_1": None,
                "_value_1": None,
            },
            "SubscriptionReference": {
                "Address": {
                    "_attr_1": None,
                    "_value_1": "http://192.168.56.127:2020/event-0_2020",
                },
                "Metadata": None,
                "ReferenceParameters": None,
                "_attr_1": None,
                "_value_1": None,
            },
            "Topic": {
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
                "_value_1": "tns1:RuleEngine/PeopleDetector/People",
            },
        }
    )

    assert event is not None
    assert event.name == "Person Detection"
    assert event.platform == "binary_sensor"
    assert event.device_class == "motion"
    assert event.value
    assert event.uid == (
        f"{util.TEST_UID}_tns1:RuleEngine/PeopleDetector/"
        "People_VideoSourceToken_VideoAnalyticsToken_MyPeopleDetectorRule"
    )


async def test_tapo_tpsmartevent_pet():
    """Tests tns1:RuleEngine/TPSmartEventDetector/TPSmartEvent - pet."""
    event = await util.get_event(
        {
            "SubscriptionReference": {
                "Address": {
                    "_value_1": "http://192.168.56.63:2020/event-0_2020",
                    "_attr_1": None,
                },
                "ReferenceParameters": None,
                "Metadata": None,
                "_value_1": None,
                "_attr_1": None,
            },
            "Topic": {
                "_value_1": "tns1:RuleEngine/TPSmartEventDetector/TPSmartEvent",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": {
                "Address": {
                    "_value_1": "http://192.168.56.63:5656/event",
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
                                "Value": "vsconf",
                            },
                            {
                                "Name": "VideoAnalyticsConfigurationToken",
                                "Value": "VideoAnalyticsToken",
                            },
                            {"Name": "Rule", "Value": "MyTPSmartEventDetectorRule"},
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [{"Name": "IsPet", "Value": "true"}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(
                        2025, 1, 22, 13, 24, 57, tzinfo=datetime.UTC
                    ),
                    "PropertyOperation": "Changed",
                    "_attr_1": {},
                }
            },
        }
    )

    assert event is not None
    assert event.name == "Pet Detection"
    assert event.platform == "binary_sensor"
    assert event.device_class == "motion"
    assert event.value
    assert event.uid == (
        f"{util.TEST_UID}_tns1:RuleEngine/TPSmartEventDetector/"
        "TPSmartEvent_VideoSourceToken_VideoAnalyticsToken_MyTPSmartEventDetectorRule"
    )


async def test_tapo_cellmotiondetector_person():
    """Tests tns1:RuleEngine/CellMotionDetector/People - person."""
    event = await util.get_event(
        {
            "SubscriptionReference": {
                "Address": {
                    "_value_1": "http://192.168.56.63:2020/event-0_2020",
                    "_attr_1": None,
                },
                "ReferenceParameters": None,
                "Metadata": None,
                "_value_1": None,
                "_attr_1": None,
            },
            "Topic": {
                "_value_1": "tns1:RuleEngine/CellMotionDetector/People",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": {
                "Address": {
                    "_value_1": "http://192.168.56.63:5656/event",
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
                                "Value": "vsconf",
                            },
                            {
                                "Name": "VideoAnalyticsConfigurationToken",
                                "Value": "VideoAnalyticsToken",
                            },
                            {"Name": "Rule", "Value": "MyPeopleDetectorRule"},
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [{"Name": "IsPeople", "Value": "true"}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(
                        2025, 1, 3, 20, 9, 22, tzinfo=datetime.UTC
                    ),
                    "PropertyOperation": "Changed",
                    "_attr_1": {},
                }
            },
        }
    )

    assert event is not None
    assert event.name == "Person Detection"
    assert event.platform == "binary_sensor"
    assert event.device_class == "motion"
    assert event.value
    assert event.uid == (
        f"{util.TEST_UID}_tns1:RuleEngine/CellMotionDetector/"
        "People_VideoSourceToken_VideoAnalyticsToken_MyPeopleDetectorRule"
    )


async def test_tapo_tamper():
    """Tests tns1:RuleEngine/CellMotionDetector/Tamper - tamper."""
    event = await util.get_event(
        {
            "SubscriptionReference": {
                "Address": {
                    "_value_1": "http://CAMERA_LOCAL_IP:2020/event-0_2020",
                    "_attr_1": None,
                },
                "ReferenceParameters": None,
                "Metadata": None,
                "_value_1": None,
                "_attr_1": None,
            },
            "Topic": {
                "_value_1": "tns1:RuleEngine/CellMotionDetector/Tamper",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": {
                "Address": {
                    "_value_1": "http://CAMERA_LOCAL_IP:5656/event",
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
                                "Value": "vsconf",
                            },
                            {
                                "Name": "VideoAnalyticsConfigurationToken",
                                "Value": "VideoAnalyticsToken",
                            },
                            {"Name": "Rule", "Value": "MyTamperDetectorRule"},
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [{"Name": "IsTamper", "Value": "true"}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(
                        2025, 1, 5, 21, 1, 5, tzinfo=datetime.UTC
                    ),
                    "PropertyOperation": "Changed",
                    "_attr_1": {},
                }
            },
        }
    )

    assert event is not None
    assert event.name == "Tamper Detection"
    assert event.platform == "binary_sensor"
    assert event.device_class == "tamper"
    assert event.value
    assert event.uid == (
        f"{util.TEST_UID}_tns1:RuleEngine/CellMotionDetector/"
        "Tamper_VideoSourceToken_VideoAnalyticsToken_MyTamperDetectorRule"
    )


async def test_tapo_intrusion():
    """Tests tns1:RuleEngine/CellMotionDetector/Intrusion - intrusion."""
    event = await util.get_event(
        {
            "SubscriptionReference": {
                "Address": {
                    "_value_1": "http://192.168.100.155:2020/event-0_2020",
                    "_attr_1": None,
                },
                "ReferenceParameters": None,
                "Metadata": None,
                "_value_1": None,
                "_attr_1": None,
            },
            "Topic": {
                "_value_1": "tns1:RuleEngine/CellMotionDetector/Intrusion",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": {
                "Address": {
                    "_value_1": "http://192.168.100.155:5656/event",
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
                                "Value": "vsconf",
                            },
                            {
                                "Name": "VideoAnalyticsConfigurationToken",
                                "Value": "VideoAnalyticsToken",
                            },
                            {"Name": "Rule", "Value": "MyIntrusionDetectorRule"},
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [{"Name": "IsIntrusion", "Value": "true"}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(
                        2025, 1, 11, 10, 40, 45, tzinfo=datetime.UTC
                    ),
                    "PropertyOperation": "Changed",
                    "_attr_1": {},
                }
            },
        }
    )

    assert event is not None
    assert event.name == "Intrusion Detection"
    assert event.platform == "binary_sensor"
    assert event.device_class == "safety"
    assert event.value
    assert event.uid == (
        f"{util.TEST_UID}_tns1:RuleEngine/CellMotionDetector/"
        "Intrusion_VideoSourceToken_VideoAnalyticsToken_MyIntrusionDetectorRule"
    )


async def test_tapo_missing_attributes():
    """Tests async_parse_tplink_detector with missing fields."""
    with pytest.raises(AttributeError, match="SimpleItem"):
        await util.get_event(
            {
                "Message": {
                    "_value_1": {
                        "Data": {
                            "ElementItem": [],
                            "Extension": None,
                            "SimpleItem": [{"Name": "IsPeople", "Value": "true"}],
                            "_attr_1": None,
                        },
                    }
                },
                "Topic": {
                    "_value_1": "tns1:RuleEngine/PeopleDetector/People",
                },
            }
        )


async def test_tapo_unknown_type():
    """Tests async_parse_tplink_detector with unknown event type."""
    event = await util.get_event(
        {
            "Message": {
                "_value_1": {
                    "Data": {
                        "ElementItem": [],
                        "Extension": None,
                        "SimpleItem": [{"Name": "IsNotPerson", "Value": "true"}],
                        "_attr_1": None,
                    },
                    "Source": {
                        "ElementItem": [],
                        "Extension": None,
                        "SimpleItem": [
                            {
                                "Name": "VideoSourceConfigurationToken",
                                "Value": "vsconf",
                            },
                            {
                                "Name": "VideoAnalyticsConfigurationToken",
                                "Value": "VideoAnalyticsToken",
                            },
                            {"Name": "Rule", "Value": "MyPeopleDetectorRule"},
                        ],
                    },
                }
            },
            "Topic": {
                "_value_1": "tns1:RuleEngine/PeopleDetector/People",
            },
        }
    )

    assert event is None
