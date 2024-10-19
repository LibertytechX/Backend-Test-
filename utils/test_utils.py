import pytest


def test_get_env():
    from utils.utils import get_env

    assert get_env("TEST_KEY", "default_value") == "test_value"
    assert get_env("NON_EXISTENT_KEY", "default_value") == "default_value"
    val = get_env("TEST_KEY", "default_value")
    assert isinstance(val, str)
