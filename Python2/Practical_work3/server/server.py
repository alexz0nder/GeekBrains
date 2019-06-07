import json, time, socket
from argparse import ArgumentParser

buffersize = 1024
encoding = 'utf-8'

parser = ArgumentParser()
parser.add_argument('-a', type=str, dest='host',
                    help="Server's address. Default = 0.0.0.0. Listens to on all availible addresses.",
                    default='0.0.0.0', nargs='?')
parser.add_argument('-p', type=int, action='store', dest='port',
                    help="Server's TCP port for clients to connect.",
                    default=7777, nargs='?')
args = parser.parse_args()

def get_message_from_client(client):
    data = json.loads(client.recv(buffersize).decode(encoding))
    print(data)
    return data

def parse_message(client_message):
    if client_message["action"] == "echo":
        server_response = {"action": "response"}
        server_response["time"] = time.time()
        return json.dumps(server_response).encode(encoding)
    else:
        return json.dumps(client_message).encode(encoding)

def send_response(client, data):
    client.send(data)
    client.close()
    return

try:
    sock = socket.socket()
    sock.bind((args.host, args.port))
    sock.listen(5)
    print(f'Server was started with {args.host}:{args.port}')

    while True:
        client, address = sock.accept()
        print(f'Client was detected {address}')

        message = get_message_from_client(client)
        send_response(client, parse_message(message))
except KeyboardInterrupt:
    pass
