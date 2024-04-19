import paramiko
import os
import six

def generate_keys(path="./", private_key_file="private_key.pem", public_key_file="public_key.pem"):
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    if os.path.exists(private_key_file) and os.path.exists(public_key_file):
        print("keys already exist, using previous keys")
        return

    private_key_file = os.path.join(path, private_key_file)
    public_key_file = os.path.join(path, public_key_file)
    key = paramiko.RSAKey.generate(bits=2048)

    privateString = six.StringIO()
    key.write_private_key(privateString)

    with open(private_key_file, 'wb') as f:
        f.write(privateString.getvalue().encode())

    privateString.close()

    with open(public_key_file, 'wb') as f:
        f.write(key.get_base64().encode())

def get_private_key(private_key_file="private_key.pem"):
    if not os.path.exists(private_key_file):
        raise "not a valid path"
    try:
        private_key = paramiko.RSAKey(filename=private_key_file)
        return private_key
    except paramiko.ssh_exception.SSHException:
        raise "key formats error"