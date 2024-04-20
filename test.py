import os
import random
import time
import paramiko
import sys
import argparse
from main import Connection
from  key_generator import generate_keys, get_private_key

def sftp_throughput_test(server_ip, port, username, password, file_directory):
    """ Tests SFTP throughput by uploading files to a server. """
    # Setup SSH client and connect
    private_key_file = "client_private_key.pem"
    public_key_file = "client_public_key.pem"
    if not os.path.exists(private_key_file):
        generate_keys(private_key_file="client_private_key.pem", public_key_file="client_public_key.pem")
    private_key = get_private_key("client_private_key.pem")
    sftp = Connection(host=server_ip, port=port, password=password, username=username)

    total_bytes_transferred = 0
    start_time = time.time()

    # Iterate over each file in the directory and upload
    for filename in os.listdir(file_directory):
        filepath = os.path.join(file_directory, filename)
        if os.path.isfile(filepath):
            sftp.put(filepath, "./test/"+os.path.basename(filepath))
            total_bytes_transferred += os.path.getsize(filepath)

    end_time = time.time()

    # Calculate throughput
    elapsed_time = end_time - start_time
    throughput = total_bytes_transferred / elapsed_time / 1024 / 1024  # Convert bytes per second to MBps

    print(
        f"Transferred {total_bytes_transferred} bytes in {elapsed_time:.3f} seconds. Throughput: {throughput:.3f} MB/s")

    # Cleanup
    sftp.close()



# Configurations for the test
NUM_FILES = 100
FILE_SIZE_MB = 2

def main():
    parser = argparse.ArgumentParser(description="Run SFTP throughput test.")
    parser.add_argument('ip', help='Server IP address')
    parser.add_argument('port', type=int, help='Server port number')
    parser.add_argument('username', help='Username for authentication')
    parser.add_argument('password', help='Password for authentication')
    parser.add_argument('directory', help='Directory containing test files')

    args = parser.parse_args()

    # Now, call your function with these parameters
    print("Starting throughput test...")
    sftp_throughput_test(args.ip, args.port, args.username, args.password, args.directory)
    print("Throughput test complete.")

if __name__ == "__main__":
    main()