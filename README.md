
### Requirements

Install the necessary requirements with `pip`

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip3 install --upgrade pip -r requirements.txt`

### Usage

#### Server

Run a server locally on port `22555`

`python3 -m ssh.server -a localhost -p 22555`

#### Client

To connect an OpenSSH client to connect to the server

`ssh user@localhost -p 22555`

To connect a paramiko client with the server:

`python3 -m ssh.client -a localhost -p 22555`

### API

```python

from ssh import server

ssh_server = SSHServer('localhost', port=2222)
ssh_server.start()

```

```python

from ssh import client

ssh_client = SSHClient('localhost', port=2222)
ssh_client.start()

ssh_client.send(b'data')

````

### Host Keys

SSH servers use host keys to identify themselves. SSH clients store trusted server public keys in `~/.ssh/knownhosts`. If the server is not a known host, the client is asked if it wants to add the server's key before proceeding with authentication.

### Authorized Keys

Authorized keys are public keys that are used to authenticate clients. This can be used instead of password authentication. 

The server receives the client's public key. If it is found in `~/.ssh/authorized_keys`, the server encrypts a challenge message with the public key. If the client can decrypt the message with the corresponding private key, it has proven its identity and is granted access.

To add a client, append the client's public key to the `authorized_keys` file. For example,

`cat id_rsa.pub >> authorized_keys`
