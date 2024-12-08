
### Usage

Run a server locally on port `22555`

`python3 -m ssh.server localhost 22555`

Use an SSH client to connect to the server

`$ ssh user@localhost -p 22555`

### Host Keys

SSH servers use host keys to identify themselves. SSH clients store trusted server public keys in `~/.ssh/knownhosts`. If the server is not a known host, the client will be requested if it wants to add the server's host key before proceeding with authentication.

### Authorized Keys

Authorized keys are public keys that are used for authenticating clients. This can be used instead of password authentication. The client is granted access to the server if it can decrypt a challenge message with the private key corresponding to the authorized public key.
