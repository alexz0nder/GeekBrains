import pytest
from datetime import datetime
from handlers import create_message, get_response_message


@pytest.fixture
def encoding_fixture():
    return 'utf-8'


@pytest.fixture
def interactive_fixture():
    return False


@pytest.fixture
def message_time_fixture():
    return datetime.now().timestamp()


def test_create_message(message_time_fixture, interactive_fixture, encoding_fixture):
    message = create_message(message_time_fixture, interactive_fixture, encoding_fixture)

    print(message)
    assert response[0].get('action') is not None
