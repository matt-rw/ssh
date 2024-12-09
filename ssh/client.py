"""SSH Client."""

import paramiko
from paramiko import SSHClient

class SSHClient:

    def __init__(self, remote, port, username='user'):
        self.ssh = SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.transport = None

    def start(self):
        """Connect to the SSH server."""
        self.ssh.connect(remote, port=port, username=username)
        self.transport = self.ssh.get_transport() 
        channel = self.open_session()

        while True:
            data = input('Input: ')
            channel.send('Hello')
            channel.recv(1024)


    def open_session():
        """Open a new session on the transport."""
        transport.open_session()

            
        
