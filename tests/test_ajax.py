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
