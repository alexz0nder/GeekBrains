import zlib
import json


def compress_middleware(func):
    def wrapper(request, *args, **kwargs):
        return zlib.compress(func(request, *args, **kwargs))
    return wrapper


def decompress_middleware(func):
    def wrapper(sock, buffer_size, encoding):
        b_response = zlib.decompress(func(sock, buffer_size, encoding))
        response = json.loads(b_response.decode(encoding))
        return response
    return wrapper
