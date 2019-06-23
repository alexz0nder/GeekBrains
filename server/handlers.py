import json
import logging

from actions import resolve
from middlewares import compression_middleware
from protocol import validate_request, make_response
from decorators import logger_required

@logger_required
@compression_middleware
def handle_default_request(raw_request, encoding):
    request = json.loads(raw_request.decode(encoding))

    if validate_request(request):
        action_name = request['action']
        controller = resolve(action_name)
        if controller:
            server_response = controller(request)
            logging.info('200 - request: ' + str(request))
        else:
            logging.error('404 - request: ' + str(request))
            server_response = make_response(request, 404, 'Action not found')
    else:
        logging.error('400 - request: ' + str(request))
        server_response = make_response(request, 400, 'Wrong request')

    return json.dumps(server_response).encode(encoding)


def client_send(client, raw_response):
    try:
        client.send(raw_response)
    except:
        logging.debug(f"client.send didn't work")
    else:
        logging.debug(f"client.send worked")
