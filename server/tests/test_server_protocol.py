import pytest
from datetime import datetime
from protocol import make_response, validate_request


@pytest.fixture
def action_fixture():
    return 'echo'


@pytest.fixture
def invalid_action_fixture():
    return 'qwerty'


@pytest.fixture
def time_fixture():
    return datetime.now().timestamp()


@pytest.fixture
def data_fixture():
    return 'some_data'


@pytest.fixture
def code_fixture():
    return 200


@pytest.fixture
def valid_request_fixture(action_fixture, time_fixture, data_fixture):
    return {
        'action': action_fixture,
        'time': time_fixture,
        'date': data_fixture
    }


@pytest.fixture
def invalid_request_fixture():
    return {
        'action': invalid_action_fixture,
        'time': time_fixture,
        'date': data_fixture
    }


def test_valid_make_response(valid_request_fixture, code_fixture, data_fixture):
    response = make_response(valid_request_fixture, code_fixture, data_fixture)

    assert response.get('code') == code_fixture


def test_invalid_make_response(invalid_request_fixture, code_fixture, data_fixture):
    response = make_response(invalid_request_fixture, code_fixture, data_fixture)

    assert response.get('code') == code_fixture


def test_validate_request(valid_request_fixture):
    response = validate_request(valid_request_fixture)

    assert response


def test_invalidate_request(invalid_request_fixture):
    response = validate_request(invalid_request_fixture)

    assert response == False
