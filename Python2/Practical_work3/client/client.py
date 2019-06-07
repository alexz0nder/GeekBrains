import socket, time, json
from argparse import ArgumentParser

buffersize = 1024
encoding = 'utf-8'
message_time = time.time()

parser = ArgumentParser()
parser.add_argument('addr', action='store', help="Server's address.", default='server')
parser.add_argument('port', type=int, help="Server's port to connect to. Default = 7777", default=7777, nargs='?')
args = parser.parse_args()

host = str(args.addr)
port = int(args.port)

def create_message():
    message = {"action": "echo"}
    message["time"] = message_time
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
