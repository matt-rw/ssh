"""
Class for an SSH server instance.

Run a SSH server on a specified address with:

``python3 -m ssh.server [-h] [-a ADDRESS] [-p PORT]``

"""

import argparse
from logging import getLogger
import os
import socket
import threading

import paramiko
from paramiko import RSAKey
from paramiko.transport import Transport

from .interface import SSHServerInterface
from . import logger

MAX_CONNECTIONS = 5
KEY_DIR = 'keys/server'


class SSHServer():

    def __init__(self, host='0.0.0.0', port=2222):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.addr = (host, port)
        self.sessions = {}

        self.host_key = paramiko.Ed25519Key.from_private_key_file(
            os.path.join(KEY_DIR, 'id_ed25519')
        )

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
                    args=(client_socket, addr),
                    daemon=True
                )
                self.sessions[addr] = session_t
                session_t.start()
        except KeyboardInterrupt:
            logger.info('Exiting server')

    def handle_client(self, client_socket, addr):
        """
        Handle an individual SSH client.
        """
        try:
            transport = paramiko.Transport(client_socket)
            transport.add_server_key(self.host_key)
            
            server_interface = SSHServerInterface()
            transport.start_server(server=server_interface)

            channel = transport.accept(20)
            if not transport.is_authenticated():
                logger.info('Failed to authenticate %r', addr)
                return
            elif channel is None:
                logger.info('No channel request received')
                return

            channel.send(f'Connected to SSH server on {self.addr}\n')
            
            # Channel loop
            while True:
                data = channel.recv(1024)
                # print(data.decode('utf-8'))
                print(data.decode('utf-8'))
                # channel.send(bytes(f'Echo: {data.decode()}'))
                channel.send(data)

        except Exception as exc:
            logger.info('%r', exc)
        finally:
            logger.info(f'Closing connection with {addr}')
            client_socket.close()


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
