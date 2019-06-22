import hashlib
import json

from _datetime import datetime
from middlewares import compress_middleware, decompress_middleware

@compress_middleware
def create_message(message_time,interactive, encoding):
    message = {
        'action': 'echo',
        'data': 'Test',
        'time': message_time,
        'user': None
    }
    if interactive:
        print('You started client in Interactive mode. Enter action and data.')
        message['action'] = input('acton: ')
        message['data'] = input('data: ')

    hash_obj = hashlib.sha256()
    hash_obj.update(
        str(datetime.now().timestamp()).encode(encoding)
    )
    message["user"] = hash_obj.hexdigest()

    source_message = json.dumps(message).encode(encoding)
    return source_message


@decompress_middleware
def get_response_message(sock, buffer_size, encoding):
    response = sock.recv(buffer_size)
    return response


