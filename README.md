
### Requirements

Install the necessary requirements with `pip`

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip3 install --upgrade pip -r requirements.txt`

### Usage

Run a server locally on port `22555`

`python3 -m ssh.server localhost 22555`

Use an SSH client to connect to the server

`ssh user@localhost -p 22555`

### Host Keys

SSH servers use host keys to identify themselves. SSH clients store trusted server public keys in `~/.ssh/knownhosts`. If the server is not a known host, the client will be requested if it wants to add the server's host key before proceeding with authentication.

### Authorized Keys

Authorized keys are public keys that are used to authenticate clients. This can be used instead of password authentication. 

The server receives the client's public key. If it is found in `~/.ssh/authorized_keys`, the server encrypts a challenge message with the public key. If the client can decrypt the message with the corresponding private key, it has proven its identity and is granted access.

To add a client, append the client's public key to the `authorized_keys` file. For example,

`cat id_rsa.pub >> authorized_keys`
