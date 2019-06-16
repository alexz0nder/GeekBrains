import socket, time, json
from argparse import ArgumentParser

buffersize = 1024
encoding = 'utf-8'

parser = ArgumentParser()
parser.add_argument('-a', type=str, dest='host',
                    help="Server's address. Default = 0.0.0.0. Listens to on all availible addresses.",
                    default='localhost', nargs='?')
parser.add_argument('-p', type=int, action='store', dest='port',
                    help="Server's TCP port for clients to connect.",
                    default=7777, nargs='?')
parser.add_argument('-i', dest='interactive', help="Interactive mode", action="store_true", default=False)
args = parser.parse_args()

host = str(args.host)
port = int(args.port)
interactive = args.interactive


def create_message():
    message = {"action": "echo"}
    message_time = time.time()
    message['time'] = message_time
    if interactive:
        print('You started client in Interactive mode. Enter action and data.')
        message['action'] = input('acton: ')
        message['data'] = input('data: ')
    else:
        message['action'] = 'echo'
        message["data"] = 'Test'
    return json.dumps(message).encode(encoding)


def send_message(sock, data):
    try:
        sock.send(data)
    except:
        print("We couldn't send the message. Check the server on:" + host)
    finally:
        print("The message: " + data.decode(encoding) + " was sucessfuly sent to the Server.")


def get_servers_message(sock):
    response = sock.recv(buffersize).decode(encoding)
    return json.loads(response)


def parse_message(response):
    server_message = response
    if server_message["action"] == "response":
        response_time = (server_message["time"] - message_time)
        print(f'Successul responce received in: {round(response_time, 4)} ms')
    else:
        print(f'Received from the Server: {server_message}')


try:
    sock = socket.socket()
    sock.connect((host, port))
except socket.error:
    print("I can't connect to the server: " + host + ". Check the connection.")
finally:
    send_message(sock, create_message())
    parse_message(get_servers_message(sock))
