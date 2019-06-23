import pytest
from actions import get_server_actions, resolve


@pytest.fixture
def valid_action_name_fixture():
    return 'echo'


@pytest.fixture
def invalid_action_name_fixture():
    return 'x3'


def test_valid_get_server_actions():
    response = get_server_actions()

    assert response[0].get('action') is not None
    assert callable(response[0].get('controller'))


def test_valid_resolve(valid_action_name_fixture):
    response = resolve(valid_action_name_fixture)

    assert callable(response)


def test_invalid_resolve(invalid_action_name_fixture):
    response = resolve(invalid_action_name_fixture)

    assert callable(response)

