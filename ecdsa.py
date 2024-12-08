"""ECDSA key."""
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


private_key = ec.generate_private_key(ec.SECP521R1())
private_key_bytes = private_key.private_bytes()
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.OpenSSH,
    encryption_algorithm=serialization.NoEncryption()
)

with open('id_ecdsa_521', 'wb') as f:
    f.write(private_key_bytes)

public_key = private_key.public_key()
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.OpenSSH,
    format=serialization.PublicFormat.OpenSSH
)

with open('id_ecdsa_521.pub', 'wb') as f:
    f.write(public_key_bytes)


