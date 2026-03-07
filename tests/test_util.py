import datetime

from lxml import etree

import onvif_parsers
import onvif_parsers.util

from . import util

RAW_UNPARSEABLE_PAYLOAD = {
    "SubscriptionReference": None,
    "Topic": {
        "_value_1": "tns1:RuleEngine/tnsajax:ObjectDetector/Detection",
        "Dialect": "http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet",
        "_attr_1": {},
    },
    "ProducerReference": None,
    "Message": {
        "_value_1": {
            "Source": {
                "SimpleItem": [
                    {"Name": "VideoSourceToken", "Value": "9c756e1c7b25-0"},
                    {"Name": "Rule", "Value": "9c756e1c7b25-0-dk2t3"},
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
                        "Name": "Objects",
                        "_value_1": """<tnsajax:Objects xmlns:tnsajax="http://ajax.systems/onvif/wsdl">
  <tnsajax:Human>true</tnsajax:Human>
  <tnsajax:Vehicle>false</tnsajax:Vehicle>
</tnsajax:Objects>""",
                    }
                ],
                "Extension": None,
                "_attr_1": None,
            },
            "Extension": None,
            "UtcTime": datetime.datetime(
                2026, 1, 23, 19, 58, 3, 901775, tzinfo=datetime.timezone.utc
            ),
            "PropertyOperation": None,
            "_attr_1": {},
        }
    },
}


def test_deserialize_event_debug():
    """Test deserializing to an event and then back to the debug format."""
    event = util.deserialize_event(RAW_UNPARSEABLE_PAYLOAD)
    assert event is not None
    assert event.Topic._value_1 == "tns1:RuleEngine/tnsajax:ObjectDetector/Detection"
    assert event.Message._value_1 is not None
    assert event.Message._value_1.Data.ElementItem[0].Name == "Objects"
    assert event.Message._value_1.Data.ElementItem[0]._value_1 is not None
    assert isinstance(
        event.Message._value_1.Data.ElementItem[0]._value_1, etree._Element
    )
    assert event.Message._value_1.UtcTime == datetime.datetime(
        2026, 1, 23, 19, 58, 3, 901775, tzinfo=datetime.timezone.utc
    )

    debug_event = onvif_parsers.util.event_to_debug_format(event)
    assert debug_event is not None
    assert isinstance(debug_event, dict)
    assert (
        debug_event["Topic"]["_value_1"]
        == "tns1:RuleEngine/tnsajax:ObjectDetector/Detection"
    )
    assert (
        debug_event["Message"]["_value_1"]["Data"]["ElementItem"][0]["Name"]
        == "Objects"
    )
    assert isinstance(
        debug_event["Message"]["_value_1"]["Data"]["ElementItem"][0]["_value_1"], str
    )
    assert debug_event["Message"]["_value_1"]["UtcTime"] == datetime.datetime(
        2026, 1, 23, 19, 58, 3, 901775, tzinfo=datetime.timezone.utc
    )
