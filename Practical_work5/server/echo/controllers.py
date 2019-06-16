from protocol import make_response


def get_echo(request):
    data = request.get('data')
    response = make_response(request, 200, data)
    return response
