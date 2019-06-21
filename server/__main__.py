import json
import socket
import yaml
import logging
import os
from argparse import ArgumentParser
from handlers import handle_default_request

buffersize = 1024
encoding = 'utf-8'
main_log_file = os.path.dirname(os.path.abspath(__file__)) + '/logs/main.log'


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


# Configure Logging basic options to log into the file  which we defined in the variable main_log
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(main_log_file, encoding=encoding),
        logging.StreamHandler()
    ]
)


# This function is about to get a message from a client
# It gets data from a client, decode it from bites and deserialize it
def get_message_from_client(client):
    data = client.recv(buffersize)
    logging.info('have got bites message: ' + str(data))
    return data


# The function to send a response back to the client
def send_response(client, data):
    client.send(data)
    client.close()


# This is the main program which creates a SOCKET, listen to clients connetions and responds
# to them with functions above
if __name__ == "__main__":
    try:
        sock = socket.socket()
        sock.bind((server_address, server_port))
        sock.listen(5)
        logging.info('Server was started with ' + str(server_address) + ':' + str(server_port))

        while True:
            client, address = sock.accept()
            logging.info('Client was detected ' + str(address))

            raw_request = get_message_from_client(client)
            send_response(client, handle_default_request(raw_request, encoding))
    except KeyboardInterrupt:
        pass
