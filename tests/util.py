import os
import typing

import onvif
from zeep import Client
from zeep.transports import Transport

import onvif_parsers
import onvif_parsers.model

TEST_UID = "test-unique-id"


async def get_event(
    notification_data: dict[typing.Any, typing.Any],
) -> onvif_parsers.model.EventEntity | None:
    """
    Take in a zeep dict, run it through the parser, and return an Event.

    When the parser encounters an unknown topic that it doesn't know how to parse,
    it outputs a message 'No registered handler for event from ...' along with a
    print out of the serialized xml message from zeep. If it tries to parse and
    can't, it prints out 'Unable to parse event from ...' along with the same
    serialized message. This method can take the output directly from these log
    messages and run them through the parser, which makes it easy to add new unit
    tests that verify the message can now be parsed.
    """
    zeep_client = Client(
        f"{os.path.dirname(onvif.__file__)}/wsdl/events.wsdl",
        wsse=None,
        transport=Transport(),
    )

    notif_msg_type = zeep_client.get_type("ns5:NotificationMessageHolderType")
    assert notif_msg_type is not None
    notif_msg = notif_msg_type(**notification_data)
    assert notif_msg is not None

    # The xsd:any type embedded inside the message doesn't parse, so parse it manually.
    msg_elem = zeep_client.get_element("ns8:Message")
    assert msg_elem is not None
    msg_data = msg_elem(**notification_data["Message"]["_value_1"])
    assert msg_data is not None
    notif_msg.Message._value_1 = msg_data

    parser = onvif_parsers.get(notif_msg.Topic._value_1)
    assert parser is not None

    return await parser(TEST_UID, notif_msg)
