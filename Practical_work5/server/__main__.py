import json, time, socket, yaml, logging
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


logger = logging.getLogger('server_main')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(messege)s')
file_handler = logging.FileHandler('server_main.log')

file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logging.CRITICAL

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


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
    logger.info('have got a message: ' + str(data))
    return data


# Main function of the server.
# It parses the client's message, finds a function that connected to a name of client's requested action
# and returns server's response from that function
def parse_message(request):

    if validate_request(request):
        action_name = request['action']
        controller = resolve(action_name)
        if controller:
            server_response = controller(request)
        else:
            logger.error('404 - request: ' + str(request))
            server_response = make_response(request, 404, 'Action not found')
    else:
        logger.error('400 - request: ' + str(request))
        server_response = make_response(request, 400, 'Wrong request')

    logger.info('200 - request: ' + str(request))
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
    logger.info('Server was started with ' + str(server_address) + ':' + str(server_port))

    while True:
        client, address = sock.accept()
        logger.info('Client was detected ' + str(address))

        message = get_message_from_client(client)
        send_response(client, parse_message(message))
except KeyboardInterrupt:
    pass
