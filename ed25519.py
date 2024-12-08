"""Edward's curve ED25519 key."""
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from cryptography.exceptions import InvalidSignature


private_key = ed25519.Ed25519PrivateKey.generate()

# The following is the same as private_bytes_raw()
private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption()
)

with open('id_ed25519', 'wb') as f:
    f.write(private_bytes)

loaded_private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_bytes)

private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.OpenSSH,
    encryption_algorithm=serialization.NoEncryption()
)

with open('id_ed25519', 'wb') as f:
    f.write(private_bytes)

# The following returns a 64 byte signature
signature = private_key.sign(b'authentication message')

public_key = private_key.public_key()

public_bytes = public_key.public_bytes_raw()

loaded_public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)

public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.OpenSSH,
    format=serialization.PublicFormat.OpenSSH
)

with open('id_ed25519.pub', 'wb') as f:
    f.write(public_bytes)

try:
    public_key.verify(signature, b'authentication message')
    print('authenticated')
except InvalidSignature:
    print('not authenticated')
