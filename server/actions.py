from functools import reduce
from settings import INSTALLED_APPS


def get_server_actions():
    server_actions = reduce(
        lambda value, item: value + getattr(item, 'actionnames', []),
        reduce(
            lambda value, item: value + [getattr(item, 'actions', [])],
            reduce(
                lambda value, item: value + [__import__(f'{item}.actions')],
                INSTALLED_APPS,
                []
            ),
            []
        ),
        []
    )
    return server_actions


def resolve(action_name, actions=None):
    actions_list = actions or get_server_actions()
    actions_mapping = {
        action.get('action'): action.get('controller')
        for action in actions_list
    }
    try:
        resolved_function = actions_mapping[action_name]
    except:
        print('everything went wrong!!!')
        resolved_function = actions_mapping['echo']

    return resolved_function
