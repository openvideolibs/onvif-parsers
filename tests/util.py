import os
import typing

import onvif
from lxml import etree
from zeep import Client
from zeep.transports import Transport

import onvif_parsers
import onvif_parsers.model

TEST_UID = "test-unique-id"


def _inflate_xml_strings(data: typing.Any) -> typing.Any:
    """
    Inflate XML strings back to lxml elements.

    Recursively walk the test dictionary. If we find a string that
    looks like an XML block, inflate it to an lxml Element so Zeep's
    constructor accepts it for xsd:any fields.
    """
    if isinstance(data, dict):
        return {k: _inflate_xml_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_inflate_xml_strings(i) for i in data]
    elif isinstance(data, str):
        clean_str = data.strip()
        if clean_str.startswith("<") and clean_str.endswith(">"):
            try:
                return etree.fromstring(data.encode("utf-8"))
            except etree.XMLSyntaxError:
                pass
    return data


def deserialize_event(notification_data: dict[typing.Any, typing.Any]) -> typing.Any:
    """
    Deserializes the serialized event dict format to a zeep object.

    Takes a raw dictionary event payload, inflates XML strings to lxml Elements,
    and constructs/returns the raw Zeep NotificationMessageHolderType object.
    Useful for testing the serialization/deserialization loop directly.
    """
    patched_data = _inflate_xml_strings(notification_data)

    zeep_client = Client(
        f"{os.path.dirname(onvif.__file__)}/wsdl/events.wsdl",
        wsse=None,
        transport=Transport(),
    )

    notif_msg_type = zeep_client.get_type("ns5:NotificationMessageHolderType")
    assert notif_msg_type is not None

    notif_msg = notif_msg_type(**patched_data)
    assert notif_msg is not None

    # The xsd:any type embedded inside the message doesn't parse, so parse it manually.
    msg_elem = zeep_client.get_element("ns8:Message")
    assert msg_elem is not None
    msg_data = msg_elem(**patched_data["Message"]["_value_1"])
    assert msg_data is not None
    notif_msg.Message._value_1 = msg_data

    return notif_msg


async def get_events(
    notification_data: dict[typing.Any, typing.Any],
) -> list[onvif_parsers.model.EventEntity]:
    """Take in a zeep dict, run it through the parser, and return an Event."""
    # Reconstruct the Zeep object from the dictionary
    notif_msg = deserialize_event(notification_data)

    # Pass it to the parser registry
    return await onvif_parsers.parse(notif_msg.Topic._value_1, TEST_UID, notif_msg)
