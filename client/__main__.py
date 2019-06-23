import socket
import threading
from datetime import datetime
from argparse import ArgumentParser
from handlers import create_message, get_response_message


buffer_size = 1024
encoding = 'utf-8'
message_time = datetime.now().timestamp()


# Arguments parser which determines in which mode to start the main program
parser = ArgumentParser()
parser.add_argument('-i', dest='interactive', help="Interactive mode", action="store_true", default=True)
parser.add_argument('-m', '--mode', type=str, dest='mode', help="Sets client mode", default='w')
parser.add_argument('-a', type=str, dest='host', default='localhost', nargs='?',
                    help="Server's address. Default = 0.0.0.0. Listens to on all availible addresses.")
parser.add_argument('-p', type=int, action='store', dest='port', default=7777, nargs='?',
                    help="Server's TCP port for clients to connect.")
args = parser.parse_args()

host = str(args.host)
port = int(args.port)
interactive = args.interactive


# Infinitive loop of sanding messages, in case interactive flag is True it will be asking you for imput...
def send_message(client_socket):
    while True:
        try:
            client_socket.send(create_message(message_time, interactive, encoding))
        except:
            print("We couldn't send the message. Check the server on:" + host)
            client_socket.close()
            pass
        else:
            print("The message:  was successfully sent to the Server.")
        finally:
            client_socket.close()
            pass


# Infinitive loop of getting messages process that will be running in the Daemon mode in Threads
def read_message(client_socket):
    while True:
        try:
            print(f'Returned from the Server: {get_response_message(client_socket, buffer_size, encoding)}')
        except:
            pass
        finally:
                client_socket.close()


# this is the main program that corresponds to mode argument and starts the Client in asked mode.
# In write mode it asks to enter some actions
# in read mode it just listens to the server and prints its responses
# And if you start the client in ReadWrite mode, it starts reading process in background as Daemon
# and always asks to send message to the server.
if __name__ == "__main__":
    try:
        sock = socket.socket()
        sock.connect((host, port))
    except socket.error:
        print("I can't connect to the server: " + host + ". Check the connection.")
        exit(1)
    else:
        if args.mode == 'w':
            send_message(sock)
        elif args.mode == 'r':
            read_message(sock)
        elif args.mode == 'rw':
            r_thread = threading.Thread(target=read_message, args=(sock,), daemon=True)
            r_thread.start()
            send_message(sock)
        else:
            print(f'Sorry. There is no {args.mode} mode')
