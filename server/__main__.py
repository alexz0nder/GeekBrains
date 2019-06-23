import socket
import yaml
import logging
import os
import select
import threading
from argparse import ArgumentParser
from handlers import handle_default_request, client_send

buffersize = 1024
encoding = 'utf-8'
main_log_file = os.path.dirname(os.path.abspath(__file__)) + '/logs/main.log'
debug_level = logging.INFO #logging.DEBUG
connections = []
requests = []

# First of all let's check if we started with arguments passed
# All arguments has a Default value to run Server in ANY way.
parser = ArgumentParser()
parser.add_argument('-a', '--address', type=str, dest='host', default='127.0.0.1', nargs='?',
                    help="Server's address. Default = 0.0.0.0. Listens to on all available addresses.")
parser.add_argument('-p', '--port', type=int, action='store', dest='port', default=7777, nargs='?',
                    help="Server's TCP port for clients to connect.")
parser.add_argument('-c', '--config', type=str, action='store', dest='config_file',
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
    level=debug_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(main_log_file, encoding=encoding),
        logging.StreamHandler()
    ]
)


# This is the main program which creates a SOCKET, listen to clients connetions and responds
# to them with functions above
if __name__ == "__main__":
    try:
        sock = socket.socket()
        sock.bind((server_address, server_port))
        sock.setblocking(False)
        sock.listen(5)
        logging.info('Server was started with ' + str(server_address) + ':' + str(server_port))

        while True:
            try:
                client, address = sock.accept()
                logging.info(f'Client with {address } was detected ')
                connections.append(client)
            except ConnectionResetError:
                logging.info('Server was successfully stopped')
                pass
            except:
                pass

            rlist, wlist, xlist = select.select(connections, connections, connections, 0)

            for r_client in rlist:
                r_thread = threading.Thread(target=requests.append, args=(r_client.recv(buffersize),))
                r_thread.start()

            if requests:
                raw_response = handle_default_request(requests.pop(), encoding)
                logging.debug(f"Server's response is {raw_response}")

                logging.debug(f'raw_response: {raw_response}')
                for w_client in wlist:
                    w_thread = threading.Thread(target=client_send, args=(w_client, raw_response,))
                    logging.debug(f'w_thread: {w_thread}')
                    w_thread.start()

    except ConnectionResetError:
        logging.info('Server was successfully stopped by stopping client')
        pass

    except KeyboardInterrupt:
        pass

    finally:
        for client in connections:
            client.close()
