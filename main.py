import os, time
import tempfile
import paramiko
import datetime

__version__ = "0.0.2"

from paramiko.sftp_attr import SFTPAttributes


class Connection(object):
    def __init__(self, host, username=None, private_key=None, password=None, port=22, private_key_pass=None,
                 log=False, ):
        self._sftp_live = False
        self._sftp = None
        if not username:
            username = os.environ['LOGNAME']
        if log:
            templog = tempfile.mkstemp('.txt', 'ssh-')[1]
            paramiko.util.log_to_file(templog)
        self._transport = paramiko.Transport((host, port))
        self._tranport_live = True

        if password:
            self._transport.connect(username=username, password=password)
        else:
            # Use Private Key.
            if not private_key:
                # Try to use default key.
                if os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
                    private_key = '~/.ssh/id_rsa'
                elif os.path.exists(os.path.expanduser('~/.ssh/id_dsa')):
                    private_key = '~/.ssh/id_dsa'
                else:
                    raise TypeError("You have not specified a password or key.")
            private_key_file = os.path.expanduser(private_key)
            try:
                xSx_key = paramiko.RSAKey.from_private_key_file(private_key_file, private_key_pass)
            except paramiko.SSHException:
                xSx_key = paramiko.DSSKey.from_private_key_file(private_key_file, password=private_key_pass)
            self._transport.connect(username=username, pkey=xSx_key)

    def _sftp_connect(self):
        """Establish the SFTP connection."""
        if not self._sftp_live:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            self._sftp_live = True

    def listdir(self, path='.'):
        """return a list of files for the given path"""
        self._sftp_connect()
        return self._sftp.listdir(path)

    def chdir(self, path):
        """change the current working directory on the remote"""
        self._sftp_connect()
        self._sftp.chdir(path)

    def getcwd(self):
        """return the current working directory on the remote"""
        self._sftp_connect()
        return self._sftp.getcwd()

    def execute(self, command):
        """Execute the given commands on a remote machine."""
        ssh_session = self._transport.open_session()
        ssh_session.exec_command(command)

        stdout = ssh_session.makefile("rb", -1).read().decode()
        stderr = ssh_session.makefile_stderr("rb", -1).read().decode()

        return stdout, stderr

    def get(self, remotepath, localpath=None):
        """Copies a file between the remote host and the local host."""
        if not localpath:
            localpath = os.path.split(remotepath)[1]
        self._sftp_connect()
        self._sftp.get(remotepath, localpath)

    def put(self, localpath, remotepath=None):
        """Copies a file between the local host and the remote host."""
        if not remotepath:
            remotepath = os.path.split(localpath)[1]
        self._sftp_connect()
        self._sftp.put(localpath, remotepath)

    def get_file_size(self, remotepath):
        """ Return File size in bytes """
        # import pdb; pdb.set_trace()
        self._sftp_connect()
        st = self._sftp.stat(remotepath)
        return st.st_size

    def get_file_created_data(self, remotepath):
        """ Return the File created time """
        self._sftp_connect()
        st = self._sftp.stat(remotepath)
        return datetime.datetime.strptime(time.ctime(st.st_atime), "%a %b %d %H:%M:%S %Y")

    def open(self, filename, mode='r', bufsize=-1):
        """ Open given path File and return file object """
        self._sftp_connect()
        return self._sftp.open(filename, mode, bufsize)

    def rename(self, oldpath, newpath):
        """ Re-name old name to New name """
        self._sftp_connect()
        self._sftp.rename(oldpath, newpath)

    def mkdir(self, path, mode=0o777):
        """ Create New dir on given path, as given file permission """
        self._sftp_connect()
        self._sftp.mkdir(path, mode=0o777)

    def chmod(self, path, mode):
        """ Change the permision of path """
        self._sftp_connect()
        self._sftp.chmod(path, mode)

    def rmdir(self, path):
        """ Remove the given file path directory"""
        self._sftp_connect()
        self._sftp.rmdir(path)

    def remove_file(self, path):
        """Remove the given File path """
        self._sftp_connect()
        self._sftp.remove(path)

    def close(self):
        """Closes the connection and cleans up."""
        # Close SFTP Connection.
        if self._sftp_live:
            self._sftp.close()
            self._sftp_live = False
        # Close the SSH Transport.
        if self._tranport_live:
            self._transport.close()
            self._tranport_live = False

hostname = '192.168.1.3'
username= 'xdfscf'
password= '13579qetuo'



while True:
    user_input = input("Please enter instruction: ")

    if user_input.startswith("execute"):
        ftp = Connection(host=hostname, port=80, password='13579qetuo', username=username)
        instruct=user_input.replace("execute ", "")
        stdout, stderr = ftp.execute(instruct)
        print(stdout)
        ftp.close()
    else:
        ftp = Connection(host=hostname, port=80, password='13579qetuo', username=username)
        method_name=user_input.split()[0]
        args=user_input.split()[1:]
        if hasattr(ftp, method_name):
            method = getattr(ftp, method_name)
            stdout=method(*args)
            print(stdout)
        else:
            print("No such method")
        ftp.close()

