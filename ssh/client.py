"""SSH Client."""

import argparse
import os

import paramiko
from paramiko import SSHClient as Client
from paramiko.ssh_exception import NoValidConnectionsError


KEY_DIR = 'keys/client'

class SSHClient:

    def __init__(self, remote, port, username='user'):
        self.remote = remote
        self.port = port
        self.username = username
        self.ssh = Client()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.transport = None
        
        key_path = os.path.join(KEY_DIR, 'id_ecdsa')
        with open(key_path, 'r') as f:
            key = f.read()
        print(key)
        self.private_key = paramiko.ECDSAKey.from_private_key_file(key_path)
        self.ssh.load_host_keys(os.path.join(KEY_DIR, 'known_hosts'))

    def start(self):
        """Connect to the SSH server."""
        try:
            self.ssh.connect(
                hostname=self.remote,
                port=self.port, 
                username=self.username,
                pkey=self.private_key
            )
        except NoValidConnectionsError:
            print('Failed to connect')
            return
        self.transport = self.ssh.get_transport() 
        channel = self.transport.open_session()

        recv = channel.recv(1024)
        print(recv.decode('utf-8'))
        while True:
            data = input('Input: ')
            channel.send(data.encode('utf-8'))
            recv = channel.recv(1024)
            print(recv.decode('utf-8'))

    def open_session(self):
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
