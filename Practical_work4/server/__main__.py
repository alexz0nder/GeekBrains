import json, time, socket, yaml
from argparse import ArgumentParser

from actions import resolve
from protocol import validate_request, make_response

buffersize = 1024
encoding = 'utf-8'

# First of all let's check if we started with arguments passed
# All arguments has a Default value to run Server in ANY way
parser = ArgumentParser()
parser.add_argument('-a', type=str, dest='host',
                    help="Server's address. Default = 0.0.0.0. Listens to on all availible addresses.",
                    default='0.0.0.0', nargs='?')
parser.add_argument('-p', type=int, action='store', dest='port',
                    help="Server's TCP port for clients to connect.",
                    default=7777, nargs='?')
parser.add_argument('-c', type=str, action='store', dest='config_file',
                    help="Config file name. Default name is config.yml")
args = parser.parse_args()

server_address = args.host
server_port = args.port

# And if there is a config file, parameters from there are prior to console attributes
if args.config_file:
    with open(args.config_file, 'r') as file:
        config = yaml.load(file, Loader=yaml.Loader)
        server_address = config['address']
        server_port = config['port']


# Here is a function to get a message from a client
# Where 'client' is a connection to a client
# Here we get data from a client, decode it from bites and deserialize it
def get_message_from_client(client):
    data = json.loads(client.recv(buffersize).decode(encoding))
    print(f'have got a message: {str(data)}')
    return data


# Main finction of the server.
# It parses the client's message, finds a function that connected to a name of client's requested action
# and returns server's response from that function
def parse_message(request):

    if validate_request(request):
        action_name = request['action']
        controller = resolve(action_name)
        if controller:
            server_response = controller(request)
        else:
            server_response = make_response(request, 404, 'Action not found')
    else:
        server_response = make_response(request, 400, 'Wrong request')

    return server_response


# The function to send a response to a client
def send_response(client, data):
    client.send(json.dumps(data).encode(encoding))
    client.close()
    return


try:
    sock = socket.socket()
    sock.bind((server_address, server_port))
    sock.listen(5)
    print(f'Server was started with {server_address}:{server_port}')

    while True:
        client, address = sock.accept()
        print(f'Client was detected {address}')

        message = get_message_from_client(client)
        send_response(client, parse_message(message))
except KeyboardInterrupt:
    pass
