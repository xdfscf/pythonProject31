import paramiko
import os


import six

private_key_file = './'
public_key_file = './'


key = paramiko.RSAKey.generate(bits=2048)

privateString = six.StringIO()
key.write_private_key(privateString)


with open(private_key_file, 'wb') as f:
    f.write(privateString.getvalue().encode())

privateString.close()

with open(public_key_file, 'wb') as f:
    f.write(key.get_base64().encode())

import socket
print(socket.gethostbyname(socket.gethostname()))

import paramiko
import os
import threading


class SFTPServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):

        return paramiko.AUTH_SUCCESSFUL

    def check_auth_publickey(self, username, key):

        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):

        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_exec_request(self, channel, command):

        if command.startswith('sftp'):
            return True
        return False

    def check_channel_subsystem_request(self, channel, name):

        if name == 'sftp':
            return True
        return False

    def begin_auth(self, username):

        pass

    def check_channel_shell_request(self, channel):

        return False


private_key = paramiko.RSAKey(filename='/content/drive/MyDrive/Colab Notebooks/keys/private_key.pem')


server = socket.gethostbyname(socket.gethostname())
port = 80


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind((server, port))
server_sock.settimeout(30)
server_sock.listen(10)

print("Waiting for client...")
client, addr = server_sock.accept()
print("Accepted connection from ", addr)

transport = paramiko.Transport(client)
transport.add_server_key(private_key)
server = SFTPServer()

try:
    transport.start_server(server=server)


    channel = transport.accept(20)
    print("SFTP session started.")


    channel.wait_close()
finally:

    transport.close()
    server_sock.close()