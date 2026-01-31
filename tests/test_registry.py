import typing

import pytest

from onvif_parsers import model, registry


@registry.register("decorator_test_topic")
async def parser1(uid: str, _: typing.Any) -> model.EventEntity | None:
    return model.EventEntity(
        uid=uid,
        name="Test",
        platform="sensor",
    )


def test_get_parser_none():
    """Getting a non-registered parser returns None."""
    parser = registry.get_parser("non_existent_topic")
    assert parser is None


@pytest.mark.asyncio
async def test_registration_works():
    """Registering a parser works as expected."""
    registry.register("test_topic1")(parser1)
    parser = registry.get_parser("test_topic1")
    assert parser is not None
    assert callable(parser)
    assert await parser("entity_1", None) == model.EventEntity(
        uid="entity_1", name="Test", platform="sensor"
    )


@pytest.mark.asyncio
async def test_decorator_registration():
    """Registering a parser via decorator works as expected."""
    parser = registry.get_parser("decorator_test_topic")
    assert parser is not None
    assert callable(parser)
    assert await parser("entity_1", None) == model.EventEntity(
        uid="entity_1", name="Test", platform="sensor"
    )


def test_double_registration():
    """Registering the same topic twice raises ValueError."""
    registry.register("test_topic2")(parser1)

    with pytest.raises(ValueError):
        registry.register("test_topic2")(parser1)
