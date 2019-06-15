from protocol import make_response


def get_echo(request):
    data = request.get('data')
    # server_response = {"action": "response"}
    # server_response["time"] = time.time()
    return make_response(request, 200, data)
