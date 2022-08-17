import pytest


@pytest.mark.unit
def test_fixture(important_parameters):
    assert important_parameters["Henrik is cool"]
    assert important_parameters["Hello"] == "World!"
    return None
