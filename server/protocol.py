from datetime import datetime
from actions import get_server_actions


def validate_request(raw):
    actions_list = get_server_actions()
    actions_mapping = {
        action.get('action'): action.get('controller')
        for action in actions_list
    }

    if 'time' in raw and 'action' in raw:
        if raw['action'] in actions_mapping:
            return True

    return False


def make_response(request, code, data=None):
    return{
        'action': request.get('action'),
        'user': request.get('user'),
        'time': datetime.now().timestamp(),
        'data': data,
        'code': code
    }
