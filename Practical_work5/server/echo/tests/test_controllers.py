import pytest
from datetime import datetime
from echo.controllers import get_echo


@pytest.fixture
def action_fixture():
    return 'echo'


@pytest.fixture
def time_fixture():
    return datetime.now().timestamp()


@pytest.fixture
def data_fixture():
    return 'Some Test Data'


@pytest.fixture
def request_fixture(action_fixture, time_fixture, data_fixture):
    return {
        'action': action_fixture,
        'time': time_fixture,
        'data': data_fixture
    }


@pytest.fixture
def expected_response_fixture(action_fixture, time_fixture, data_fixture):
    return {
        'action': action_fixture,
        'time': time_fixture,
        'user': None,
        'data': data_fixture,
        'code': 200,
    }


def test_get_valid_echo(request_fixture, expected_response_fixture):
    response = get_echo(request_fixture)

    assert expected_response_fixture.get('code') == response.get('code')
