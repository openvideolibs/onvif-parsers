import pytest

from onvif_parsers import errors

from . import util

pytestmark = pytest.mark.asyncio


async def test_reolink_package():
    """Tests unknown topic."""
    with pytest.raises(
        errors.UnknownTopicError, match="No parser registered for topic"
    ):
        await util.get_event(
            {
                "SubscriptionReference": None,
                "Topic": {
                    "_value_1": "jeff:This/Rule/DoesNotExist",
                },
                "ProducerReference": None,
                "Message": {
                    "_value_1": {
                        "Source": {
                            "SimpleItem": [{"Name": "Source", "Value": "000"}],
                        },
                        "Key": None,
                        "Data": {
                            "SimpleItem": [{"Name": "State", "Value": "true"}],
                        },
                        "Extension": None,
                    }
                },
            }
        )
