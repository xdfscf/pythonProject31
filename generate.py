import os
import random
import time
import paramiko
import sys


def generate_files(num_files, file_size, directory):
    """ Generates a number of files with specified size in a directory. """
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(num_files):
        filename = os.path.join(directory, f"test_file_{i}.dat")
        with open(filename, 'wb') as f:
            f.write(os.urandom(file_size * 1024 * 1024))  # Generate random bytes multiplied by 1MB

NUM_FILES = 100
FILE_SIZE_MB = 2
DIRECTORY = 'test_files'

if __name__ == "__main__":

    # Generate test files
    print("Generating test files...")
    generate_files(NUM_FILES, FILE_SIZE_MB, DIRECTORY)
    print("File generation complete.")