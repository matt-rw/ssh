"""SSH Client."""

import argparse
from dataclasses import dataclass

import paramiko
from paramiko import SSHClient as Client
from paramiko.ssh_exception import NoValidConnectionsError


# class SSHClientConfig(dataclass):
    # remote: str = ''
    # port: int = 0
    # username: str = ''

class SSHClient:

    def __init__(self, remote, port, username='user'):
        self.remote = remote
        self.port = port
        self.username = username
        self.ssh = Client()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.transport = None

    def start(self):
        """Connect to the SSH server."""
        try:
            self.ssh.connect(self.remote, port=self.port, username=self.username)
        except NoValidConnectionsError:
            print('Failed to connect')
            return
        self.transport = self.ssh.get_transport() 
        channel = self.open_session()

        while True:
            data = input('Input: ')
            channel.send('Hello')
            channel.recv(1024)


    def open_session():
        """Open a new session on the transport."""
        transport.open_session()

            
if __name__ == '__main__':

    parser = argparse.ArgumentParser('SSH client.')
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
    client = SSHClient(args.address, args.port)
    client.start()
