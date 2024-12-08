"""
Class for an SSH server instance.

Run a SSH server on a specified address with:

``python3 -m ssh.server [-h] [-a ADDRESS] [-p PORT]``

"""

import argparse
from logging import getLogger
import socket
import threading

from paramiko import RSAKey
from paramiko.transport import Transport

from .interface import SSHServerInterface
from . import logger

MAX_CONNECTIONS = 5
HOST_KEY = RSAKey.generate(2048)


class SSHServer():

    def __init__(self, host='0.0.0.0', port=2222):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.addr = (host, port)
        self.sessions = {}

    def start(self):
        """
        Start the SSH server.
        """
        self.socket.bind(self.addr)
        self.socket.listen(MAX_CONNECTIONS)
        
        try:
            while True:
                client_socket, addr = self.socket.accept()
                logger.info('Connection from %r', addr)
                session_t = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,),
                    daemon=True
                )
                self.sessions[addr] = session_t
        except KeyboardInterrupt:
            logger.info('Exiting server')

    def handle_client(client_socket):
        """
        Handle an individual SSH client.
        """
        try:
            transport = paramiko.Transport(client_socket)
            transport.add_server_key(HOST_KEY)
            
            server_interface = SSHServerInterfaec()
            transport.start_server(server=server)

            channel = transport.accept(20)
            if channel is None:
                logger.info('No channel request from client')
                return
            
            while True:
                data = channel.recv(1024)
                channel.send(f'Echo: {data.decode()}')
        except Exception as exc:
            logger.info('%r', exc)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='SSH server'
    )
    parser.add_argument(
        '-a',
        '--address',
        type=str,
        default='0.0.0.0'
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=2222
    )
    
    args = parser.parse_args()
    host = args.address
    port = args.port
    server = SSHServer(host, port)
    server.start()
