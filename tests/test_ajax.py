import datetime

import pytest

from . import util

pytestmark = pytest.mark.asyncio


async def test_ajax_motion_detector():
    """Tests tns1:RuleEngine/tnsajax:MotionDetector/Detection."""
    events = await util.get_events(
        {
            "Topic": {
                "_value_1": "tns1:RuleEngine/tnsajax:MotionDetector/Detection",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "Message": {
                "_value_1": {
                    "Source": {
                        "SimpleItem": [
                            {"Name": "VideoSourceToken", "Value": "vsconf"},
                            {"Name": "Rule", "Value": "AjaxMotionRule"},
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [{"Name": "Detected", "Value": "true"}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(
                        2026, 1, 10, 20, 4, 32, tzinfo=datetime.timezone.utc
                    ),
                    "PropertyOperation": "Changed",
                    "_attr_1": {},
                }
            },
        }
    )

    assert events is not None
    assert len(events) == 1
    event = events[0]

    assert event.name == "Motion Detection"
    assert event.platform == "binary_sensor"
    assert event.device_class == "motion"
    assert event.value is True
    assert event.uid == (
        f"{util.TEST_UID}_tns1:RuleEngine/tnsajax:MotionDetector/"
        "Detection_VideoSourceToken_AjaxMotionRule"
    )


async def test_ajax_object_detector_human():
    """Tests tns1:RuleEngine/ObjectDetection/Object - Person detection."""
    events = await util.get_events(
        {
            "Topic": {
                "_value_1": "tns1:RuleEngine/ObjectDetection/Object",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "Message": {
                "_value_1": {
                    "Source": {
                        "SimpleItem": [
                            {"Name": "VideoSourceToken", "Value": "vsconf"},
                            {"Name": "Rule", "Value": "AjaxObjectRule"},
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [{"Name": "ClassTypes", "Value": "Human"}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(
                        2026, 1, 23, 18, 52, 43, tzinfo=datetime.timezone.utc
                    ),
                    "PropertyOperation": "Initialized",
                    "_attr_1": {},
                }
            },
        }
    )

    assert events is not None
    assert isinstance(events, list)
    assert len(events) == 3

    assert {"Person Detection", "Vehicle Detection", "Pet Detection"} == {
        e.name for e in events
    }
    assert all(e.platform == "binary_sensor" for e in events)
    assert all(e.device_class == "motion" for e in events)
    human_event = next(e for e in events if e.name == "Person Detection")
    assert human_event.value is True
    assert human_event.uid == (
        f"{util.TEST_UID}_tns1:RuleEngine/ObjectDetection/"
        "Object_VideoSourceToken_AjaxObjectRule_Human"
    )

    events.remove(human_event)
    assert all(e.value is False for e in events)


async def test_ajax_object_detector_cleared():
    """Tests tns1:RuleEngine/ObjectDetection/Object - Cleared detection."""
    events = await util.get_events(
        {
            "Topic": {
                "_value_1": "tns1:RuleEngine/ObjectDetection/Object",
            },
            "Message": {
                "_value_1": {
                    "Source": {
                        "SimpleItem": [
                            {"Name": "VideoSourceToken", "Value": "vsconf"},
                            {"Name": "Rule", "Value": "AjaxObjectRule"},
                        ],
                    },
                    "Data": {
                        "SimpleItem": [{"Name": "ClassTypes", "Value": ""}],
                    },
                }
            },
        }
    )

    assert events is not None
    assert all(
        e.name in {"Person Detection", "Vehicle Detection", "Pet Detection"}
        for e in events
    )
    assert all(e.value is False for e in events)


async def test_ajax_missing_attributes():
    """Tests async_parse_ajax_object_detector with missing fields."""
    with pytest.raises(AttributeError, match="SimpleItem"):
        await util.get_events(
            {
                "Topic": {
                    "_value_1": "tns1:RuleEngine/ObjectDetection/Object",
                },
                "Message": {
                    "_value_1": {
                        "Data": {
                            "ElementItem": [],
                            "Extension": None,
                            "SimpleItem": [{"Name": "ClassTypes", "Value": "Human"}],
                            "_attr_1": None,
                        },
                    }
                },
            }
        )


async def test_ajax_human_animal():
    """Tests tns1:RuleEngine/ObjectDetection/Object - Human and Pet detection."""
    events = await util.get_events(
        {
            "SubscriptionReference": None,
            "Topic": {
                "_value_1": "tns1:RuleEngine/ObjectDetection/Object",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": None,
            "Message": {
                "_value_1": {
                    "Source": {
                        "SimpleItem": [
                            {"Name": "VideoSourceToken", "Value": "9c756e1c82d0-0"},
                            {"Name": "Rule", "Value": "9c756e1c82d0-0-dk2t3b"},
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [{"Name": "ClassTypes", "Value": "Human Animal"}],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(
                        2026, 3, 8, 16, 19, 5, 928881, tzinfo=datetime.timezone.utc
                    ),
                    "PropertyOperation": "Changed",
                    "_attr_1": {},
                }
            },
        }
    )
    assert events is not None
    assert len(events) == 3
    human_event = next(e for e in events if e.name == "Person Detection")
    animal_event = next(e for e in events if e.name == "Pet Detection")
    assert human_event.value is True
    assert animal_event.value is True
    events.remove(human_event)
    events.remove(animal_event)
    assert all(e.value is False for e in events)


async def test_ajax_human_vehicle():
    """Tests tns1:RuleEngine/ObjectDetection/Object - Human and Pet detection."""
    events = await util.get_events(
        {
            "SubscriptionReference": None,
            "Topic": {
                "_value_1": "tns1:RuleEngine/ObjectDetection/Object",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": None,
            "Message": {
                "_value_1": {
                    "Source": {
                        "SimpleItem": [
                            {"Name": "VideoSourceToken", "Value": "9c756e1c82d0-0"},
                            {"Name": "Rule", "Value": "9c756e1c82d0-0-dk2t3b"},
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [
                            {"Name": "ClassTypes", "Value": "Human Vehicle"}
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(
                        2026, 3, 8, 16, 23, 1, 503234, tzinfo=datetime.timezone.utc
                    ),
                    "PropertyOperation": "Changed",
                    "_attr_1": {},
                }
            },
        }
    )
    assert events is not None
    assert len(events) == 3
    human_event = next(e for e in events if e.name == "Person Detection")
    vehicle_event = next(e for e in events if e.name == "Vehicle Detection")
    assert human_event.value is True
    assert vehicle_event.value is True
    events.remove(human_event)
    events.remove(vehicle_event)
    assert all(e.value is False for e in events)


async def test_ajax_line_crossing():
    """Tests tns1:RuleEngine/tnsajax:LineDetector/Crossing."""
    events = await util.get_events(
        {
            "SubscriptionReference": None,
            "Topic": {
                "_value_1": "tns1:RuleEngine/tnsajax:LineDetector/Crossing",
                "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
                "_attr_1": {},
            },
            "ProducerReference": None,
            "Message": {
                "_value_1": {
                    "Source": {
                        "SimpleItem": [
                            {"Name": "VideoSourceToken", "Value": "9c756e1c82d0-0"},
                            {"Name": "Rule", "Value": "9c756e1c82d0-0-dk2t3c"},
                        ],
                        "ElementItem": [],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Key": None,
                    "Data": {
                        "SimpleItem": [],
                        "ElementItem": [
                            {
                                "_value_1": '<ajax:LineCrossing xmlns:ajax="http://ajax.systems/onvif/wsdl" xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:tns1="http://www.onvif.org/ver10/topics" xmlns:tnsajax="http://ajax.systems/onvif/topics" xmlns:tt="http://www.onvif.org/ver10/schema" xmlns:tev="http://www.onvif.org/ver10/events/wsdl" xmlns:wsnt="http://docs.oasis-open.org/wsn/b-2">\n  <ajax:Line id="0" index="0" points="0.77 0.7 0.48 0.037"/>\n</ajax:LineCrossing>\n',  # noqa: E501
                                "Name": "LineCrossing",
                            }
                        ],
                        "Extension": None,
                        "_attr_1": None,
                    },
                    "Extension": None,
                    "UtcTime": datetime.datetime(
                        2026, 3, 8, 16, 23, 29, 197832, tzinfo=datetime.timezone.utc
                    ),
                    "PropertyOperation": None,
                    "_attr_1": {},
                }
            },
        }
    )

    assert events is not None
    assert len(events) == 1
    event = events[0]

    assert event.name == "Line Detector Crossed"
    assert event.platform == "event"
    assert event.device_class == "motion"
    assert event.value is None
    assert event.uid == (
        f"{util.TEST_UID}_tns1:RuleEngine/tnsajax:LineDetector/"
        "Crossing_9c756e1c82d0-0_9c756e1c82d0-0-dk2t3c"
    )
