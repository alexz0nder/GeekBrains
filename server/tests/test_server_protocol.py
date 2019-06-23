import pytest
from datetime import datetime
from protocol import make_response, validate_request


@pytest.fixture
def valid_action_fixture():
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
def valid_code_fixture():
    return 200


@pytest.fixture
def invalid_code_fixture():
    return 400


@pytest.fixture
def unauthorized_code_fixture():
    return 403


@pytest.fixture
def user_fixture():
    return '923f604b32a1a6fd4d5df9f3c6dc64b1fd49afb0a9a2ae3469085d4ecba1c580'


@pytest.fixture
def valid_request_fixture(action_fixture, time_fixture, data_fixture):
    return {
        'action': action_fixture,
        'time': time_fixture,
        'date': data_fixture,
        'user': user_fixture
    }


@pytest.fixture
def invalid_request_fixture():
    return {
        'action': invalid_action_fixture,
        'time': time_fixture,
        'date': data_fixture,
        'user': user_fixture
    }


@pytest.fixture
def unauthorized_request_fixture():
    return {
        'action': invalid_action_fixture,
        'time': time_fixture,
        'date': data_fixture,
    }


def test_make_response_valid_action(valid_request_fixture, valid_action_fixture, data_fixture):
    response = make_response(valid_request_fixture, valid_action_fixture, data_fixture)

    assert response.get('action') == valid_action_fixture


def test_make_response_invalid_action(valid_request_fixture, valid_action_fixture, invalid_action_fixture, data_fixture):
    response = make_response(valid_request_fixture, valid_action_fixture, data_fixture)

    assert response.get('action') != invalid_action_fixture


def test_invalid_make_response(invalid_request_fixture, valid_code_fixture, invalid_code_fixture, data_fixture):
    response = make_response(invalid_request_fixture, invalid_code_fixture, data_fixture)

    assert response.get('code') == invalid_code_fixture


def test_unauthorized_make_response(unauthorized_request_fixture, unauthorized_code_fixture, data_fixture):
    response = make_response(invalid_request_fixture, unauthorized_code_fixture, data_fixture)

    assert response.get('code') == unauthorized_code_fixture


def test_validate_request(valid_request_fixture):
    response = validate_request(valid_request_fixture)

    assert response


def test_invalidate_request(invalid_request_fixture):
    response = validate_request(invalid_request_fixture)

    assert response == False
