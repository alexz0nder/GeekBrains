import socket

from datetime import datetime
from argparse import ArgumentParser
from handlers import create_message, get_response_message


buffer_size = 1024
encoding = 'utf-8'
message_time = datetime.now().timestamp()

parser = ArgumentParser()
parser.add_argument('-a', type=str, dest='host',
                    help="Server's address. Default = 0.0.0.0. Listens to on all availible addresses.",
                    default='localhost', nargs='?')
parser.add_argument('-p', type=int, action='store', dest='port',
                    help="Server's TCP port for clients to connect.",
                    default=7777, nargs='?')
parser.add_argument('-i', dest='interactive', help="Interactive mode", action="store_true", default=True)
parser.add_argument('-m', '--mode', type=str, dest='mode', help="Sets client mode", default='w')
args = parser.parse_args()

host = str(args.host)
port = int(args.port)
interactive = args.interactive


def send_message(sock, data):
    try:
        sock.send(data)
    except:
        print("We couldn't send the message. Check the server on:" + host)
    else:
        print("The message:  was successfully sent to the Server.")


try:
    sock = socket.socket()
    sock.connect((host, port))
except socket.error:
    print("I can't connect to the server: " + host + ". Check the connection.")
else:
    if args.mode == 'w':
        while True:
            send_message(sock, create_message(message_time, interactive, encoding))
    else:
        while True:
            print(f'Returned from the Server: {get_response_message(sock, buffer_size, encoding)}')
